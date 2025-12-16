#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""템플릿 경로 테스트"""

import unittest
import os
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from payroll_generator.templates.designs.template_sample1 import TemplateSample1
from payroll_generator.templates.designs.template_sample2 import TemplateSample2


class TestTemplatePath(unittest.TestCase):
    """템플릿 경로 테스트"""
    
    def setUp(self):
        """테스트 전 설정"""
        self.project_root = Path(__file__).parent.parent
        self.sample_dir = self.project_root / 'sample'
    
    def test_template_sample1_path(self):
        """TemplateSample1 경로 테스트"""
        design = TemplateSample1()
        template_path = design._get_template_path()
        
        # 경로가 존재하는지 확인
        self.assertTrue(os.path.exists(template_path), f"템플릿 파일이 존재하지 않습니다: {template_path}")
        
        # sample 폴더에 있는지 확인
        self.assertIn('sample', template_path, "템플릿 파일이 sample 폴더에 있어야 합니다")
        self.assertIn('급여명세서_template.xlsx', template_path, "템플릿 파일명이 올바르지 않습니다")
        
        # 파일 확장자 확인
        self.assertTrue(template_path.endswith('.xlsx'), "템플릿 파일은 .xlsx 확장자를 가져야 합니다")
    
    def test_template_sample2_path(self):
        """TemplateSample2 경로 테스트"""
        design = TemplateSample2()
        template_path = design._get_template_path()
        
        # 경로가 존재하는지 확인
        self.assertTrue(os.path.exists(template_path), f"템플릿 파일이 존재하지 않습니다: {template_path}")
        
        # sample 폴더에 있는지 확인
        self.assertIn('sample', template_path, "템플릿 파일이 sample 폴더에 있어야 합니다")
        self.assertIn('임금명세서양식_template3.xlsx', template_path, "템플릿 파일명이 올바르지 않습니다")
        
        # 파일 확장자 확인
        self.assertTrue(template_path.endswith('.xlsx'), "템플릿 파일은 .xlsx 확장자를 가져야 합니다")
    
    def test_template_path_priority(self):
        """템플릿 경로 우선순위 테스트"""
        # sample 폴더에 파일이 있으면 sample 폴더 경로를 우선 사용해야 함
        design1 = TemplateSample1()
        path1 = design1._get_template_path()
        
        # sample 폴더 경로가 우선순위가 높아야 함
        self.assertIn('sample', path1, "sample 폴더 경로가 우선순위가 높아야 합니다")
    
    def test_template_file_exists(self):
        """템플릿 파일 존재 확인"""
        # sample 폴더에 템플릿 파일이 있는지 확인
        template1_path = self.sample_dir / '급여명세서_template.xlsx'
        template2_path = self.sample_dir / '임금명세서양식_template3.xlsx'
        
        self.assertTrue(template1_path.exists(), f"템플릿 파일이 없습니다: {template1_path}")
        self.assertTrue(template2_path.exists(), f"템플릿 파일이 없습니다: {template2_path}")


if __name__ == '__main__':
    unittest.main()
