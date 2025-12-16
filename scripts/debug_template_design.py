#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""템플릿 디자인 디버깅 스크립트

템플릿 디자인이 제대로 작동하는지 확인하는 스크립트입니다.
"""

import sys
import os

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def debug_template_design():
    """템플릿 디자인 디버깅"""
    print("="*70)
    print("템플릿 디자인 디버깅")
    print("="*70)
    
    # 1. DesignFactory Import 테스트
    print("\n1. DesignFactory Import 테스트")
    print("-"*70)
    try:
        from payroll_generator.templates.designs.design_factory import DesignFactory
        print("✓ DesignFactory import 성공")
    except Exception as e:
        print(f"❌ DesignFactory import 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 2. 사용 가능한 디자인 확인
    print("\n2. 사용 가능한 디자인 확인")
    print("-"*70)
    try:
        available_designs = DesignFactory.list_available_designs()
        print(f"사용 가능한 디자인: {available_designs}")
        
        if 'template_sample1' not in available_designs:
            print("❌ template_sample1이 사용 가능한 디자인 목록에 없습니다!")
        else:
            print("✓ template_sample1이 사용 가능한 디자인 목록에 있습니다")
        
        if 'template_sample2' not in available_designs:
            print("❌ template_sample2가 사용 가능한 디자인 목록에 없습니다!")
        else:
            print("✓ template_sample2가 사용 가능한 디자인 목록에 있습니다")
    except Exception as e:
        print(f"❌ 디자인 목록 확인 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 3. _designs 딕셔너리 확인
    print("\n3. _designs 딕셔너리 확인")
    print("-"*70)
    try:
        designs_status = {}
        for name, design_class in DesignFactory._designs.items():
            is_none = design_class is None
            designs_status[name] = is_none
            status = "❌ None" if is_none else "✓ 클래스 존재"
            print(f"  {name:20s}: {status}")
        
        if designs_status.get('template_sample1'):
            print("\n⚠️ template_sample1이 None입니다. Import 실패 가능성!")
            print("   template_sample1.py의 Import 경로를 확인하세요.")
        
        if designs_status.get('template_sample2'):
            print("\n⚠️ template_sample2가 None입니다. Import 실패 가능성!")
            print("   template_sample2.py의 Import 경로를 확인하세요.")
    except Exception as e:
        print(f"❌ _designs 확인 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. TemplateSample1 직접 Import 테스트
    print("\n4. TemplateSample1 직접 Import 테스트")
    print("-"*70)
    try:
        from payroll_generator.templates.designs.template_sample1 import TemplateSample1
        print("✓ TemplateSample1 직접 import 성공")
        print(f"  클래스: {TemplateSample1}")
    except ImportError as e:
        print(f"❌ TemplateSample1 직접 import 실패: {e}")
        print("   template_sample1.py 파일이 올바른 위치에 있는지 확인하세요.")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ TemplateSample1 import 중 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. TemplateSample1 인스턴스 생성 테스트
    print("\n5. TemplateSample1 인스턴스 생성 테스트")
    print("-"*70)
    try:
        instance = TemplateSample1()
        print("✓ TemplateSample1 인스턴스 생성 성공")
        print(f"  템플릿 파일: {instance.template_filename}")
        print(f"  셀 매핑 개수: {len(instance.cell_mapping)}")
    except FileNotFoundError as e:
        print(f"❌ 템플릿 파일을 찾을 수 없습니다: {e}")
        print("   payroll_generator/templates/designs/template_sample1.xlsx 파일을 확인하세요.")
        return False
    except Exception as e:
        print(f"❌ 인스턴스 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 6. DesignFactory를 통한 가져오기 테스트
    print("\n6. DesignFactory를 통한 가져오기 테스트")
    print("-"*70)
    try:
        design = DesignFactory.get_design('template_sample1')
        if design:
            print("✓ DesignFactory.get_design('template_sample1') 성공")
            print(f"  인스턴스: {design}")
            print(f"  템플릿 파일: {design.template_filename}")
        else:
            print("❌ DesignFactory.get_design('template_sample1')가 None을 반환했습니다")
            return False
    except Exception as e:
        print(f"❌ DesignFactory.get_design 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 7. 템플릿 파일 존재 확인
    print("\n7. 템플릿 파일 존재 확인")
    print("-"*70)
    template_paths = [
        os.path.join(project_root, 'payroll_generator', 'templates', 'designs', 'template_sample1.xlsx'),
        os.path.join(project_root, 'payroll_generator', 'templates', 'designs', 'template_sample2.xlsx'),
    ]
    
    for template_path in template_paths:
        if os.path.exists(template_path):
            file_size = os.path.getsize(template_path)
            print(f"✓ {os.path.basename(template_path)} 존재 ({file_size:,} bytes)")
        else:
            print(f"❌ {os.path.basename(template_path)} 없음: {template_path}")
    
    # 8. 셀 매핑 파일 존재 확인
    print("\n8. 셀 매핑 파일 존재 확인")
    print("-"*70)
    mapping_paths = [
        os.path.join(project_root, 'payroll_generator', 'templates', 'designs', 'configs', 'template_sample1_mapping.json'),
        os.path.join(project_root, 'payroll_generator', 'templates', 'designs', 'configs', 'template_sample2_mapping.json'),
    ]
    
    for mapping_path in mapping_paths:
        if os.path.exists(mapping_path):
            file_size = os.path.getsize(mapping_path)
            print(f"✓ {os.path.basename(mapping_path)} 존재 ({file_size:,} bytes)")
        else:
            print(f"⚠️ {os.path.basename(mapping_path)} 없음 (기본 매핑 사용): {mapping_path}")
    
    print("\n" + "="*70)
    print("✅ 모든 테스트 통과!")
    print("="*70)
    return True


if __name__ == '__main__':
    success = debug_template_design()
    sys.exit(0 if success else 1)
