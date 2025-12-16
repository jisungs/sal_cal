#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""템플릿 디자인 클래스 테스트"""

import unittest
import os
import tempfile
import sys

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from payroll_generator.templates.designs.template_sample1 import TemplateSample1
    from payroll_generator.templates.designs.template_sample2 import TemplateSample2
    from payroll_generator.templates.designs.design_factory import DesignFactory
except ImportError as e:
    print(f"Import 오류: {e}")
    print("필요한 모듈을 확인하세요.")
    sys.exit(1)


class TestTemplateDesign(unittest.TestCase):
    """템플릿 디자인 클래스 테스트"""
    
    def setUp(self):
        """테스트 데이터 준비"""
        self.sample_payroll_data = {
            '기본급': 3000000,
            '연장근무수당': 500000,
            '상여금': 0,
            '총지급액': 3500000,
            '국민연금': 157500,
            '건강보험': 105000,
            '장기요양': 15750,
            '고용보험': 10500,
            '소득세': 50000,
            '지방소득세': 5000,
            '총공제액': 343750,
            '실수령액': 3156250,
        }
        self.sample_employee_data = {
            '이름': '홍길동',
            '주민번호': '123456-1234567',
            '입사일': '2020-01-01',
        }
        self.period = '2025-01'
    
    def test_template_sample1_init(self):
        """TemplateSample1 초기화 테스트"""
        try:
            design = TemplateSample1()
            self.assertIsNotNone(design)
            self.assertEqual(design.template_filename, 'template_sample1.xlsx')
            print("✓ TemplateSample1 초기화 성공")
        except Exception as e:
            self.fail(f"TemplateSample1 초기화 실패: {e}")
    
    def test_template_sample1_cell_mapping(self):
        """TemplateSample1 셀 매핑 확인"""
        try:
            design = TemplateSample1()
            # 셀 매핑이 비어있지 않은지 확인 (기본 매핑이 있거나 JSON 파일이 있으면)
            self.assertIsNotNone(design.cell_mapping)
            print(f"✓ TemplateSample1 셀 매핑: {len(design.cell_mapping)}개")
        except Exception as e:
            self.fail(f"셀 매핑 확인 실패: {e}")
    
    def test_template_sample1_excel_generation(self):
        """TemplateSample1 엑셀 생성 테스트"""
        try:
            design = TemplateSample1()
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                design.generate_excel(
                    self.sample_payroll_data,
                    self.sample_employee_data,
                    output_path,
                    self.period
                )
                self.assertTrue(os.path.exists(output_path), "엑셀 파일이 생성되지 않았습니다")
                self.assertGreater(os.path.getsize(output_path), 0, "엑셀 파일이 비어있습니다")
                print(f"✓ TemplateSample1 엑셀 생성 성공: {output_path}")
            finally:
                if os.path.exists(output_path):
                    os.remove(output_path)
        except FileNotFoundError as e:
            self.skipTest(f"템플릿 파일을 찾을 수 없습니다: {e}")
        except Exception as e:
            self.fail(f"엑셀 생성 실패: {e}")
    
    def test_template_sample2_init(self):
        """TemplateSample2 초기화 테스트"""
        try:
            design = TemplateSample2()
            self.assertIsNotNone(design)
            self.assertEqual(design.template_filename, 'template_sample2.xlsx')
            print("✓ TemplateSample2 초기화 성공")
        except Exception as e:
            self.fail(f"TemplateSample2 초기화 실패: {e}")
    
    def test_template_sample2_cell_mapping(self):
        """TemplateSample2 셀 매핑 확인"""
        try:
            design = TemplateSample2()
            self.assertIsNotNone(design.cell_mapping)
            print(f"✓ TemplateSample2 셀 매핑: {len(design.cell_mapping)}개")
        except Exception as e:
            self.fail(f"셀 매핑 확인 실패: {e}")
    
    def test_template_sample2_excel_generation(self):
        """TemplateSample2 엑셀 생성 테스트"""
        try:
            design = TemplateSample2()
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                design.generate_excel(
                    self.sample_payroll_data,
                    self.sample_employee_data,
                    output_path,
                    self.period
                )
                self.assertTrue(os.path.exists(output_path), "엑셀 파일이 생성되지 않았습니다")
                self.assertGreater(os.path.getsize(output_path), 0, "엑셀 파일이 비어있습니다")
                print(f"✓ TemplateSample2 엑셀 생성 성공: {output_path}")
            finally:
                if os.path.exists(output_path):
                    os.remove(output_path)
        except FileNotFoundError as e:
            self.skipTest(f"템플릿 파일을 찾을 수 없습니다: {e}")
        except Exception as e:
            self.fail(f"엑셀 생성 실패: {e}")
    
    def test_design_factory_template_sample1(self):
        """DesignFactory를 통한 TemplateSample1 가져오기"""
        try:
            design = DesignFactory.get_design('template_sample1')
            self.assertIsNotNone(design, "DesignFactory가 template_sample1을 반환하지 않았습니다")
            self.assertEqual(design.template_filename, 'template_sample1.xlsx')
            print("✓ DesignFactory template_sample1 가져오기 성공")
        except Exception as e:
            self.fail(f"DesignFactory 테스트 실패: {e}")
    
    def test_design_factory_template_sample2(self):
        """DesignFactory를 통한 TemplateSample2 가져오기"""
        try:
            design = DesignFactory.get_design('template_sample2')
            self.assertIsNotNone(design, "DesignFactory가 template_sample2를 반환하지 않았습니다")
            self.assertEqual(design.template_filename, 'template_sample2.xlsx')
            print("✓ DesignFactory template_sample2 가져오기 성공")
        except Exception as e:
            self.fail(f"DesignFactory 테스트 실패: {e}")
    
    def test_design_factory_list_available_designs(self):
        """사용 가능한 디자인 목록 확인"""
        try:
            designs = DesignFactory.list_available_designs()
            self.assertIn('template_sample1', designs, "template_sample1이 목록에 없습니다")
            self.assertIn('template_sample2', designs, "template_sample2가 목록에 없습니다")
            print(f"✓ 사용 가능한 디자인: {designs}")
        except Exception as e:
            self.fail(f"디자인 목록 확인 실패: {e}")
    
    def test_design_factory_is_available(self):
        """디자인 사용 가능 여부 확인"""
        try:
            self.assertTrue(DesignFactory.is_design_available('template_sample1'))
            self.assertTrue(DesignFactory.is_design_available('template_sample2'))
            self.assertFalse(DesignFactory.is_design_available('nonexistent_design'))
            print("✓ 디자인 사용 가능 여부 확인 성공")
        except Exception as e:
            self.fail(f"디자인 사용 가능 여부 확인 실패: {e}")


