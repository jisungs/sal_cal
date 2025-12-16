# design_factory.py
import logging

logger = logging.getLogger(__name__)

# 디자인 클래스 import (순환 참조 방지를 위해 지연 import)
# design_1, design_2는 더 이상 사용하지 않음 (YAML 기반 디자인 삭제됨)

try:
    from .template_sample1 import TemplateSample1
except ImportError:
    try:
        from payroll_generator.templates.designs.template_sample1 import TemplateSample1
    except ImportError:
        TemplateSample1 = None

try:
    from .template_sample2 import TemplateSample2
except ImportError:
    try:
        from payroll_generator.templates.designs.template_sample2 import TemplateSample2
    except ImportError:
        TemplateSample2 = None

class DesignFactory:
    """디자인 팩토리 클래스"""
    
    _designs = {
        'default': None,  # 기존 방식
        # 'design_1': Design1,  # 삭제됨 (YAML 기반 디자인 더 이상 사용 안 함)
        # 'design_2': Design2,  # 삭제됨 (YAML 기반 디자인 더 이상 사용 안 함)
        'template_sample1': TemplateSample1,  # 템플릿 샘플 1
        'template_sample2': TemplateSample2,  # 템플릿 샘플 2
    }
    
    _instances = {}  # 싱글톤 인스턴스 캐시
    
    @classmethod
    def get_design(cls, design_name='default'):
        """디자인 인스턴스 반환
        
        Args:
            design_name: 디자인 이름 ('default', 'template_sample1', 'template_sample2')
                - 'default': 기본 디자인 (None 반환)
                - 'template_sample1': 급여명세서 템플릿
                - 'template_sample2': 임금명세서 템플릿
                - 'design_1', 'design_2': 더 이상 지원하지 않음 (폴백 처리)
            
        Returns:
            디자인 인스턴스 또는 None (기본 방식 사용)
        """
        if design_name == 'default' or design_name is None:
            return None
        
        # design_1, design_2는 더 이상 지원하지 않음
        if design_name in ['design_1', 'design_2']:
            logger.warning(
                f"디자인 '{design_name}'는 더 이상 지원하지 않습니다. "
                f"기본 디자인으로 폴백합니다. "
                f"템플릿 디자인(template_sample1, template_sample2)을 사용하세요."
            )
            return None
        
        if design_name not in cls._designs:
            logger.warning(f"알 수 없는 디자인: {design_name}, 기본 방식 사용")
            return None
        
        design_class = cls._designs.get(design_name)
        if design_class is None:
            logger.warning(f"디자인 클래스가 None입니다: {design_name}. Import 실패 가능성.")
            logger.warning(f"사용 가능한 디자인: {cls.list_available_designs()}")
            logger.warning(f"_designs 상태: {[(k, v is not None) for k, v in cls._designs.items()]}")
            return None
        
        # 싱글톤 패턴으로 인스턴스 재사용
        if design_name not in cls._instances:
            try:
                logger.debug(f"디자인 인스턴스 생성 시도: {design_name}, 클래스: {design_class}")
                cls._instances[design_name] = design_class()
                logger.info(f"디자인 인스턴스 생성 완료: {design_name}")
            except Exception as e:
                logger.error(f"디자인 생성 실패: {design_name}, {e}", exc_info=True)
                return None
        
        return cls._instances[design_name]
    
    @classmethod
    def list_available_designs(cls):
        """사용 가능한 디자인 목록 반환
        
        Returns:
            디자인 이름 리스트
        """
        return [name for name, design_class in cls._designs.items() 
                if design_class is not None]
    
    @classmethod
    def register_design(cls, name, design_class):
        """새 디자인 등록 (확장용)
        
        Args:
            name: 디자인 이름
            design_class: 디자인 클래스
        """
        cls._designs[name] = design_class
        # 기존 인스턴스 캐시 초기화 (새 디자인 등록 시)
        if name in cls._instances:
            del cls._instances[name]
        logger.info(f"디자인 등록 완료: {name}")
    
    @classmethod
    def is_design_available(cls, design_name):
        """디자인 사용 가능 여부 확인
        
        Args:
            design_name: 디자인 이름
            
        Returns:
            bool: 사용 가능 여부
        """
        return design_name in cls._designs and cls._designs[design_name] is not None
