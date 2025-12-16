# logger.py
import logging
import os
import sys

def setup_logger():
    """로깅 시스템 초기화"""
    # PyInstaller 환경에서는 사용자 홈 디렉토리에 로그 저장
    try:
        if getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 실행 파일
            log_dir = os.path.join(os.path.expanduser('~'), '.급여명세서생성기', 'logs')
        else:
            # 개발 환경
            log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    except:
        # 오류 발생 시 홈 디렉토리 사용
        log_dir = os.path.join(os.path.expanduser('~'), '.급여명세서생성기', 'logs')
    
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'app.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

