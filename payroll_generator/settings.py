# settings.py
"""설정 파일 관리 모듈"""

import json
import os
from pathlib import Path

try:
    from .logger import setup_logger
except ImportError:
    from logger import setup_logger

logger = setup_logger()

class SettingsManager:
    """설정 파일 관리 클래스"""
    
    def __init__(self):
        """설정 관리자 초기화"""
        # 설정 파일 경로
        # PyInstaller 환경에서는 사용자 홈 디렉토리에 설정 저장
        import sys
        try:
            if getattr(sys, 'frozen', False):
                # PyInstaller로 빌드된 실행 파일
                settings_dir = Path(os.path.expanduser('~')) / '.급여명세서생성기' / 'data'
            else:
                # 개발 환경
                settings_dir = Path(__file__).parent / 'data'
        except:
            # 오류 발생 시 홈 디렉토리 사용
            settings_dir = Path(os.path.expanduser('~')) / '.급여명세서생성기' / 'data'
        
        settings_dir.mkdir(parents=True, exist_ok=True)
        self.settings_file = settings_dir / 'settings.json'
        
        # 기본 설정
        self.default_settings = {
            'last_employee_file': '',
            'last_output_folder': './payroll_generator/output',
            'last_period': '2025-01',
            'last_output_format': 'both',
            'last_design_name': 'default',
            'is_first_run': True
        }
        
        # 설정 로드
        self.settings = self.load_settings()
    
    def load_settings(self):
        """설정 파일 로드"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # 기본값과 병합 (새로운 키 추가 대응)
                    merged = self.default_settings.copy()
                    merged.update(settings)
                    return merged
            else:
                return self.default_settings.copy()
        except json.JSONDecodeError as e:
            logger.warning(f"설정 파일 JSON 파싱 오류: {e}. 기본값 사용")
            return self.default_settings.copy()
        except Exception as e:
            logger.warning(f"설정 파일 로드 오류: {e}. 기본값 사용")
            return self.default_settings.copy()
    
    def save_settings(self):
        """설정 파일 저장"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            logger.info(f"설정 파일 저장 완료: {self.settings_file}")
        except PermissionError as e:
            logger.error(f"설정 파일 저장 권한 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"설정 파일 저장 오류: {e}")
            raise
    
    def get_last_employee_file(self):
        """마지막으로 사용한 직원 파일 경로 반환"""
        file_path = self.settings.get('last_employee_file', '')
        if file_path:
            # 절대 경로로 변환
            return os.path.abspath(os.path.normpath(file_path))
        return ''
    
    def set_last_employee_file(self, file_path):
        """마지막으로 사용한 직원 파일 경로 저장"""
        if file_path:
            # 절대 경로로 변환하여 저장
            abs_path = os.path.abspath(os.path.normpath(file_path))
            self.settings['last_employee_file'] = abs_path
            self.save_settings()
            logger.info(f"직원 파일 경로 저장: {abs_path}")
        else:
            self.settings['last_employee_file'] = ''
            self.save_settings()
    
    def is_first_run(self):
        """첫 실행 여부 확인"""
        return self.settings.get('is_first_run', True)
    
    def set_first_run_complete(self):
        """첫 실행 완료 표시"""
        self.settings['is_first_run'] = False
        self.save_settings()
        logger.info("첫 실행 완료 표시")
    
    def get_last_output_folder(self):
        """마지막으로 사용한 출력 폴더 경로 반환"""
        return self.settings.get('last_output_folder', './payroll_generator/output')
    
    def set_last_output_folder(self, folder_path):
        """마지막으로 사용한 출력 폴더 경로 저장"""
        if folder_path:
            # 절대 경로로 변환하여 저장
            abs_path = os.path.abspath(os.path.normpath(folder_path))
            self.settings['last_output_folder'] = abs_path
            self.save_settings()
            logger.info(f"출력 폴더 경로 저장: {abs_path}")
        else:
            self.settings['last_output_folder'] = './payroll_generator/output'
            self.save_settings()
    
    def get_last_period(self):
        """마지막으로 사용한 기간 반환"""
        return self.settings.get('last_period', '2025-01')
    
    def set_last_period(self, period):
        """마지막으로 사용한 기간 저장"""
        self.settings['last_period'] = period
        self.save_settings()
    
    def get_last_output_format(self):
        """마지막으로 사용한 출력 형식 반환"""
        return self.settings.get('last_output_format', 'both')
    
    def set_last_output_format(self, output_format):
        """마지막으로 사용한 출력 형식 저장"""
        self.settings['last_output_format'] = output_format
        self.save_settings()
    
    def get_last_design_name(self):
        """마지막으로 사용한 디자인 이름 반환"""
        return self.settings.get('last_design_name', 'default')
    
    def set_last_design_name(self, design_name):
        """마지막으로 사용한 디자인 이름 저장"""
        self.settings['last_design_name'] = design_name
        self.save_settings()

