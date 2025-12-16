# history_manager.py
import pandas as pd
from pathlib import Path
from datetime import datetime
import os
import sys
try:
    from .logger import setup_logger
except ImportError:
    from logger import setup_logger

logger = setup_logger()

class HistoryManager:
    """월별 급여 이력 데이터 관리자"""
    
    def __init__(self):
        """월별 급여 이력 데이터 관리자 초기화"""
        # 이력 파일 경로
        # PyInstaller 환경에서는 사용자 홈 디렉토리에 이력 저장
        try:
            if getattr(sys, 'frozen', False):
                # PyInstaller로 빌드된 실행 파일
                data_dir = Path(os.path.expanduser('~')) / '.급여명세서생성기' / 'data'
            else:
                # 개발 환경
                data_dir = Path(__file__).parent / 'data'
        except:
            # 오류 발생 시 홈 디렉토리 사용
            data_dir = Path(os.path.expanduser('~')) / '.급여명세서생성기' / 'data'
        
        data_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = data_dir / 'monthly_payroll_history.xlsx'
        
        # 파일 존재 확인 및 생성
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """이력 파일 존재 확인 및 생성"""
        if not self.history_file.exists():
            self._create_empty_history_file()
    
    def _create_empty_history_file(self):
        """빈 이력 파일 생성"""
        try:
            df = pd.DataFrame(columns=[
                '년월', '정규직_급여', '계약직_급여', '총_급여',
                '정규직_인원', '계약직_인원', '총_인원', '생성일시'
            ])
            df.to_excel(self.history_file, index=False, sheet_name='월별_이력', engine='openpyxl')
            logger.info(f"이력 파일 생성: {self.history_file}")
        except Exception as e:
            logger.error(f"이력 파일 생성 실패: {e}")
            raise
    
    def save_monthly_data(self, year_month, data):
        """
        월별 급여 이력 데이터 저장
        
        Args:
            year_month: 'YYYY-MM' 형식의 년월 문자열
            data: {
                'regular_payment': 정규직 급여 합계,
                'contract_payment': 계약직 급여 합계,
                'regular_count': 정규직 인원 수,
                'contract_count': 계약직 인원 수
            }
        """
        try:
            # 데이터 검증
            self._validate_data(data)
            
            # 기존 데이터 로드
            if self.history_file.exists():
                try:
                    df = pd.read_excel(self.history_file, sheet_name='월별_이력', engine='openpyxl')
                except Exception as e:
                    logger.warning(f"기존 이력 파일 읽기 실패, 새로 생성: {e}")
                    df = pd.DataFrame(columns=[
                        '년월', '정규직_급여', '계약직_급여', '총_급여',
                        '정규직_인원', '계약직_인원', '총_인원', '생성일시'
                    ])
            else:
                df = pd.DataFrame(columns=[
                    '년월', '정규직_급여', '계약직_급여', '총_급여',
                    '정규직_인원', '계약직_인원', '총_인원', '생성일시'
                ])
            
            # 총 급여 및 총 인원 계산
            total_payment = data.get('regular_payment', 0) + data.get('contract_payment', 0)
            total_count = data.get('regular_count', 0) + data.get('contract_count', 0)
            
            # 생성일시
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 새 데이터 행
            new_row = {
                '년월': year_month,
                '정규직_급여': int(data.get('regular_payment', 0)),
                '계약직_급여': int(data.get('contract_payment', 0)),
                '총_급여': int(total_payment),
                '정규직_인원': int(data.get('regular_count', 0)),
                '계약직_인원': int(data.get('contract_count', 0)),
                '총_인원': int(total_count),
                '생성일시': created_at
            }
            
            # 해당 년월 데이터가 있는지 확인
            if '년월' in df.columns and year_month in df['년월'].values:
                # 업데이트: 해당 년월 행 찾아서 업데이트
                df.loc[df['년월'] == year_month, '정규직_급여'] = new_row['정규직_급여']
                df.loc[df['년월'] == year_month, '계약직_급여'] = new_row['계약직_급여']
                df.loc[df['년월'] == year_month, '총_급여'] = new_row['총_급여']
                df.loc[df['년월'] == year_month, '정규직_인원'] = new_row['정규직_인원']
                df.loc[df['년월'] == year_month, '계약직_인원'] = new_row['계약직_인원']
                df.loc[df['년월'] == year_month, '총_인원'] = new_row['총_인원']
                df.loc[df['년월'] == year_month, '생성일시'] = new_row['생성일시']
                logger.info(f"이력 데이터 업데이트: {year_month}")
            else:
                # 추가: 새 행 추가
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                logger.info(f"이력 데이터 추가: {year_month}")
            
            # 년월 기준으로 정렬 (오래된 것부터)
            df = df.sort_values('년월', ascending=True)
            
            # 파일 저장
            df.to_excel(self.history_file, index=False, sheet_name='월별_이력', engine='openpyxl')
            logger.info(f"이력 데이터 저장 완료: {year_month}")
            
        except Exception as e:
            logger.error(f"이력 데이터 저장 실패: {year_month} - {e}")
            raise
    
    def load_monthly_data(self, start_month=None, end_month=None):
        """
        월별 데이터 로드
        
        Args:
            start_month: 시작 년월 (YYYY-MM 형식, None이면 전체)
            end_month: 종료 년월 (YYYY-MM 형식, None이면 전체)
        
        Returns:
            리스트 형태의 데이터 (딕셔너리 리스트)
        """
        try:
            if not self.history_file.exists():
                logger.warning("이력 파일이 없습니다.")
                return []
            
            df = pd.read_excel(self.history_file, sheet_name='월별_이력', engine='openpyxl')
            
            if df.empty:
                return []
            
            # 년월 필터링
            if start_month:
                df = df[df['년월'] >= start_month]
            if end_month:
                df = df[df['년월'] <= end_month]
            
            # 딕셔너리 리스트로 변환
            return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"이력 데이터 로드 실패: {e}")
            return []
    
    def get_latest_12_months(self):
        """
        최근 12개월 데이터 로드
        
        Returns:
            리스트 형태의 데이터 (딕셔너리 리스트)
        """
        try:
            if not self.history_file.exists():
                return []
            
            df = pd.read_excel(self.history_file, sheet_name='월별_이력', engine='openpyxl')
            
            if df.empty:
                return []
            
            # 년월 기준으로 정렬 (최신순)
            df = df.sort_values('년월', ascending=False)
            
            # 최근 12개월만 선택
            latest_12 = df.head(12)
            
            # 딕셔너리 리스트로 변환
            return latest_12.to_dict('records')
            
        except Exception as e:
            logger.error(f"최근 12개월 데이터 로드 실패: {e}")
            return []
    
    def _validate_data(self, data):
        """데이터 유효성 검증"""
        required_fields = ['regular_payment', 'contract_payment', 'regular_count', 'contract_count']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"필수 필드가 없습니다: {field}")
        
        # 데이터 타입 확인
        for field in required_fields:
            value = data[field]
            if not isinstance(value, (int, float)):
                raise ValueError(f"필드 타입 오류: {field}는 숫자여야 합니다")
            if value < 0:
                raise ValueError(f"필드 값 오류: {field}는 0 이상이어야 합니다")

