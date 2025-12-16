#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 6: 통합 테스트 및 검증

테스트 시나리오:
1. Template1 엑셀 생성 통합 테스트
2. Template2 엑셀 생성 통합 테스트
3. Template1 PDF 생성 통합 테스트
4. Template2 PDF 생성 통합 테스트
5. DesignFactory 동작 테스트
6. 에러 처리 테스트 (템플릿 파일 없을 때 등)
"""

import unittest
import os
import tempfile
import shutil
from pathlib import Path

# 프로젝트 루트를 경로에 추가
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from payroll_generator.calculator import PayrollCalculator
from payroll_generator.templates.designs.design_factory import DesignFactory
from payroll_generator.templates.designs.template_sample1 import TemplateSample1
from payroll_generator.templates.designs.template_sample2 import TemplateSample2


class TestIntegrationPhase6(unittest.TestCase):
    """Phase 6 통합 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        self.test_output_dir = tempfile.mkdtemp(prefix='phase6_test_')
        self.calculator = PayrollCalculator()
        
        # 테스트 데이터
        self.employee_data = {
            '이름': '홍길동',
            '주민번호': '123456-1234567',
            '입사일': '2020-01-01',
            '기본급': 1000000,
            '부양가족수': 1,
            '연장근무시간': 10,
            '연장근무단가': 10000,
            '상여금': 0,
            '소속': '개발팀',
            '직급': '선임'
        }
        
        self.period = '2025-12'
    
    def tearDown(self):
        """테스트 정리"""
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
    
    def test_01_template1_excel_generation(self):
        """Template1 엑셀 생성 통합 테스트"""
        print("\n=== 테스트 1: Template1 엑셀 생성 ===")
        
        # 급여 계산
        payroll_data = self.calculator.calculate_deductions(self.employee_data)
        
        # Template1 디자인 가져오기
        design = DesignFactory.get_design('template_sample1')
        self.assertIsNotNone(design, "Template1 디자인을 가져올 수 없습니다")
        
        # 엑셀 파일 생성
        excel_path = os.path.join(self.test_output_dir, 'test_template1.xlsx')
        result = design.generate_excel(payroll_data, self.employee_data, excel_path, self.period)
        
        # 검증 (generate_excel은 경로를 반환하거나 None을 반환할 수 있음)
        # 파일 존재 여부로 검증
        self.assertTrue(os.path.exists(excel_path), f"엑셀 파일이 생성되지 않았습니다: {excel_path}")
        self.assertGreater(os.path.getsize(excel_path), 0, "엑셀 파일 크기가 0입니다")
        
        print(f"✓ Template1 엑셀 생성 성공: {excel_path} ({os.path.getsize(excel_path):,} bytes)")
    
    def test_02_template2_excel_generation(self):
        """Template2 엑셀 생성 통합 테스트"""
        print("\n=== 테스트 2: Template2 엑셀 생성 ===")
        
        # 급여 계산
        payroll_data = self.calculator.calculate_deductions(self.employee_data)
        
        # Template2 디자인 가져오기
        design = DesignFactory.get_design('template_sample2')
        self.assertIsNotNone(design, "Template2 디자인을 가져올 수 없습니다")
        
        # 엑셀 파일 생성
        excel_path = os.path.join(self.test_output_dir, 'test_template2.xlsx')
        result = design.generate_excel(payroll_data, self.employee_data, excel_path, self.period)
        
        # 검증 (generate_excel은 경로를 반환하거나 None을 반환할 수 있음)
        # 파일 존재 여부로 검증
        self.assertTrue(os.path.exists(excel_path), f"엑셀 파일이 생성되지 않았습니다: {excel_path}")
        self.assertGreater(os.path.getsize(excel_path), 0, "엑셀 파일 크기가 0입니다")
        
        print(f"✓ Template2 엑셀 생성 성공: {excel_path} ({os.path.getsize(excel_path):,} bytes)")
    
    def test_03_template1_pdf_generation(self):
        """Template1 PDF 생성 통합 테스트"""
        print("\n=== 테스트 3: Template1 PDF 생성 ===")
        
        # 급여 계산
        payroll_data = self.calculator.calculate_deductions(self.employee_data)
        
        # Template1 디자인 가져오기
        design = DesignFactory.get_design('template_sample1')
        self.assertIsNotNone(design, "Template1 디자인을 가져올 수 없습니다")
        
        # PDF 파일 생성
        pdf_path = os.path.join(self.test_output_dir, 'test_template1.pdf')
        
        try:
            result = design.generate_pdf(payroll_data, self.employee_data, pdf_path, self.period)
            
            # 검증
            self.assertIsNotNone(result, "PDF 파일 생성 실패")
            self.assertTrue(os.path.exists(pdf_path), f"PDF 파일이 생성되지 않았습니다: {pdf_path}")
            self.assertGreater(os.path.getsize(pdf_path), 0, "PDF 파일 크기가 0입니다")
            
            print(f"✓ Template1 PDF 생성 성공: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
        except RuntimeError as e:
            # LibreOffice가 없으면 엑셀 파일이 생성되었는지 확인
            excel_path = pdf_path.replace('.pdf', '.xlsx')
            if os.path.exists(excel_path):
                print(f"⚠ PDF 변환 실패 (LibreOffice 필요), 엑셀 파일 생성됨: {excel_path}")
                self.skipTest(f"PDF 변환 실패 (LibreOffice 필요): {e}")
            else:
                raise
    
    def test_04_template2_pdf_generation(self):
        """Template2 PDF 생성 통합 테스트"""
        print("\n=== 테스트 4: Template2 PDF 생성 ===")
        
        # 급여 계산
        payroll_data = self.calculator.calculate_deductions(self.employee_data)
        
        # Template2 디자인 가져오기
        design = DesignFactory.get_design('template_sample2')
        self.assertIsNotNone(design, "Template2 디자인을 가져올 수 없습니다")
        
        # PDF 파일 생성
        pdf_path = os.path.join(self.test_output_dir, 'test_template2.pdf')
        
        try:
            result = design.generate_pdf(payroll_data, self.employee_data, pdf_path, self.period)
            
            # 검증
            self.assertIsNotNone(result, "PDF 파일 생성 실패")
            self.assertTrue(os.path.exists(pdf_path), f"PDF 파일이 생성되지 않았습니다: {pdf_path}")
            self.assertGreater(os.path.getsize(pdf_path), 0, "PDF 파일 크기가 0입니다")
            
            print(f"✓ Template2 PDF 생성 성공: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
        except RuntimeError as e:
            # LibreOffice가 없으면 엑셀 파일이 생성되었는지 확인
            excel_path = pdf_path.replace('.pdf', '.xlsx')
            if os.path.exists(excel_path):
                print(f"⚠ PDF 변환 실패 (LibreOffice 필요), 엑셀 파일 생성됨: {excel_path}")
                self.skipTest(f"PDF 변환 실패 (LibreOffice 필요): {e}")
            else:
                raise
    
    def test_05_design_factory_availability(self):
        """DesignFactory 동작 테스트"""
        print("\n=== 테스트 5: DesignFactory 동작 확인 ===")
        
        # 사용 가능한 디자인 목록 확인
        available_designs = DesignFactory.list_available_designs()
        print(f"사용 가능한 디자인: {available_designs}")
        
        # template_sample1, template_sample2가 있어야 함
        self.assertIn('template_sample1', available_designs, "template_sample1이 사용 가능하지 않습니다")
        self.assertIn('template_sample2', available_designs, "template_sample2가 사용 가능하지 않습니다")
        
        # design_1, design_2는 없어야 함
        self.assertNotIn('design_1', available_designs, "design_1이 제거되지 않았습니다")
        self.assertNotIn('design_2', available_designs, "design_2가 제거되지 않았습니다")
        
        # 디자인 가져오기 테스트
        design1 = DesignFactory.get_design('template_sample1')
        self.assertIsNotNone(design1, "template_sample1을 가져올 수 없습니다")
        
        design2 = DesignFactory.get_design('template_sample2')
        self.assertIsNotNone(design2, "template_sample2를 가져올 수 없습니다")
        
        # design_1, design_2는 None을 반환해야 함
        old_design1 = DesignFactory.get_design('design_1')
        self.assertIsNone(old_design1, "design_1이 제거되지 않았습니다")
        
        old_design2 = DesignFactory.get_design('design_2')
        self.assertIsNone(old_design2, "design_2가 제거되지 않았습니다")
        
        print("✓ DesignFactory 동작 확인 완료")
    
    def test_06_error_handling_invalid_design(self):
        """에러 처리 테스트: 잘못된 디자인 이름"""
        print("\n=== 테스트 6: 잘못된 디자인 이름 처리 ===")
        
        # 존재하지 않는 디자인
        design = DesignFactory.get_design('invalid_design')
        self.assertIsNone(design, "잘못된 디자인은 None을 반환해야 합니다")
        
        print("✓ 잘못된 디자인 이름 처리 확인")
    
    def test_07_error_handling_design_1_2_fallback(self):
        """에러 처리 테스트: design_1, design_2 폴백"""
        print("\n=== 테스트 7: design_1, design_2 폴백 처리 ===")
        
        # design_1은 None을 반환해야 함 (폴백)
        design1 = DesignFactory.get_design('design_1')
        self.assertIsNone(design1, "design_1은 None을 반환해야 합니다")
        
        # design_2는 None을 반환해야 함 (폴백)
        design2 = DesignFactory.get_design('design_2')
        self.assertIsNone(design2, "design_2는 None을 반환해야 합니다")
        
        print("✓ design_1, design_2 폴백 처리 확인")
    
    def test_08_template_path_resolution(self):
        """템플릿 경로 해석 테스트"""
        print("\n=== 테스트 8: 템플릿 경로 해석 ===")
        
        # Template1 경로 확인
        design1 = TemplateSample1()
        template_path1 = design1._get_template_path()
        self.assertTrue(os.path.exists(template_path1), f"Template1 경로를 찾을 수 없습니다: {template_path1}")
        print(f"✓ Template1 경로: {template_path1}")
        
        # Template2 경로 확인
        design2 = TemplateSample2()
        template_path2 = design2._get_template_path()
        self.assertTrue(os.path.exists(template_path2), f"Template2 경로를 찾을 수 없습니다: {template_path2}")
        print(f"✓ Template2 경로: {template_path2}")
    
    def test_09_default_design_handling(self):
        """기본 디자인 처리 테스트"""
        print("\n=== 테스트 9: 기본 디자인 처리 ===")
        
        # default 디자인은 None을 반환해야 함
        design = DesignFactory.get_design('default')
        self.assertIsNone(design, "default 디자인은 None을 반환해야 합니다")
        
        # None도 기본 디자인으로 처리
        design_none = DesignFactory.get_design(None)
        self.assertIsNone(design_none, "None 디자인은 None을 반환해야 합니다")
        
        print("✓ 기본 디자인 처리 확인")


if __name__ == '__main__':
    # 테스트 실행
    unittest.main(verbosity=2)
