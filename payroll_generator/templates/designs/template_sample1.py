# template_sample1.py
from .template_design import TemplateDesign
import logging

logger = logging.getLogger(__name__)

class TemplateSample1(TemplateDesign):
    """템플릿 샘플 1: 급여명세서_template.xlsx"""
    
    def __init__(self):
        super().__init__(
            template_filename='template_sample1.xlsx',
            mapping_filename='template_sample1_mapping.json'
        )
        logger.info("TemplateSample1 인스턴스 생성 완료")
