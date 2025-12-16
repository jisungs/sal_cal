#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""메인 라우트 Blueprint - 급여명세서 생성 관련 라우트"""

import os
import sys
import uuid
import zipfile
import tempfile
from datetime import datetime
from flask import Blueprint, render_template, request, send_file, jsonify, session, current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from payroll_generator.calculator import PayrollCalculator
from payroll_generator.excel_handler import ExcelHandler
from payroll_generator.pdf_generator import PDFGenerator
from payroll_generator.logger import setup_logger
from flask_login import current_user
from app.utils.analytics import (
    log_activity, 
    log_payroll_calculation, 
    log_file_generation,
    calculate_totals_from_results
)

logger = setup_logger()

# Blueprint 생성
main_bp = Blueprint('main', __name__)


def allowed_file(filename):
    """파일 확장자 검증"""
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'xlsx', 'xls'})
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@main_bp.route('/')
def index():
    """메인 페이지"""
    # Phase 4: 페이지뷰 로그 저장
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        log_activity(
            user_id=user_id,
            activity_type='page_view',
            activity_data={'page': 'index'}
        )
    except Exception as e:
        logger.error(f'활동 로그 저장 오류: {str(e)}')
    
    return render_template('index.html')


@main_bp.route('/upload', methods=['POST'])
def upload_file():
    """파일 업로드 및 처리"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '파일이 없습니다.'}), 400
        
        file = request.files['file']
        period = request.form.get('period', datetime.now().strftime('%Y-%m'))
        output_format = request.form.get('format', 'both')
        
        if file.filename == '':
            return jsonify({'error': '파일을 선택해주세요.'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '엑셀 파일(.xlsx, .xls)만 업로드 가능합니다.'}), 400
        
        # 세션 ID 생성
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        
        # 파일 저장
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, f"{session_id}_{filename}")
        file.save(filepath)
        
        # 엑셀 파일 읽기
        excel_handler = ExcelHandler()
        try:
            df = excel_handler.read_employee_data(filepath)
        except FileNotFoundError as e:
            logger.exception(f"파일을 찾을 수 없음: {filepath}")
            return jsonify({'error': '업로드된 파일을 찾을 수 없습니다. 다시 업로드해주세요.'}), 404
        except PermissionError as e:
            logger.exception(f"파일 읽기 권한 없음: {filepath}")
            return jsonify({'error': '파일을 읽을 권한이 없습니다.'}), 403
        except ValueError as e:
            logger.exception(f"엑셀 파일 형식 오류: {str(e)}")
            return jsonify({'error': f'엑셀 파일 형식이 올바르지 않습니다: {str(e)}'}), 400
        except Exception as e:
            logger.exception(f"엑셀 파일 읽기 오류: {str(e)}")
            return jsonify({'error': f'엑셀 파일을 읽는 중 오류가 발생했습니다: {str(e)}'}), 400
        
        # 급여 계산
        calculator = PayrollCalculator()
        results = []
        
        for idx, row in df.iterrows():
            try:
                payroll_data = calculator.calculate_deductions(row.to_dict())
                results.append({
                    'employee_name': row.get('이름', f'직원{idx+1}'),
                    'payroll_data': payroll_data,
                    'employee_data': row.to_dict()
                })
            except Exception as e:
                logger.exception(f"급여 계산 오류: {row.get('이름', '')} - {str(e)}")
                continue
        
        # 세션에 결과 저장
        session['results'] = results
        session['period'] = period
        session['output_format'] = output_format
        session['filepath'] = filepath
        
        # Phase 4: 데이터 수집 - 급여 계산 결과 저장
        try:
            user_id = current_user.id if current_user.is_authenticated else None
            totals = calculate_totals_from_results(results)
            calculation_data = {
                'employee_count': len(results),
                'period': period,
                'total_payroll': totals['total_payroll'],
                'total_deductions': totals['total_deductions'],
                'total_net_pay': totals['total_net_pay'],
                'results': results
            }
            log_payroll_calculation(user_id, calculation_data)
            
            # 활동 로그 저장
            log_activity(
                user_id=user_id,
                activity_type='file_upload',
                activity_data={
                    'file_name': filename,
                    'employee_count': len(results),
                    'period': period,
                    'output_format': output_format
                }
            )
        except Exception as e:
            logger.error(f'데이터 수집 오류: {str(e)}')
            # 데이터 수집 실패해도 메인 기능은 계속 진행
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'count': len(results),
            'redirect': f'/result/{session_id}'
        })
        
    except RequestEntityTooLarge:
        return jsonify({'error': '파일 크기가 너무 큽니다. (최대 16MB)'}), 400
    except Exception as e:
        logger.exception(f"파일 업로드 오류: {str(e)}")
        return jsonify({'error': f'처리 중 오류가 발생했습니다: {str(e)}'}), 500


@main_bp.route('/result/<session_id>')
def result(session_id):
    """결과 페이지"""
    if 'results' not in session or session.get('session_id') != session_id:
        return render_template('error.html', message='세션이 만료되었거나 잘못된 접근입니다.'), 404
    
    results = session.get('results', [])
    period = session.get('period', '')
    output_format = session.get('output_format', 'both')
    
    return render_template('result.html', 
                         results=results, 
                         period=period,
                         output_format=output_format,
                         session_id=session_id)


@main_bp.route('/download/<format>/<employee_name>')
def download_file(format, employee_name):
    """개별 파일 다운로드"""
    if 'results' not in session:
        return jsonify({'error': '세션이 만료되었습니다.'}), 404
    
    results = session.get('results', [])
    period = session.get('period', '')
    output_folder = current_app.config['OUTPUT_FOLDER']
    
    # 해당 직원 찾기
    employee_result = None
    for result_item in results:
        if result_item['employee_name'] == employee_name:
            employee_result = result_item
            break
    
    if not employee_result:
        return jsonify({'error': '직원을 찾을 수 없습니다.'}), 404
    
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        
        if format == 'excel':
            excel_handler = ExcelHandler()
            output_path = os.path.join(output_folder, 'excel', 
                                     f"{employee_name}_급여명세서.xlsx")
            # 디자인 선택: 'default'는 None으로 변환하여 기본 방식 사용
            design_name = session.get('design_name', None)
            logger.info(f"[다운로드-Excel] 세션에서 읽은 design_name: '{design_name}'")
            
            if design_name == 'default':
                design_name = None
                logger.info("[다운로드-Excel] 'default'를 None으로 변환")
            
            if design_name:
                # 디자인 사용 가능 여부 확인
                try:
                    from payroll_generator.templates.designs.design_factory import DesignFactory
                    if not DesignFactory.is_design_available(design_name):
                        logger.warning(f"[다운로드-Excel] 사용 불가능한 디자인: '{design_name}', 기본 방식 사용")
                        logger.info(f"[다운로드-Excel] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                        design_name = None
                    else:
                        logger.info(f"[다운로드-Excel] 디자인 '{design_name}' 사용 가능 확인")
                except Exception as e:
                    logger.error(f"[다운로드-Excel] 디자인 검증 중 오류: {e}", exc_info=True)
                    design_name = None
            
            logger.info(f"[다운로드-Excel] 최종 사용할 design_name: '{design_name}'")
            excel_handler.write_payroll(
                employee_result['payroll_data'],
                output_path,
                employee_result['employee_data'],
                period,
                use_template=True,
                design_name=design_name
            )
            
            # Phase 4: 파일 생성 로그 저장
            try:
                file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                log_file_generation(
                    user_id=user_id,
                    file_type='excel',
                    file_name=f"{employee_name}_급여명세서.xlsx",
                    file_size=file_size,
                    employee_count=1,
                    period=period,
                    file_path=output_path
                )
                log_activity(
                    user_id=user_id,
                    activity_type='file_download',
                    activity_data={'file_type': 'excel', 'employee_name': employee_name}
                )
            except Exception as e:
                logger.error(f'파일 생성 로그 저장 오류: {str(e)}')
            
            return send_file(output_path, as_attachment=True)
        
        elif format == 'pdf':
            pdf_generator = PDFGenerator()
            output_path = os.path.join(output_folder, 'pdf',
                                     f"{employee_name}_급여명세서.pdf")
            # 디자인 선택: 'default'는 None으로 변환하여 기본 방식 사용
            design_name = session.get('design_name', None)
            logger.info(f"[다운로드-PDF] 세션에서 읽은 design_name: '{design_name}'")
            
            if design_name == 'default':
                design_name = None
                logger.info("[다운로드-PDF] 'default'를 None으로 변환")
            
            if design_name:
                # 디자인 사용 가능 여부 확인
                try:
                    from payroll_generator.templates.designs.design_factory import DesignFactory
                    if not DesignFactory.is_design_available(design_name):
                        logger.warning(f"[다운로드-PDF] 사용 불가능한 디자인: '{design_name}', 기본 방식 사용")
                        design_name = None
                    else:
                        logger.info(f"[다운로드-PDF] 디자인 '{design_name}' 사용 가능 확인")
                except Exception as e:
                    logger.error(f"[다운로드-PDF] 디자인 검증 중 오류: {e}", exc_info=True)
                    design_name = None
            
            logger.info(f"[다운로드-PDF] 최종 사용할 design_name: '{design_name}'")
            pdf_generator.generate_payslip(
                employee_result['payroll_data'],
                employee_result['employee_data'],
                output_path,
                period,
                use_template=True,
                design_name=design_name
            )
            
            # Phase 4: 파일 생성 로그 저장
            try:
                file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                log_file_generation(
                    user_id=user_id,
                    file_type='pdf',
                    file_name=f"{employee_name}_급여명세서.pdf",
                    file_size=file_size,
                    employee_count=1,
                    period=period,
                    file_path=output_path
                )
                log_activity(
                    user_id=user_id,
                    activity_type='file_download',
                    activity_data={'file_type': 'pdf', 'employee_name': employee_name}
                )
            except Exception as e:
                logger.error(f'파일 생성 로그 저장 오류: {str(e)}')
            
            return send_file(output_path, as_attachment=True)
        
        else:
            return jsonify({'error': '지원하지 않는 형식입니다.'}), 400
            
    except Exception as e:
        logger.exception(f"파일 다운로드 오류: {str(e)}")
        return jsonify({'error': f'파일 생성 오류: {str(e)}'}), 500


@main_bp.route('/batch_download/<format>')
def batch_download(format):
    """일괄 다운로드 (ZIP 파일)"""
    if 'results' not in session:
        return jsonify({'error': '세션이 만료되었습니다.'}), 404
    
    results = session.get('results', [])
    period = session.get('period', '')
    output_folder = current_app.config['OUTPUT_FOLDER']
    
    if format not in ['excel', 'pdf', 'both']:
        return jsonify({'error': '지원하지 않는 형식입니다.'}), 400
    
    try:
        # 임시 ZIP 파일 생성
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        zip_path = temp_zip.name
        temp_zip.close()
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            excel_handler = ExcelHandler()
            pdf_generator = PDFGenerator()
            # 디자인 선택: 'default'는 None으로 변환하여 기본 방식 사용
            design_name = session.get('design_name', None)
            logger.info(f"[일괄 다운로드] 세션에서 읽은 design_name: '{design_name}'")
            
            if design_name == 'default':
                design_name = None
                logger.info("[일괄 다운로드] 'default'를 None으로 변환")
            
            if design_name:
                # 디자인 사용 가능 여부 확인
                try:
                    from payroll_generator.templates.designs.design_factory import DesignFactory
                    if not DesignFactory.is_design_available(design_name):
                        logger.warning(f"[일괄 다운로드] 사용 불가능한 디자인: '{design_name}', 기본 방식 사용")
                        design_name = None
                    else:
                        logger.info(f"[일괄 다운로드] 디자인 '{design_name}' 사용 가능 확인")
                except Exception as e:
                    logger.error(f"[일괄 다운로드] 디자인 검증 중 오류: {e}", exc_info=True)
                    design_name = None
            
            logger.info(f"[일괄 다운로드] 최종 사용할 design_name: '{design_name}'")

            for result_item in results:
                employee_name = result_item['employee_name']
                payroll_data = result_item['payroll_data']
                employee_data = result_item['employee_data']
                
                if format in ['excel', 'both']:
                    excel_path = os.path.join(output_folder, 'excel',
                                            f"{employee_name}_급여명세서.xlsx")
                    excel_handler.write_payroll(
                        payroll_data, excel_path, employee_data, period, 
                        use_template=True, design_name=design_name
                    )
                    zipf.write(excel_path, f"{employee_name}_급여명세서.xlsx")
                
                if format in ['pdf', 'both']:
                    pdf_path = os.path.join(output_folder, 'pdf',
                                          f"{employee_name}_급여명세서.pdf")
                    pdf_generator.generate_payslip(
                        payroll_data, employee_data, pdf_path, period, 
                        use_template=True, design_name=design_name
                    )
                    zipf.write(pdf_path, f"{employee_name}_급여명세서.pdf")
        
        # Phase 4: 파일 생성 로그 저장
        try:
            user_id = current_user.id if current_user.is_authenticated else None
            file_size = os.path.getsize(zip_path) if os.path.exists(zip_path) else 0
            log_file_generation(
                user_id=user_id,
                file_type='zip',
                file_name=f'급여명세서_{period}_{format}.zip',
                file_size=file_size,
                employee_count=len(results),
                period=period,
                file_path=zip_path
            )
            log_activity(
                user_id=user_id,
                activity_type='file_download',
                activity_data={'file_type': 'zip', 'format': format, 'employee_count': len(results)}
            )
        except Exception as e:
            logger.error(f'파일 생성 로그 저장 오류: {str(e)}')
        
        return send_file(zip_path, as_attachment=True, 
                        download_name=f'급여명세서_{period}_{format}.zip')
        
    except Exception as e:
        logger.exception(f"일괄 다운로드 오류: {str(e)}")
        return jsonify({'error': f'ZIP 파일 생성 오류: {str(e)}'}), 500


def register_error_handlers(app):
    """에러 핸들러 등록"""
    @app.errorhandler(400)
    def bad_request(error):
        """400 에러 핸들러 - 잘못된 요청"""
        logger.warning(f"잘못된 요청: {error.description if hasattr(error, 'description') else str(error)}")
        if request.is_json:
            return jsonify({'error': '잘못된 요청입니다.'}), 400
        return render_template('error.html', message='잘못된 요청입니다.'), 400
    
    @app.errorhandler(403)
    def forbidden(error):
        """403 에러 핸들러 - 권한 없음"""
        logger.warning(f"권한 없음: {error.description if hasattr(error, 'description') else str(error)}")
        if request.is_json:
            return jsonify({'error': '접근 권한이 없습니다.'}), 403
        return render_template('error.html', message='접근 권한이 없습니다.'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """404 에러 핸들러"""
        logger.warning(f"페이지 없음: {request.path}")
        if request.is_json:
            return jsonify({'error': '페이지를 찾을 수 없습니다.'}), 404
        return render_template('error.html', message='페이지를 찾을 수 없습니다.'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 에러 핸들러"""
        logger.exception("서버 오류 발생")
        if request.is_json:
            return jsonify({'error': '서버 오류가 발생했습니다.'}), 500
        return render_template('error.html', message='서버 오류가 발생했습니다.'), 500

