#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""템플릿 디자인 흐름 테스트 스크립트

실제 코드 흐름을 따라가며 어디서 문제가 발생하는지 확인합니다.
"""

import sys
import os
import tempfile
from datetime import datetime

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_design_flow():
    """디자인 흐름 테스트"""
    print("="*70)
    print("템플릿 디자인 흐름 테스트")
    print("="*70)
    
    # 샘플 데이터
    sample_payroll_data = {
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
    
    sample_employee_data = {
        '이름': '홍길동',
        '주민번호': '123456-1234567',
        '입사일': datetime(2020, 1, 1),
    }
    
    period = '2025-01'
    design_name = 'template_sample1'
    
    print(f"\n1. DesignFactory에서 디자인 가져오기")
    print("-"*70)
    try:
        from payroll_generator.templates.designs.design_factory import DesignFactory
        
        print(f"요청한 디자인: {design_name}")
        print(f"사용 가능한 디자인: {DesignFactory.list_available_designs()}")
        print(f"_designs 상태:")
        for name, cls in DesignFactory._designs.items():
            status = "✓ 클래스 존재" if cls is not None else "❌ None"
            print(f"  {name:20s}: {status} ({cls})")
        
        design = DesignFactory.get_design(design_name)
        if design:
            print(f"✓ 디자인 인스턴스 획득 성공: {type(design)}")
            print(f"  템플릿 파일: {design.template_filename}")
            print(f"  셀 매핑 개수: {len(design.cell_mapping)}")
        else:
            print(f"❌ 디자인 인스턴스가 None입니다!")
            print("   DesignFactory.get_design()이 None을 반환했습니다.")
            return False
    except Exception as e:
        print(f"❌ DesignFactory 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"\n2. 엑셀 생성 테스트")
    print("-"*70)
    try:
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            excel_path = tmp.name
        
        print(f"엑셀 파일 생성 중: {excel_path}")
        design.generate_excel(sample_payroll_data, sample_employee_data, excel_path, period)
        
        if os.path.exists(excel_path):
            file_size = os.path.getsize(excel_path)
            print(f"✓ 엑셀 파일 생성 성공 ({file_size:,} bytes)")
            print(f"  파일 경로: {excel_path}")
        else:
            print(f"❌ 엑셀 파일이 생성되지 않았습니다!")
            return False
    except Exception as e:
        print(f"❌ 엑셀 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"\n3. PDF 생성 테스트 (실제 흐름 시뮬레이션)")
    print("-"*70)
    try:
        from payroll_generator.pdf_generator import PDFGenerator
        
        pdf_gen = PDFGenerator()
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            pdf_path = tmp.name
        
        print(f"PDF 생성 중: {pdf_path}")
        print(f"design_name 전달: {design_name}")
        
        result = pdf_gen.generate_payslip(
            sample_payroll_data,
            sample_employee_data,
            pdf_path,
            period,
            use_template=True,
            design_name=design_name
        )
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✓ PDF 파일 생성 성공 ({file_size:,} bytes)")
            print(f"  파일 경로: {pdf_path}")
            print(f"  반환값: {result}")
        else:
            print(f"❌ PDF 파일이 생성되지 않았습니다!")
            return False
    except Exception as e:
        print(f"❌ PDF 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"\n4. 생성된 파일 확인")
    print("-"*70)
    print(f"엑셀 파일: {excel_path}")
    print(f"PDF 파일: {pdf_path}")
    print(f"\n💡 다음 단계:")
    print(f"  1. 엑셀 파일을 열어서 템플릿 디자인이 적용되었는지 확인")
    print(f"  2. PDF 파일을 열어서 템플릿 디자인이 적용되었는지 확인")
    print(f"  3. 두 파일이 동일한 디자인인지 비교")
    
    print("\n" + "="*70)
    print("✅ 흐름 테스트 완료")
    print("="*70)
    return True


if __name__ == '__main__':
    success = test_design_flow()
    sys.exit(0 if success else 1)
