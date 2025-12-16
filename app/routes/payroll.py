#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""급여 직접 입력 라우트 - 웹 폼을 통한 직접 입력 기능"""

import os
import sys
import uuid
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app, flash
from flask_login import current_user

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.forms.payroll_forms import EmployeeInputForm
from payroll_generator.calculator import PayrollCalculator
from app.utils.analytics import (
    log_activity, 
    log_payroll_calculation, 
    calculate_totals_from_results
)

# Blueprint 생성
payroll_bp = Blueprint('payroll', __name__, url_prefix='/input')


@payroll_bp.route('/', methods=['GET', 'POST'])
def input_form():
    """단일 직원 입력 폼"""
    form = EmployeeInputForm()
    
    if form.validate_on_submit():
        # 폼 데이터를 딕셔너리로 변환 (기존 엑셀 입력 형식과 동일하게)
        employee_data = {
            '이름': form.name.data,
            '주민번호': form.resident_number.data,
            '입사일': form.hire_date.data.strftime('%Y-%m-%d'),
            '기본급': form.base_salary.data,
            '부양가족수': form.dependents.data,
            '소속': form.department.data or '',
            '직급': form.position.data or '',
            '은행명': form.bank_name.data or '',
            '계좌번호': form.account_number.data or '',
            '연장근무시간': form.overtime_hours.data or 0,
            '연장근무단가': form.overtime_rate.data or 0,
            '상여금': form.bonus.data or 0,
            '공제사항': form.deduction_note.data or ''
        }
        
        # 급여 계산 (기존 계산 로직 재사용)
        calculator = PayrollCalculator()
        payroll_data = calculator.calculate_deductions(employee_data)
        
        # 결과를 세션에 저장 (기존 결과 페이지와 호환)
        session_id = str(uuid.uuid4())
        results = [{
            'employee_name': employee_data['이름'],
            'payroll_data': payroll_data,
            'employee_data': employee_data
        }]
        
        session['session_id'] = session_id
        session['results'] = results
        session['period'] = form.period.data
        session['output_format'] = form.output_format.data
        # 디자인 선택: 'default'는 None으로 변환하여 기본 방식 사용
        design_name_value = form.design_name.data if hasattr(form, 'design_name') and form.design_name.data else None
        current_app.logger.info(f"[디자인 선택] 폼에서 받은 값: '{design_name_value}'")
        
        # 값 정규화 및 검증
        if design_name_value == 'default' or design_name_value == '':
            design_name_value = None
            current_app.logger.info("[디자인 선택] 'default'를 None으로 변환")
        elif design_name_value in ['design_1', 'design_2']:
            # design_1, design_2는 더 이상 지원하지 않음
            current_app.logger.warning(
                f"[디자인 선택] '{design_name_value}'는 더 이상 지원하지 않습니다. "
                f"기본 디자인으로 폴백합니다."
            )
            design_name_value = None
        elif design_name_value:
            # 유효한 디자인 이름인지 확인
            try:
                from payroll_generator.templates.designs.design_factory import DesignFactory
                if not DesignFactory.is_design_available(design_name_value):
                    current_app.logger.warning(f"[디자인 선택] 사용 불가능한 디자인: '{design_name_value}'")
                    current_app.logger.info(f"[디자인 선택] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                    design_name_value = None
                else:
                    current_app.logger.info(f"[디자인 선택] 유효한 디자인 확인: '{design_name_value}'")
            except Exception as e:
                current_app.logger.error(f"[디자인 선택] 디자인 검증 중 오류: {e}", exc_info=True)
                design_name_value = None
        
        session['design_name'] = design_name_value
        current_app.logger.info(f"[디자인 선택] 세션에 저장된 값: '{session.get('design_name')}'")
        session['input_method'] = 'web_form'  # 입력 방법 표시
        
        # Phase 4: 데이터 수집
        try:
            user_id = current_user.id if current_user.is_authenticated else None
            totals = calculate_totals_from_results(results)
            calculation_data = {
                'employee_count': 1,
                'period': form.period.data,
                'total_payroll': totals['total_payroll'],
                'total_deductions': totals['total_deductions'],
                'total_net_pay': totals['total_net_pay'],
                'results': results
            }
            log_payroll_calculation(user_id, calculation_data)
            log_activity(user_id, 'web_form_input', {'employee_count': 1})
        except Exception as e:
            current_app.logger.error(f'데이터 수집 오류: {str(e)}')
            # 데이터 수집 실패해도 메인 기능은 계속 진행
        
        # 기존 결과 페이지로 리다이렉트
        return redirect(url_for('main.result', session_id=session_id))
    
    # GET 요청 시 폼 표시
    # 활동 로그 저장
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        log_activity(user_id, 'page_view', {'page': 'input_form'})
    except Exception as e:
        current_app.logger.error(f'활동 로그 저장 오류: {str(e)}')
    
    return render_template('payroll/input_form.html', form=form)


@payroll_bp.route('/multiple', methods=['GET', 'POST'])
def multiple_input_form():
    """다중 직원 입력 폼"""
    if request.method == 'POST':
        try:
            # 폼 데이터 받기
            period = request.form.get('period')
            output_format = request.form.get('output_format', 'both')
            employees_data = request.form.getlist('employees')
            
            # employees 데이터 파싱 (Flask의 form 데이터 구조에 따라 조정 필요)
            # 실제로는 request.form에서 employees[0][name], employees[0][base_salary] 등으로 전달됨
            employees = []
            employee_index = 0
            
            while True:
                name = request.form.get(f'employees[{employee_index}][name]')
                if not name:
                    break
                
                employee_data = {
                    '이름': name,
                    '주민번호': request.form.get(f'employees[{employee_index}][resident_number]', ''),
                    '입사일': request.form.get(f'employees[{employee_index}][hire_date]', ''),
                    '기본급': int(request.form.get(f'employees[{employee_index}][base_salary]', 0) or 0),
                    '부양가족수': int(request.form.get(f'employees[{employee_index}][dependents]', 0) or 0),
                    '소속': request.form.get(f'employees[{employee_index}][department]', '') or '',
                    '직급': request.form.get(f'employees[{employee_index}][position]', '') or '',
                    '은행명': request.form.get(f'employees[{employee_index}][bank_name]', '') or '',
                    '계좌번호': request.form.get(f'employees[{employee_index}][account_number]', '') or '',
                    '연장근무시간': int(request.form.get(f'employees[{employee_index}][overtime_hours]', 0) or 0),
                    '연장근무단가': int(request.form.get(f'employees[{employee_index}][overtime_rate]', 0) or 0),
                    '상여금': int(request.form.get(f'employees[{employee_index}][bonus]', 0) or 0),
                    '공제사항': request.form.get(f'employees[{employee_index}][deduction_note]', '') or ''
                }
                
                # 필수 필드 검증
                if not employee_data['이름'] or not employee_data['주민번호'] or not employee_data['입사일'] or employee_data['기본급'] <= 0:
                    current_app.logger.warning(f'직원 {employee_index + 1} 필수 정보 누락')
                    employee_index += 1
                    continue
                
                employees.append(employee_data)
                employee_index += 1
            
            if not employees:
                flash('최소 1명의 직원 정보를 입력해주세요.', 'danger')
                return render_template('payroll/multiple_input.html')
            
            # 각 직원별 급여 계산
            calculator = PayrollCalculator()
            results = []
            
            for emp_data in employees:
                try:
                    payroll_data = calculator.calculate_deductions(emp_data)
                    results.append({
                        'employee_name': emp_data['이름'],
                        'payroll_data': payroll_data,
                        'employee_data': emp_data
                    })
                except Exception as e:
                    current_app.logger.error(f"급여 계산 오류: {emp_data.get('이름', '')} - {str(e)}")
                    continue
            
            if not results:
                flash('급여 계산 중 오류가 발생했습니다.', 'danger')
                return render_template('payroll/multiple_input.html')
            
            # 결과를 세션에 저장
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            session['results'] = results
            session['period'] = period
            session['output_format'] = output_format
            # 디자인 선택: 'default'는 None으로 변환하여 기본 방식 사용
            design_name_value = request.form.get('design_name', None)
            current_app.logger.info(f"[디자인 선택-다중] 폼에서 받은 값: '{design_name_value}'")
            
            # 값 정규화 및 검증
            if design_name_value == 'default' or design_name_value == '':
                design_name_value = None
                current_app.logger.info("[디자인 선택-다중] 'default'를 None으로 변환")
            elif design_name_value in ['design_1', 'design_2']:
                # design_1, design_2는 더 이상 지원하지 않음
                current_app.logger.warning(
                    f"[디자인 선택-다중] '{design_name_value}'는 더 이상 지원하지 않습니다. "
                    f"기본 디자인으로 폴백합니다."
                )
                design_name_value = None
            elif design_name_value:
                # 유효한 디자인 이름인지 확인
                try:
                    from payroll_generator.templates.designs.design_factory import DesignFactory
                    if not DesignFactory.is_design_available(design_name_value):
                        current_app.logger.warning(f"[디자인 선택-다중] 사용 불가능한 디자인: '{design_name_value}'")
                        design_name_value = None
                    else:
                        current_app.logger.info(f"[디자인 선택-다중] 유효한 디자인 확인: '{design_name_value}'")
                except Exception as e:
                    current_app.logger.error(f"[디자인 선택-다중] 디자인 검증 중 오류: {e}", exc_info=True)
                    design_name_value = None
            
            session['design_name'] = design_name_value
            current_app.logger.info(f"[디자인 선택-다중] 세션에 저장된 값: '{session.get('design_name')}'")
            session['input_method'] = 'web_form_multiple'
            
            # Phase 4: 데이터 수집
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
                log_activity(user_id, 'web_form_multiple_input', {'employee_count': len(results)})
            except Exception as e:
                current_app.logger.error(f'데이터 수집 오류: {str(e)}')
            
            # 기존 결과 페이지로 리다이렉트
            return redirect(url_for('main.result', session_id=session_id))
        
        except Exception as e:
            current_app.logger.exception(f'다중 직원 입력 처리 오류: {str(e)}')
            flash(f'처리 중 오류가 발생했습니다: {str(e)}', 'danger')
            return render_template('payroll/multiple_input.html')
    
    # GET 요청 시 폼 표시
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        log_activity(user_id, 'page_view', {'page': 'multiple_input_form'})
    except Exception as e:
        current_app.logger.error(f'활동 로그 저장 오류: {str(e)}')
    
    return render_template('payroll/multiple_input.html')


@payroll_bp.route('/preview', methods=['POST'])
def preview_calculation():
    """실시간 계산 미리보기 (AJAX)"""
    try:
        data = request.get_json()
        
        # 입력 데이터 검증 및 변환
        employee_data = {
            '기본급': data.get('base_salary', 0) or 0,
            '연장근무시간': data.get('overtime_hours', 0) or 0,
            '연장근무단가': data.get('overtime_rate', 0) or 0,
            '상여금': data.get('bonus', 0) or 0,
            '부양가족수': data.get('dependents', 0) or 0
        }
        
        # 급여 계산 (기존 계산 로직 재사용)
        calculator = PayrollCalculator()
        payroll_data = calculator.calculate_deductions(employee_data)
        
        return jsonify({
            'success': True,
            'payroll_data': payroll_data
        })
    except Exception as e:
        current_app.logger.error(f'미리보기 계산 오류: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

