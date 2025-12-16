# pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
import os
try:
    from .utils import mask_resident_number, normalize_path, resource_path
    from .logger import setup_logger
except ImportError:
    from utils import mask_resident_number, normalize_path, resource_path
    from logger import setup_logger

logger = setup_logger()

class PDFGenerator:
    def __init__(self):
        """PDF 생성기 초기화 및 한글 폰트 등록"""
        # 한글 폰트 경로 찾기 (여러 위치 확인)
        # PyInstaller 환경에서는 resource_path를 사용하여 올바른 경로 찾기
        font_paths = [
            # PyInstaller 빌드 환경 (build.spec에서 assets로 복사됨)
            resource_path('assets/NanumGothic.ttf'),
            # 개발 환경
            os.path.join(os.path.dirname(__file__), 'assets', 'NanumGothic.ttf'),
            # 나눔 글꼴 폴더 내 위치 (개발 환경)
            os.path.join(os.path.dirname(__file__), 'assets', '나눔 글꼴', '나눔고딕', 'NanumFontSetup_TTF_GOTHIC', 'NanumGothic.ttf'),
        ]
        
        font_path = None
        for path in font_paths:
            if os.path.exists(path):
                font_path = path
                break
        
        if font_path:
            try:
                pdfmetrics.registerFont(TTFont('NanumGothic', font_path))
                self.font_name = 'NanumGothic'
                logger.info(f"한글 폰트 등록 완료: {font_path}")
            except Exception as e:
                logger.warning(f"한글 폰트 등록 실패: {e}. 기본 폰트 사용")
                self.font_name = 'Helvetica'  # 폴백
        else:
            logger.warning(f"한글 폰트 파일을 찾을 수 없습니다. 다음 위치를 확인했습니다: {font_paths}. 기본 폰트 사용")
            self.font_name = 'Helvetica'  # 폴백
    
    def generate_payslip(self, payroll_data, employee_data, output_path, period, use_template=True, design_name=None):
        """급여명세서 PDF 생성
        
        Args:
            payroll_data (dict): calculator.calculate_deductions()의 반환값
            employee_data (dict): 직원 정보 (이름, 주민번호, 입사일 등)
            output_path (str): 출력 파일 경로
            period (str): 급여 기간 (예: "2025-01")
            use_template (bool): True면 엑셀 템플릿 사용, False면 코드 기반 생성 (기본값: True)
            design_name (str, optional): 디자인 이름 ('template_sample1', 'template_sample2', None)
                - 'template_sample1': 급여명세서 템플릿
                - 'template_sample2': 임금명세서 템플릿
                - 'design_1', 'design_2': 더 이상 지원하지 않음 (기본 디자인으로 폴백)
        """
        # 디자인 선택 시 디자인 클래스 사용
        if design_name:
            # design_1, design_2는 더 이상 지원하지 않음
            if design_name in ['design_1', 'design_2']:
                logger.warning(
                    f"[PDF 생성] '{design_name}'는 더 이상 지원하지 않습니다. "
                    f"기본 디자인으로 폴백합니다. "
                    f"템플릿 디자인(template_sample1, template_sample2)을 사용하세요."
                )
                design_name = None  # 기본 디자인으로 폴백
            
            if design_name:  # template_sample1, template_sample2만 처리
                logger.info(f"[PDF 생성] design_name 파라미터: '{design_name}'")
                try:
                    from .templates.designs.design_factory import DesignFactory
                    logger.info(f"[PDF 생성] 디자인 팩토리에서 '{design_name}' 가져오기 시도")
                    logger.info(f"[PDF 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                    
                    design = DesignFactory.get_design(design_name)
                    logger.info(f"[PDF 생성] 디자인 인스턴스: {design is not None}")
                    
                    if design:
                        logger.info(f"[PDF 생성] 디자인 '{design_name}' 사용하여 PDF 생성 시작")
                        result = design.generate_pdf(payroll_data, employee_data, output_path, period)
                        logger.info(f"[PDF 생성] 디자인 '{design_name}' 사용하여 PDF 생성 완료")
                        return result
                    else:
                        logger.warning(f"[PDF 생성] 디자인 '{design_name}'을 찾을 수 없습니다. 기본 방식 사용")
                        logger.warning(f"[PDF 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                except Exception as e:
                    logger.error(f"[PDF 생성] 디자인 '{design_name}' 생성 실패: {e}", exc_info=True)
                    logger.warning(f"[PDF 생성] 기본 방식으로 폴백")
        
        logger.info("[PDF 생성] 기본 방식으로 PDF 생성")
        
        # 기존 로직 (변경 없음, 하위 호환성 유지)
        if use_template:
            try:
                return self.generate_payslip_from_template(payroll_data, employee_data, output_path, period)
            except Exception as e:
                logger.warning(f"템플릿 기반 PDF 생성 실패, 코드 기반 생성으로 전환: {str(e)}")
                # 템플릿 실패 시 코드 기반 생성으로 폴백
                return self._generate_payslip_code_based(payroll_data, employee_data, output_path, period)
        else:
            return self._generate_payslip_code_based(payroll_data, employee_data, output_path, period)
    
    def generate_payslip_from_template(self, payroll_data, employee_data, output_path, period):
        """엑셀 템플릿을 사용하여 PDF 생성
        
        Args:
            payroll_data (dict): calculator.calculate_deductions()의 반환값
            employee_data (dict): 직원 정보
            output_path (str): 출력 PDF 파일 경로
            period (str): 급여 기간
        """
        import tempfile
        import shutil
        
        try:
            # ExcelHandler를 사용하여 엑셀 파일 생성
            try:
                from .excel_handler import ExcelHandler
            except ImportError:
                from excel_handler import ExcelHandler
            
            excel_handler = ExcelHandler()
            
            # 임시 엑셀 파일 생성
            temp_excel = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
            temp_excel_path = temp_excel.name
            temp_excel.close()
            
            # 템플릿 기반 엑셀 파일 생성
            excel_handler.write_payroll(payroll_data, temp_excel_path, employee_data, period, use_template=True)
            
            # 엑셀을 PDF로 변환 (현재는 코드 기반 PDF 생성으로 대체)
            # 향후 엑셀→PDF 변환 라이브러리 추가 시 사용 가능
            # 예: xlsx2pdf, win32com, LibreOffice 등
            logger.info("엑셀 템플릿 기반 PDF 생성: 엑셀 파일 생성 완료, PDF 변환은 코드 기반으로 수행")
            
            # 임시 엑셀 파일 삭제
            if os.path.exists(temp_excel_path):
                os.unlink(temp_excel_path)
            
            # 코드 기반 PDF 생성으로 대체 (템플릿 스타일 유지)
            return self._generate_payslip_code_based(payroll_data, employee_data, output_path, period)
            
        except Exception as e:
            logger.exception(f"템플릿 기반 PDF 생성 오류: {str(e)}")
            # 임시 파일 정리
            if 'temp_excel_path' in locals() and os.path.exists(temp_excel_path):
                try:
                    os.unlink(temp_excel_path)
                except:
                    pass
            raise
    
    def _generate_payslip_code_based(self, payroll_data, employee_data, output_path, period):
        """코드 기반 급여명세서 PDF 생성 (기존 방식)
        
        Args:
            payroll_data (dict): calculator.calculate_deductions()의 반환값
            employee_data (dict): 직원 정보 (이름, 주민번호, 입사일 등)
            output_path (str): 출력 파일 경로
            period (str): 급여 기간 (예: "2025-01")
        """
        try:
            # 파일 경로 정규화
            output_path = normalize_path(output_path)
            logger.info(f"코드 기반 PDF 생성 시작: {output_path}")
            
            # 출력 디렉토리 생성
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # PDF 캔버스 생성
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            
            # 상단 여백
            top_margin = 30*mm
            left_margin = 30*mm
            right_margin = 30*mm
            content_width = width - left_margin - right_margin
            
            # 제목 영역 (박스 처리)
            title_y = height - top_margin
            title_height = 20*mm
            # 제목 박스 배경
            c.setFillColorRGB(0.95, 0.95, 0.95)  # 연한 회색
            c.rect(left_margin, title_y - title_height, content_width, title_height, fill=1, stroke=0)
            # 제목 박스 테두리
            c.setStrokeColorRGB(0.7, 0.7, 0.7)  # 회색 테두리
            c.setLineWidth(1)
            c.rect(left_margin, title_y - title_height, content_width, title_height, fill=0, stroke=1)
            
            # 제목 텍스트
            c.setFillColorRGB(0, 0, 0)  # 검은색
            c.setFont(self.font_name, 22)
            c.drawString(left_margin + 10*mm, title_y - 15*mm, "급여명세서")
            
            # 기간 (제목 박스 내)
            c.setFont(self.font_name, 11)
            c.setFillColorRGB(0.4, 0.4, 0.4)  # 어두운 회색
            c.drawString(left_margin + 10*mm, title_y - 30*mm, f"지급기간: {period}")
            
            # 직원 정보 영역
            y_pos = title_y - title_height - 20*mm
            info_box_height = 50*mm
            # 직원 정보 박스 배경
            c.setFillColorRGB(0.98, 0.98, 0.98)  # 매우 연한 회색
            c.rect(left_margin, y_pos - info_box_height, content_width, info_box_height, fill=1, stroke=0)
            # 직원 정보 박스 테두리
            c.setStrokeColorRGB(0.8, 0.8, 0.8)
            c.rect(left_margin, y_pos - info_box_height, content_width, info_box_height, fill=0, stroke=1)
            
            # 직원 정보 텍스트
            info_y = y_pos - 10*mm
            c.setFillColorRGB(0, 0, 0)
            c.setFont(self.font_name, 11)
            c.drawString(left_margin + 10*mm, info_y, f"성명: {employee_data.get('이름', '')}")
            info_y -= 12*mm
            
            # 주민번호 마스킹 처리
            masked_rrn = mask_resident_number(employee_data.get('주민번호', ''))
            c.drawString(left_margin + 10*mm, info_y, f"주민번호: {masked_rrn}")
            info_y -= 12*mm
            
            # 입사일 표시 (있는 경우)
            if employee_data.get('입사일'):
                join_date = employee_data.get('입사일', '')
                if hasattr(join_date, 'strftime'):
                    join_date_str = join_date.strftime('%Y-%m-%d')
                else:
                    join_date_str = str(join_date)
                c.drawString(left_margin + 10*mm, info_y, f"입사일: {join_date_str}")
            
            # 지급 항목 테이블
            y_pos = y_pos - info_box_height - 20*mm
            table_x = left_margin
            table_width = content_width
            col1_width = table_width * 0.6  # 항목명 열
            col2_width = table_width * 0.4  # 금액 열
            
            # 테이블 헤더
            header_height = 8*mm
            header_y = y_pos
            # 헤더 배경
            c.setFillColorRGB(0.2, 0.4, 0.8)  # 파란색
            c.rect(table_x, header_y - header_height, table_width, header_height, fill=1, stroke=0)
            # 헤더 텍스트
            c.setFillColorRGB(1, 1, 1)  # 흰색
            c.setFont(self.font_name, 12)
            c.drawString(table_x + 5*mm, header_y - 6*mm, "지급 항목")
            c.drawString(table_x + col1_width + 5*mm, header_y - 6*mm, "금액")
            
            y_pos = header_y - header_height - 2*mm
            
            # 지급 항목 리스트 (0원인 항목은 제외, 단 기본급은 항상 표시)
            payment_items = []
            if payroll_data.get('기본급', 0) > 0:
                payment_items.append(("기본급", payroll_data.get('기본급', 0)))
            if payroll_data.get('연장근무수당', 0) > 0:
                payment_items.append(("연장근무수당", payroll_data.get('연장근무수당', 0)))
            if payroll_data.get('상여금', 0) > 0:
                payment_items.append(("상여금", payroll_data.get('상여금', 0)))
            
            # 지급 항목 표시
            row_height = 10*mm
            for item_name, amount in payment_items:
                # 행 배경 (교차 색상)
                if len(payment_items) % 2 == 0:
                    c.setFillColorRGB(0.98, 0.98, 0.98)  # 매우 연한 회색
                else:
                    c.setFillColorRGB(1, 1, 1)  # 흰색
                c.rect(table_x, y_pos - row_height, table_width, row_height, fill=1, stroke=0)
                
                # 행 테두리
                c.setStrokeColorRGB(0.9, 0.9, 0.9)
                c.setLineWidth(0.5)
                c.line(table_x, y_pos - row_height, table_x + table_width, y_pos - row_height)
                
                # 텍스트
                c.setFillColorRGB(0, 0, 0)
                c.setFont(self.font_name, 10)
                c.drawString(table_x + 5*mm, y_pos - 7*mm, item_name)
                c.drawString(table_x + col1_width + 5*mm, y_pos - 7*mm, f"{amount:,}원")
                y_pos -= row_height
            
            # 총 지급액 (강조)
            total_row_height = 12*mm
            # 총액 행 배경
            c.setFillColorRGB(0.9, 0.95, 1.0)  # 연한 파란색
            c.rect(table_x, y_pos - total_row_height, table_width, total_row_height, fill=1, stroke=0)
            # 총액 행 테두리
            c.setStrokeColorRGB(0.2, 0.4, 0.8)
            c.setLineWidth(1.5)
            c.rect(table_x, y_pos - total_row_height, table_width, total_row_height, fill=0, stroke=1)
            
            # 총액 텍스트
            c.setFillColorRGB(0, 0, 0)
            c.setFont(self.font_name, 11)
            c.drawString(table_x + 5*mm, y_pos - 9*mm, "총 지급액")
            c.setFont(self.font_name, 11)
            c.drawString(table_x + col1_width + 5*mm, y_pos - 9*mm, f"{payroll_data.get('총지급액', 0):,}원")
            y_pos -= total_row_height + 5*mm
            
            # 공제 항목 테이블
            # 테이블 헤더
            header_y = y_pos
            # 헤더 배경
            c.setFillColorRGB(0.8, 0.2, 0.2)  # 빨간색
            c.rect(table_x, header_y - header_height, table_width, header_height, fill=1, stroke=0)
            # 헤더 텍스트
            c.setFillColorRGB(1, 1, 1)  # 흰색
            c.setFont(self.font_name, 12)
            c.drawString(table_x + 5*mm, header_y - 6*mm, "공제 항목")
            c.drawString(table_x + col1_width + 5*mm, header_y - 6*mm, "금액")
            
            y_pos = header_y - header_height - 2*mm
            
            # 공제 항목 리스트
            deduction_items = [
                ("국민연금", payroll_data.get('국민연금', 0)),
                ("건강보험", payroll_data.get('건강보험', 0)),
                ("장기요양", payroll_data.get('장기요양', 0)),
                ("고용보험", payroll_data.get('고용보험', 0)),
                ("소득세", payroll_data.get('소득세', 0)),
                ("지방소득세", payroll_data.get('지방소득세', 0)),
            ]
            
            # 공제 항목 표시
            for idx, (item_name, amount) in enumerate(deduction_items):
                # 행 배경 (교차 색상)
                if idx % 2 == 0:
                    c.setFillColorRGB(0.98, 0.98, 0.98)  # 매우 연한 회색
                else:
                    c.setFillColorRGB(1, 1, 1)  # 흰색
                c.rect(table_x, y_pos - row_height, table_width, row_height, fill=1, stroke=0)
                
                # 행 테두리
                c.setStrokeColorRGB(0.9, 0.9, 0.9)
                c.setLineWidth(0.5)
                c.line(table_x, y_pos - row_height, table_x + table_width, y_pos - row_height)
                
                # 텍스트
                c.setFillColorRGB(0, 0, 0)
                c.setFont(self.font_name, 10)
                c.drawString(table_x + 5*mm, y_pos - 7*mm, item_name)
                c.drawString(table_x + col1_width + 5*mm, y_pos - 7*mm, f"{amount:,}원")
                y_pos -= row_height
            
            # 총 공제액 (강조)
            # 총액 행 배경
            c.setFillColorRGB(1.0, 0.95, 0.95)  # 연한 빨간색
            c.rect(table_x, y_pos - total_row_height, table_width, total_row_height, fill=1, stroke=0)
            # 총액 행 테두리
            c.setStrokeColorRGB(0.8, 0.2, 0.2)
            c.setLineWidth(1.5)
            c.rect(table_x, y_pos - total_row_height, table_width, total_row_height, fill=0, stroke=1)
            
            # 총액 텍스트
            c.setFillColorRGB(0, 0, 0)
            c.setFont(self.font_name, 11)
            c.drawString(table_x + 5*mm, y_pos - 9*mm, "총 공제액")
            c.setFont(self.font_name, 11)
            c.drawString(table_x + col1_width + 5*mm, y_pos - 9*mm, f"{payroll_data.get('총공제액', 0):,}원")
            y_pos -= total_row_height + 10*mm
            
            # 실수령액 강조 표시 (박스 처리)
            net_pay_box_height = 20*mm
            net_pay = payroll_data.get('실수령액', 0)
            
            # 실수령액 박스 배경
            c.setFillColorRGB(0.9, 0.95, 1.0)  # 연한 파란색
            c.rect(table_x, y_pos - net_pay_box_height, table_width, net_pay_box_height, fill=1, stroke=0)
            
            # 실수령액 박스 테두리
            c.setStrokeColorRGB(0, 0.4, 0.8)  # 파란색 테두리
            c.setLineWidth(2)
            c.rect(table_x, y_pos - net_pay_box_height, table_width, net_pay_box_height, fill=0, stroke=1)
            
            # 실수령액 텍스트
            c.setFillColorRGB(0, 0, 0.8)  # 진한 파란색
            c.setFont(self.font_name, 18)
            c.drawString(table_x + 10*mm, y_pos - 14*mm, f"실수령액: {net_pay:,}원")
            
            # 테두리 복원
            c.setLineWidth(1)
            c.setStrokeColorRGB(0, 0, 0)
            
            c.save()
            logger.info(f"PDF 생성 완료: {output_path}")
            
        except Exception as e:
            logger.exception(f"PDF 생성 오류: {str(e)}")
            raise ValueError(f"PDF 생성 오류: {str(e)}")
    
    def _draw_table_header(self, c, x, y, title):
        """테이블 헤더 그리기 (레거시 메서드 - 현재 사용되지 않음)
        
        Note: 이 메서드는 이전 버전에서 사용되었으나, 
        현재는 인라인으로 헤더를 그리도록 변경되었습니다.
        향후 호환성을 위해 유지됩니다.
        
        Args:
            c: Canvas 객체
            x: X 좌표 (mm 단위)
            y: Y 좌표 (mm 단위)
            title: 헤더 제목
        """
        # 레거시 메서드 - 현재 사용되지 않음
        pass

