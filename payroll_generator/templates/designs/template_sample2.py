# template_sample2.py
from .template_design import TemplateDesign
import logging

logger = logging.getLogger(__name__)

class TemplateSample2(TemplateDesign):
    """템플릿 샘플 2: 임금명세서양식_template3.xlsx"""
    
    def __init__(self):
        super().__init__(
            template_filename='template_sample2.xlsx',
            mapping_filename='template_sample2_mapping.json'
        )
        logger.info("TemplateSample2 인스턴스 생성 완료")
