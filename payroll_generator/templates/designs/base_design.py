# base_design.py
from abc import ABC, abstractmethod
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    yaml = None
from pathlib import Path
import os

class BaseDesign(ABC):
    """디자인 템플릿 기본 클래스"""
    
    def __init__(self, config_path=None):
        """초기화"""
        if config_path:
            self.config = self._load_config(config_path)
        else:
            self.config = {}
        self.font_name = self._get_font_name()
    
    def _load_config(self, config_path):
        """YAML 설정 파일 로드"""
        # YAML이 없으면 빈 딕셔너리 반환 (템플릿 디자인은 YAML 불필요)
        if not HAS_YAML:
            return {}
        
        # 여러 경로 시도
        paths_to_try = []
        
        # 1. resource_path를 사용한 경로 (PyInstaller 환경)
        try:
            from ..utils import resource_path
            paths_to_try.append(resource_path(f'templates/designs/configs/{Path(config_path).name}'))
        except ImportError:
            try:
                from payroll_generator.utils import resource_path
                paths_to_try.append(resource_path(f'templates/designs/configs/{Path(config_path).name}'))
            except ImportError:
                pass
        
        # 2. 상대 경로 (개발 환경)
        paths_to_try.append(os.path.join(
            os.path.dirname(__file__), 'configs', Path(config_path).name
        ))
        
        # 3. 절대 경로 (config_path가 절대 경로인 경우)
        if os.path.isabs(config_path):
            paths_to_try.append(config_path)
        
        # 경로 찾기
        for path in paths_to_try:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        if yaml is None:
                            # YAML이 없으면 빈 딕셔너리 반환
                            return {}
                        config = yaml.safe_load(f)
                        if config:
                            return config
                except Exception as e:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"설정 파일 로드 실패 ({path}): {e}")
                    continue
        
        # 설정 파일을 찾을 수 없는 경우
        raise FileNotFoundError(
            f"설정 파일을 찾을 수 없습니다: {config_path}. "
            f"다음 경로를 시도했습니다: {paths_to_try}"
        )
    
    def _get_font_name(self):
        """사용 가능한 한글 폰트 이름 반환"""
        # 기존 PDFGenerator와 동일한 로직
        # 실제로는 PDFGenerator에서 폰트가 등록되어 있어야 함
        return 'NanumGothic'  # 또는 'Helvetica' (폴백)
    
    @abstractmethod
    def generate_pdf(self, payroll_data, employee_data, output_path, period):
        """PDF 생성 - 하위 클래스에서 구현"""
        pass
    
    @abstractmethod
    def generate_excel(self, payroll_data, employee_data, output_path, period):
        """엑셀 생성 - 하위 클래스에서 구현"""
        pass
    
    def format_currency(self, amount):
        """통화 포맷팅"""
        if amount is None:
            return "0원"
        return f"{int(amount):,}원"
    
    def mask_resident_number(self, rrn):
        """주민번호 마스킹"""
        try:
            from ..utils import mask_resident_number as mask_rrn
        except ImportError:
            try:
                from payroll_generator.utils import mask_resident_number as mask_rrn
            except ImportError:
                from utils import mask_resident_number as mask_rrn
        return mask_rrn(rrn)
    
    def get_config_value(self, *keys, default=None):
        """설정 값 가져오기 (중첩된 키 지원)
        
        Args:
            *keys: 중첩된 키 경로 (예: 'fonts', 'title', 'size')
            default: 기본값
            
        Returns:
            설정 값 또는 기본값
        """
        value = self.config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            if value is None:
                return default
        return value