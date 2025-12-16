# utils.py
import os
import re
import sys

def resource_path(relative_path):
    """PyInstaller로 빌드된 실행 파일에서 리소스 경로를 올바르게 반환
    
    Args:
        relative_path: 리소스 파일의 상대 경로
        
    Returns:
        리소스 파일의 절대 경로
    """
    try:
        # PyInstaller로 빌드된 실행 파일인지 확인
        base_path = sys._MEIPASS
    except Exception:
        # 개발 환경에서는 현재 파일의 디렉토리 기준
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)

def mask_resident_number(resident_number):
    """주민번호 마스킹 처리 (앞 6자리만 표시, 나머지 마스킹)"""
    if not resident_number:
        return ""
    
    # 숫자만 추출
    numbers = re.sub(r'[^0-9]', '', str(resident_number))
    
    if len(numbers) >= 7:
        return f"{numbers[:6]}-*******"
    elif len(numbers) == 6:
        return f"{numbers}-*******"
    else:
        return "*******"

def normalize_path(file_path):
    """파일 경로 정규화 및 검증"""
    if not file_path:
        raise ValueError("파일 경로가 비어있습니다.")
    
    # 절대 경로로 변환
    abs_path = os.path.abspath(file_path)
    
    # 경로 정규화
    normalized = os.path.normpath(abs_path)
    
    # 경로 검증 (상위 디렉토리 접근 방지)
    if '..' in normalized:
        raise ValueError("잘못된 파일 경로입니다.")
    
    return normalized

def validate_file_path(file_path, allowed_extensions=None):
    """파일 경로 유효성 검증"""
    normalized = normalize_path(file_path)
    
    if not os.path.exists(normalized):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {normalized}")
    
    if allowed_extensions:
        ext = os.path.splitext(normalized)[1].lower()
        if ext not in allowed_extensions:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {ext}")
    
    return normalized