class TestTemplateDesignIntegration(unittest.TestCase):
    """템플릿 디자인 통합 테스트"""
    
    def setUp(self):
        """테스트 데이터 준비"""
        self.sample_payroll_data = {
            '기본급': 3000000,
            '연장근무수당': 500000,
            '상여금': 0,
            '총지급액': 3500000,
            '국민연금': 157500,
            '건강보험': 105000,
            '장기요양': 15750,
            '고용보험': 10500,
            '소득세': 50000,
            '지방소득세': 5000,
            '총공제액': 343750,
            '실수령액': 3156250,
        }
        self.sample_employee_data = {
            '이름': '홍길동',
            '주민번호': '123456-1234567',
            '입사일': '2020-01-01',
        }
    
    def test_excel_handler_with_template_design(self):
        """ExcelHandler를 통한 템플릿 디자인 사용 테스트"""
        try:
            from payroll_generator.excel_handler import ExcelHandler
            
            excel_handler = ExcelHandler()
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                excel_handler.write_payroll(
                    self.sample_payroll_data,
                    output_path,
                    self.sample_employee_data,
                    '2025-01',
                    use_template=True,
                    design_name='template_sample1'
                )
                self.assertTrue(os.path.exists(output_path))
                self.assertGreater(os.path.getsize(output_path), 0)
                print(f"✓ ExcelHandler를 통한 template_sample1 생성 성공")
            finally:
                if os.path.exists(output_path):
                    os.remove(output_path)
        except Exception as e:
            self.fail(f"ExcelHandler 통합 테스트 실패: {e}")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("템플릿 디자인 클래스 테스트 시작")
    print("="*70 + "\n")
    
    unittest.main(verbosity=2)
