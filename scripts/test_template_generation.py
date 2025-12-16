#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""템플릿 디자인 생성 테스트 스크립트

실제 샘플 데이터로 템플릿 디자인이 제대로 작동하는지 테스트합니다.
"""

import sys
import os
import tempfile
from datetime import datetime

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_template_generation():
    """템플릿 디자인 생성 테스트"""
    print("="*70)
    print("템플릿 디자인 생성 테스트")
    print("="*70)
    
    # 샘플 데이터 준비
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
    
    # 테스트할 디자인 목록
    design_names = ['template_sample1', 'template_sample2']
    
    results = []
    
    for design_name in design_names:
        print(f"\n{'='*70}")
        print(f"테스트: {design_name}")
        print(f"{'='*70}")
        
        try:
            # DesignFactory를 통해 디자인 가져오기
            from payroll_generator.templates.designs.design_factory import DesignFactory
            
            design = DesignFactory.get_design(design_name)
            if not design:
                print(f"❌ 디자인을 찾을 수 없습니다: {design_name}")
                results.append((design_name, False, "디자인을 찾을 수 없음"))
                continue
            
            print(f"✓ 디자인 인스턴스 생성 성공")
            print(f"  - 템플릿 파일: {design.template_filename}")
            print(f"  - 셀 매핑 개수: {len(design.cell_mapping)}")
            
            # 엑셀 생성 테스트
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                print(f"\n엑셀 생성 중...")
                design.generate_excel(
                    sample_payroll_data,
                    sample_employee_data,
                    output_path,
                    period
                )
                
                # 파일 확인
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    print(f"✓ 엑셀 파일 생성 성공")
                    print(f"  - 파일 경로: {output_path}")
                    print(f"  - 파일 크기: {file_size:,} bytes")
                    
                    # 파일을 열어서 확인하도록 안내
                    print(f"\n📝 다음 단계:")
                    print(f"  1. 생성된 파일을 엑셀로 열어서 확인하세요: {output_path}")
                    print(f"  2. 다음 데이터가 올바른 위치에 있는지 확인하세요:")
                    print(f"     - 이름: {sample_employee_data['이름']}")
                    print(f"     - 주민번호: 123456-*******")
                    print(f"     - 입사일: 2020-01-01")
                    print(f"     - 기본급: {sample_payroll_data['기본급']:,}원")
                    print(f"     - 실수령액: {sample_payroll_data['실수령액']:,}원")
                    print(f"  3. 셀 위치가 맞지 않으면 셀 매핑 JSON 파일을 수정하세요")
                    
                    results.append((design_name, True, f"파일 생성 성공 ({file_size:,} bytes)"))
                else:
                    print(f"❌ 엑셀 파일이 생성되지 않았습니다")
                    results.append((design_name, False, "파일 생성 실패"))
                    
            except FileNotFoundError as e:
                print(f"❌ 템플릿 파일을 찾을 수 없습니다: {e}")
                results.append((design_name, False, f"템플릿 파일 없음: {e}"))
            except Exception as e:
                print(f"❌ 엑셀 생성 실패: {e}")
                import traceback
                traceback.print_exc()
                results.append((design_name, False, f"생성 실패: {e}"))
            finally:
                # 테스트 파일은 삭제하지 않음 (확인용)
                if os.path.exists(output_path):
                    print(f"\n💡 테스트 파일이 유지됩니다: {output_path}")
                    print(f"   확인 후 수동으로 삭제하세요.")
                    
        except ImportError as e:
            print(f"❌ Import 오류: {e}")
            print(f"   필요한 패키지를 설치하세요: pip install -r requirements.txt")
            results.append((design_name, False, f"Import 오류: {e}"))
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
            import traceback
            traceback.print_exc()
            results.append((design_name, False, f"예상치 못한 오류: {e}"))
    
    # 결과 요약
    print(f"\n{'='*70}")
    print("테스트 결과 요약")
    print(f"{'='*70}")
    
    for design_name, success, message in results:
        status = "✓ 성공" if success else "❌ 실패"
        print(f"{status}: {design_name} - {message}")
    
    success_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)
    
    print(f"\n총 {total_count}개 중 {success_count}개 성공")
    
    if success_count == total_count:
        print("\n✅ 모든 테스트 통과!")
    else:
        print("\n⚠️ 일부 테스트 실패. 위의 오류 메시지를 확인하세요.")
    
    return success_count == total_count


if __name__ == '__main__':
    success = test_template_generation()
    sys.exit(0 if success else 1)
