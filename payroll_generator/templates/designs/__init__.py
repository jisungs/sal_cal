# designs 패키지 초기화 파일
# Import 실패 시에도 다른 클래스가 Import 가능하도록 try-except 사용
try:
    from .base_design import BaseDesign
except ImportError as e:
    # BaseDesign Import 실패 시 (예: yaml 모듈 없음)
    # 템플릿 디자인은 BaseDesign을 사용하지만, design_factory에서 이미 처리함
    BaseDesign = None

try:
    from .design_factory import DesignFactory
except ImportError as e:
    DesignFactory = None

__all__ = ['BaseDesign', 'DesignFactory']
