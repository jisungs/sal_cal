#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""템플릿 PDF 생성 테스트 스크립트"""

import os
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from payroll_generator.templates.designs.design_factory import DesignFactory
from payroll_generator.logger import setup_logger

logger = setup_logger()

def test_template_pdf_generation():
    """템플릿 PDF 생성 테스트"""
    
    # 테스트 데이터 준비
    payroll_data = {
        '기본급': 3000000,
        '연장근로수당': 200000,
        '상여금': 500000,
        '국민연금': 135000,
        '건강보험': 93750,
        '장기요양보험': 11250,
        '고용보험': 13500,
        '소득세': 50000,
        '지방소득세': 5000,
        '공제합계': 304500,
        '실수령액': 3395500
    }
    
    employee_data = {
        '이름': '홍길동',
        '주민번호': '123456-1234567',
        '입사일': '2020-01-01',
        '소속': '개발팀',
        '직급': '과장'
    }
    
    period = '2025-12'
    output_dir = project_root / 'outputs' / 'test_pdf'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Template1 테스트
    print("=" * 70)
    print("Template1 PDF 생성 테스트")
    print("=" * 70)
    
    try:
        design1 = DesignFactory.get_design('template_sample1')
        if design1:
            output_path1 = str(output_dir / 'template1_test.pdf')
            print(f"\n✓ Template1 디자인 인스턴스 생성 성공")
            print(f"  PDF 생성 중: {output_path1}")
            
            result1 = design1.generate_pdf(payroll_data, employee_data, output_path1, period)
            
            if os.path.exists(result1):
                size = os.path.getsize(result1)
                print(f"✓ Template1 PDF 생성 성공")
                print(f"  파일 경로: {result1}")
                print(f"  파일 크기: {size:,} bytes")
            else:
                print(f"✗ Template1 PDF 파일이 생성되지 않았습니다")
                print(f"  반환 경로: {result1}")
        else:
            print("✗ Template1 디자인을 찾을 수 없습니다")
    except Exception as e:
        print(f"✗ Template1 PDF 생성 실패: {e}")
        import traceback
        traceback.print_exc()
    
    # Template2 테스트
    print("\n" + "=" * 70)
    print("Template2 PDF 생성 테스트")
    print("=" * 70)
    
    try:
        design2 = DesignFactory.get_design('template_sample2')
        if design2:
            output_path2 = str(output_dir / 'template2_test.pdf')
            print(f"\n✓ Template2 디자인 인스턴스 생성 성공")
            print(f"  PDF 생성 중: {output_path2}")
            
            result2 = design2.generate_pdf(payroll_data, employee_data, output_path2, period)
            
            if os.path.exists(result2):
                size = os.path.getsize(result2)
                print(f"✓ Template2 PDF 생성 성공")
                print(f"  파일 경로: {result2}")
                print(f"  파일 크기: {size:,} bytes")
            else:
                print(f"✗ Template2 PDF 파일이 생성되지 않았습니다")
                print(f"  반환 경로: {result2}")
        else:
            print("✗ Template2 디자인을 찾을 수 없습니다")
    except Exception as e:
        print(f"✗ Template2 PDF 생성 실패: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("테스트 완료")
    print("=" * 70)
    print(f"\n생성된 파일 위치: {output_dir}")
    print("PDF 파일을 확인하여 템플릿 디자인이 제대로 적용되었는지 확인하세요.")


if __name__ == '__main__':
    test_template_pdf_generation()
