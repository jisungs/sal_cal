#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""급여자동계산기 데모 실행 스크립트"""

import sys
import os

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from config import (
    INSURANCE_RATES, 
    INSURANCE_LIMITS, 
    INCOME_TAX_TABLE,
    DEPENDENT_DEDUCTION
)
from utils import mask_resident_number
from logger import setup_logger
from calculator import PayrollCalculator
from excel_handler import ExcelHandler

def print_header(title):
    """헤더 출력"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_section(title):
    """섹션 제목 출력"""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")

def demo_read_excel():
    """엑셀 파일 읽기 데모"""
    print_header("📄 엑셀 파일 읽기 데모")
    
    handler = ExcelHandler()
    template_path = 'payroll_generator/templates/employee_template.xlsx'
    
    if not os.path.exists(template_path):
        print(f"❌ 템플릿 파일을 찾을 수 없습니다: {template_path}")
        return None
    
    try:
        print(f"\n📁 파일 경로: {template_path}")
        print("   파일 읽는 중...")
        
        df = handler.read_employee_data(template_path)
        
        print(f"\n✅ 성공! {len(df)}명의 직원 정보를 읽었습니다.\n")
        
        # 데이터 미리보기
        print("📋 직원 정보 미리보기:")
        print("─" * 70)
        for idx, row in df.iterrows():
            name = row.get('이름', '')
            rrn = mask_resident_number(str(row.get('주민번호', '')))
            join_date = row.get('입사일', '')
            base_salary = row.get('기본급', 0)
            dependents = row.get('부양가족수', 0)
            
            print(f"  {idx+1}. {name}")
            print(f"     주민번호: {rrn}")
            print(f"     입사일: {join_date}")
            print(f"     기본급: {base_salary:,}원")
            print(f"     부양가족수: {dependents}명")
            if row.get('연장근무시간', 0) > 0:
                print(f"     연장근무: {row.get('연장근무시간', 0)}시간")
            if row.get('상여금', 0) > 0:
                print(f"     상여금: {row.get('상여금', 0):,}원")
            print()
        
        return df
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None

def demo_calculate_payroll(df):
    """급여 계산 데모"""
    print_header("💰 급여 계산 데모")
    
    calculator = PayrollCalculator()
    
    if df is None or len(df) == 0:
        print("❌ 계산할 직원 데이터가 없습니다.")
        return
    
    print(f"\n📊 {len(df)}명의 직원 급여를 계산합니다...\n")
    
    total_payment = 0
    total_deduction = 0
    total_net_pay = 0
    
    for idx, row in df.iterrows():
        employee_name = row.get('이름', f'직원{idx+1}')
        print_section(f"👤 {employee_name}님의 급여 계산")
        
        # 급여 계산
        result = calculator.calculate_deductions(row.to_dict())
        
        # 지급 항목
        print("\n  💵 지급 항목:")
        print(f"     기본급:           {result['기본급']:>12,}원")
        if result['연장근무수당'] > 0:
            print(f"     연장근무수당:     {result['연장근무수당']:>12,}원")
        if result['상여금'] > 0:
            print(f"     상여금:           {result['상여금']:>12,}원")
        print(f"     ─────────────────────────────")
        print(f"     총 지급액:        {result['총지급액']:>12,}원")
        
        # 공제 항목
        print("\n  💸 공제 항목:")
        print(f"     국민연금:         {result['국민연금']:>12,}원")
        print(f"     건강보험:         {result['건강보험']:>12,}원")
        print(f"     장기요양:         {result['장기요양']:>12,}원")
        print(f"     고용보험:         {result['고용보험']:>12,}원")
        if result['부양가족공제'] > 0:
            print(f"     부양가족공제:     {result['부양가족공제']:>12,}원")
        print(f"     소득세:           {result['소득세']:>12,}원")
        print(f"     지방소득세:       {result['지방소득세']:>12,}원")
        print(f"     ─────────────────────────────")
        print(f"     총 공제액:        {result['총공제액']:>12,}원")
        
        # 실수령액
        print("\n  💰 실수령액:")
        print(f"     {result['실수령액']:>12,}원")
        
        # 합계 누적
        total_payment += result['총지급액']
        total_deduction += result['총공제액']
        total_net_pay += result['실수령액']
    
    # 전체 합계
    print_header("📊 전체 급여 현황 요약")
    print(f"\n  총 직원 수:        {len(df):>12}명")
    print(f"  총 지급액:        {total_payment:>12,}원")
    print(f"  총 공제액:        {total_deduction:>12,}원")
    print(f"  총 실수령액:      {total_net_pay:>12,}원")
    print(f"\n  평균 급여:        {total_payment // len(df):>12,}원")
    print(f"  평균 공제액:      {total_deduction // len(df):>12,}원")
    print(f"  평균 실수령액:    {total_net_pay // len(df):>12,}원")

def demo_config_info():
    """설정 정보 데모"""
    print_header("⚙️  시스템 설정 정보")
    
    print("\n📋 4대보험 요율 (2025년 기준):")
    print("─" * 70)
    for key, value in INSURANCE_RATES.items():
        insurance_name = {
            'national_pension': '국민연금',
            'health_insurance': '건강보험',
            'long_term_care': '장기요양',
            'employment_insurance': '고용보험'
        }.get(key, key)
        print(f"  {insurance_name:12s}: {value*100:>6.2f}%")
    
    print("\n📋 4대보험 상한액:")
    print("─" * 70)
    for key, value in INSURANCE_LIMITS.items():
        insurance_name = {
            'national_pension': '국민연금',
            'health_insurance': '건강보험',
            'employment_insurance': '고용보험'
        }.get(key, key)
        print(f"  {insurance_name:12s}: {value:>12,}원")
    
    print("\n📋 소득세 간이세액표:")
    print("─" * 70)
    for start, end, rate, deduction in INCOME_TAX_TABLE:
        if end == float('inf'):
            print(f"  {start:>12,}원 이상: {rate*100:>5.1f}% (누진공제: {deduction:>10,}원)")
        else:
            print(f"  {start:>12,}원 ~ {end:>12,}원: {rate*100:>5.1f}% (누진공제: {deduction:>10,}원)")
    
    print("\n📋 부양가족 공제액:")
    print("─" * 70)
    for dependents, deduction in DEPENDENT_DEDUCTION.items():
        if dependents == 4:
            print(f"  {dependents}명 이상:     {deduction:>12,}원")
        else:
            print(f"  {dependents}명:           {deduction:>12,}원")

def main():
    """메인 데모 함수"""
    # 로거 설정
    logger = setup_logger()
    logger.info("데모 프로그램 시작")
    
    print("\n" + "=" * 70)
    print("  💼 급여명세서 자동생성기 - 데모 프로그램")
    print("=" * 70)
    print("\n  현재 구현된 기능을 테스트합니다.")
    print("  템플릿 파일을 읽어서 급여를 계산하고 결과를 보여줍니다.\n")
    
    import time
    time.sleep(1)  # 1초 대기
    
    # 1. 설정 정보 보기
    demo_config_info()
    
    time.sleep(1)  # 1초 대기
    
    # 2. 엑셀 파일 읽기
    df = demo_read_excel()
    
    if df is not None:
        time.sleep(1)  # 1초 대기
        
        # 3. 급여 계산
        demo_calculate_payroll(df)
        
        print("\n" + "=" * 70)
        print("  ✅ 데모 완료!")
        print("=" * 70)
        print("\n  다음 단계:")
        print("  - 엑셀 출력 기능 구현 (Day 3)")
        print("  - PDF 출력 기능 구현 (Day 5)")
        print("  - GUI 인터페이스 구현 (Day 4)")
        print("\n")
    else:
        print("\n❌ 엑셀 파일을 읽을 수 없어 급여 계산을 진행할 수 없습니다.")
    
    logger.info("데모 프로그램 종료")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

