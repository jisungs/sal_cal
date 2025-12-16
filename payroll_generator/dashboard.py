# dashboard.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from .calculator import PayrollCalculator
    from .logger import setup_logger
except ImportError:
    from calculator import PayrollCalculator
    from logger import setup_logger

logger = setup_logger()

class Dashboard:
    def __init__(self):
        self.calculator = PayrollCalculator()
    
    def analyze_employee_data(self, df):
        """직원 데이터 분석 및 대시보드 데이터 생성"""
        try:
            total_employees = len(df)
            
            # 급여 계산
            total_payment = 0
            total_deduction = 0
            total_net_pay = 0
            
            payroll_summary = []
            for idx, row in df.iterrows():
                payroll_data = self.calculator.calculate_deductions(row.to_dict())
                total_payment += payroll_data['총지급액']
                total_deduction += payroll_data['총공제액']
                total_net_pay += payroll_data['실수령액']
                
                payroll_summary.append({
                    '이름': row.get('이름', f'직원{idx+1}'),
                    '총지급액': payroll_data['총지급액'],
                    '실수령액': payroll_data['실수령액']
                })
            
            # 근무현황 분석
            work_status = self._analyze_work_status(df)
            
            # 특이사항 분석
            special_notes = self._analyze_special_notes(df)
            
            # 월별 근무자 수 데이터 생성 (임시 - 향후 실제 월별 데이터로 대체)
            monthly_data = self._generate_monthly_data(df, work_status)
            
            return {
                'total_employees': total_employees,
                'total_payment': total_payment,
                'total_deduction': total_deduction,
                'total_net_pay': total_net_pay,
                'payroll_summary': payroll_summary,
                'work_status': work_status,
                'special_notes': special_notes,
                'monthly_data': monthly_data
            }
        except Exception as e:
            logger.exception(f"대시보드 데이터 분석 오류: {str(e)}")
            raise
    
    def _analyze_work_status(self, df):
        """근무현황 분석"""
        from datetime import datetime, timedelta
        
        regular = 0
        contract = 0
        new = 0
        
        # 입사일 기준으로 분석
        today = datetime.now()
        three_months_ago = today - timedelta(days=90)
        
        for idx, row in df.iterrows():
            join_date_str = row.get('입사일', '')
            if not join_date_str:
                regular += 1
                continue
            
            try:
                # 날짜 형식 변환
                if isinstance(join_date_str, str):
                    join_date = datetime.strptime(join_date_str, '%Y-%m-%d')
                else:
                    join_date = join_date_str
                
                # 3개월 이내 입사자는 신입
                if join_date >= three_months_ago:
                    new += 1
                else:
                    # 임시로 정규직으로 분류 (향후 계약직 구분 로직 추가 가능)
                    regular += 1
            except:
                regular += 1
        
        return {
            'regular': regular,
            'contract': contract,
            'new': new
        }
    
    def _generate_monthly_data(self, df, work_status):
        """월별 급여 지출 현황 데이터 생성"""
        try:
            from .history_manager import HistoryManager
        except ImportError:
            from history_manager import HistoryManager
        
        try:
            history_manager = HistoryManager()
            
            # 최근 12개월 이력 데이터 로드 시도
            history_data = history_manager.get_latest_12_months()
            
            if history_data and len(history_data) > 0:
                # 실제 이력 데이터 사용 (없는 월은 0으로 표시)
                logger.info(f"실제 이력 데이터 사용: {len(history_data)}개월")
                return self._format_history_data(history_data)
            else:
                # 이력 데이터가 없으면 모두 0으로 표시
                logger.info("이력 데이터 없음, 빈 데이터(0) 사용")
                return self._generate_empty_data()
        except Exception as e:
            logger.warning(f"이력 데이터 로드 실패: {e}. 빈 데이터(0) 사용")
            return self._generate_empty_data()
    
    def _format_history_data(self, history_data):
        """이력 데이터를 그래프 형식으로 변환 (최근 12개월 기준, 없는 월은 0)"""
        from datetime import datetime
        
        # 현재 날짜 기준으로 최근 12개월 목록 생성
        today = datetime.now()
        current_month = today.month
        current_year = today.year
        
        # 이력 데이터를 딕셔너리로 변환 (년월을 키로)
        history_dict = {row['년월']: row for row in history_data}
        
        months = []
        regular_payments = []
        contract_payments = []
        
        # 최근 12개월 데이터 생성 (역순: 현재 월이 첫 번째)
        for i in range(12):
            # 월 계산
            month_offset = i
            target_month = current_month - month_offset
            target_year = current_year
            
            # 연도 조정
            while target_month <= 0:
                target_month += 12
                target_year -= 1
            
            year_month = f"{target_year}-{target_month:02d}"
            month_label = f"{target_month}월"
            
            months.append(month_label)
            
            # 이력 데이터가 있으면 사용, 없으면 0
            if year_month in history_dict:
                regular_payments.append(int(history_dict[year_month]['정규직_급여']))
                contract_payments.append(int(history_dict[year_month]['계약직_급여']))
            else:
                regular_payments.append(0)
                contract_payments.append(0)
        
        return {
            'months': months,
            'regular': regular_payments,
            'contract': contract_payments
        }
    
    def _generate_empty_data(self):
        """이력 데이터가 없을 때 빈 데이터 생성 (모두 0)"""
        from datetime import datetime
        
        today = datetime.now()
        current_month = today.month
        current_year = today.year
        
        months = []
        regular_payments = []
        contract_payments = []
        
        # 최근 12개월 데이터 생성 (모두 0)
        for i in range(12):
            month_offset = i
            target_month = current_month - month_offset
            target_year = current_year
            
            while target_month <= 0:
                target_month += 12
                target_year -= 1
            
            months.append(f"{target_month}월")
            regular_payments.append(0)
            contract_payments.append(0)
        
        return {
            'months': months,
            'regular': regular_payments,
            'contract': contract_payments
        }
    
    def _analyze_special_notes(self, df):
        """특이사항 분석"""
        notes = []
        
        # 연장근무 있는 직원 수
        overtime_count = 0
        for idx, row in df.iterrows():
            overtime_hours = row.get('연장근무시간', 0)
            if pd.notna(overtime_hours) and overtime_hours > 0:
                overtime_count += 1
        
        if overtime_count > 0:
            notes.append(f"이번 달 연장근무: {overtime_count}명")
        
        # 상여금 지급 직원 수
        bonus_count = 0
        for idx, row in df.iterrows():
            bonus = row.get('상여금', 0)
            if pd.notna(bonus) and bonus > 0:
                bonus_count += 1
        
        if bonus_count > 0:
            notes.append(f"상여금 지급: {bonus_count}명")
        
        # 신규 입사자 수
        from datetime import datetime, timedelta
        today = datetime.now()
        three_months_ago = today - timedelta(days=90)
        
        new_employee_count = 0
        for idx, row in df.iterrows():
            join_date_str = row.get('입사일', '')
            if join_date_str:
                try:
                    if isinstance(join_date_str, str):
                        join_date = datetime.strptime(join_date_str, '%Y-%m-%d')
                    else:
                        join_date = join_date_str
                    
                    if join_date >= three_months_ago:
                        new_employee_count += 1
                except:
                    pass
        
        if new_employee_count > 0:
            notes.append(f"신규 입사: {new_employee_count}명")
        
        return notes
    
    def create_monthly_workforce_chart(self, monthly_data, figsize=None):
        """월별 급여 지출 현황 클러스터 막대 그래프 생성"""
        try:
            # 한글 폰트 설정
            plt.rcParams['font.family'] = 'AppleGothic'  # macOS
            plt.rcParams['axes.unicode_minus'] = False
            
            # 그래프 크기 설정 (기본값 또는 전달된 값)
            if figsize is None:
                figsize = (5, 2.5)
            fig, ax = plt.subplots(figsize=figsize, dpi=100)
            
            months = monthly_data['months']
            regular = monthly_data['regular']
            contract = monthly_data['contract']
            
            x = range(len(months))
            width = 0.35  # 막대 너비
            
            # 클러스터 막대 그래프 생성 (모던 색상)
            bars1 = ax.bar([i - width/2 for i in x], regular, width, 
                          label='정규직', color='#2196F3', edgecolor='#1565C0', linewidth=1.5)
            bars2 = ax.bar([i + width/2 for i in x], contract, width,
                          label='계약', color='#FF6B35', edgecolor='#E55A2B', linewidth=1.5)
            
            # X축 설정
            ax.set_xlabel('월', fontsize=9, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(months, fontsize=8)
            
            # Y축 설정 (급여 지출 금액)
            max_payment = max(max(regular), max(contract)) if regular and contract else 1000000
            # 100만원 단위로 올림
            y_max = ((max_payment // 1000000) + 1) * 1000000
            ax.set_ylabel('급여 지출 (원)', fontsize=9, fontweight='bold')
            ax.set_ylim(0, max(y_max, 1000000))
            
            # Y축 눈금을 5개 구간으로 나누어 설정
            num_ticks = 5
            tick_interval = max(1000000, int(y_max) // num_ticks)
            # 100만원 단위로 정렬
            tick_interval = ((tick_interval // 1000000) + 1) * 1000000
            
            y_ticks = [i * tick_interval for i in range(num_ticks + 1) if i * tick_interval <= y_max]
            if y_max not in y_ticks:
                y_ticks.append(y_max)
            
            ax.set_yticks(y_ticks)
            # Y축 레이블을 만원 단위로 표시
            ax.set_yticklabels([f'{int(tick/10000)}만' for tick in y_ticks], fontsize=8)
            
            # 제목
            ax.set_title('월별 급여 지출 현황', fontsize=11, fontweight='bold', pad=10)
            
            # 범례
            ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
            
            # 그리드
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)
            
            # 값 표시 (선택적)
            # for bars in [bars1, bars2]:
            #     for bar in bars:
            #         height = bar.get_height()
            #         ax.text(bar.get_x() + bar.get_width()/2., height,
            #                f'{int(height)}', ha='center', va='bottom', fontsize=8)
            
            # tight_layout으로 자동 조정 (반응형 대응)
            plt.tight_layout(pad=1.0)
            return fig
        except Exception as e:
            logger.exception(f"월별 근무자 그래프 생성 오류: {str(e)}")
            raise
    
    def create_salary_chart(self, payroll_summary):
        """월급여 정산현황 막대 그래프 생성 (레거시 - 호환성 유지)"""
        try:
            # 한글 폰트 설정
            plt.rcParams['font.family'] = 'AppleGothic'  # macOS
            plt.rcParams['axes.unicode_minus'] = False
            
            fig, ax = plt.subplots(figsize=(8, 4))
            
            names = [item['이름'] for item in payroll_summary]
            salaries = [item['실수령액'] for item in payroll_summary]
            
            bars = ax.barh(names, salaries, color='#304FFE')
            ax.set_xlabel('실수령액 (원)', fontsize=10)
            ax.set_ylabel('직원', fontsize=10)
            ax.set_title('월급여 정산현황', fontsize=12, fontweight='bold')
            
            # 값 표시
            for i, (bar, v) in enumerate(zip(bars, salaries)):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, 
                       f'{v:,}원', ha='left', va='center', fontsize=8)
            
            plt.tight_layout()
            return fig
        except Exception as e:
            logger.exception(f"급여 그래프 생성 오류: {str(e)}")
            raise
    
    def create_workforce_chart(self, work_status):
        """근무자구성 도넛 그래프 생성"""
        try:
            # 한글 폰트 설정
            plt.rcParams['font.family'] = 'AppleGothic'  # macOS
            plt.rcParams['axes.unicode_minus'] = False
            
            fig, ax = plt.subplots(figsize=(6, 6))
            
            labels = []
            sizes = []
            colors_list = []
            
            # 디자인에 맞는 색상 매핑
            color_map = {
                'regular': '#E3F2FD',  # 연한 파란색
                'contract': '#64B5F6',  # 중간 파란색
                'new': '#1976D2'        # 진한 파란색
            }
            
            if work_status.get('regular', 0) > 0:
                labels.append('정규')
                sizes.append(work_status['regular'])
                colors_list.append(color_map['regular'])
            
            if work_status.get('contract', 0) > 0:
                labels.append('계약')
                sizes.append(work_status['contract'])
                colors_list.append(color_map['contract'])
            
            if work_status.get('new', 0) > 0:
                labels.append('신입')
                sizes.append(work_status['new'])
                colors_list.append(color_map['new'])
            
            if not sizes:
                # 데이터가 없을 경우
                ax.text(0.5, 0.5, '데이터 없음', 
                       ha='center', va='center', fontsize=12)
                ax.set_title('근무자구성', fontsize=12, fontweight='bold')
                plt.tight_layout()
                return fig
            
            # 도넛 그래프 생성 (wedgeprops로 중앙 구멍 만들기)
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                autopct='%1.1f%%',
                startangle=90,
                colors=colors_list,
                wedgeprops=dict(width=0.5),  # 도넛 모양
                textprops={'fontsize': 10}
            )
            
            ax.set_title('근무자구성', fontsize=12, fontweight='bold', pad=20)
            
            plt.tight_layout()
            return fig
        except Exception as e:
            logger.exception(f"근무자구성 그래프 생성 오류: {str(e)}")
            raise

