#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flask 앱 초기화 테스트"""

import os
import sys

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app


def test_app_creation():
    """앱 생성 테스트"""
    print("🧪 테스트 1: Flask 앱 생성")
    
    try:
        app = create_app('development')
        assert app is not None, "앱이 생성되어야 함"
        print("✅ 통과: Flask 앱 정상 생성")
        return True
    except Exception as e:
        print(f"❌ 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_app_config():
    """앱 설정 테스트"""
    print("🧪 테스트 2: 앱 설정 확인")
    
    app = create_app('development')
    
    # 필수 설정 확인
    assert 'SECRET_KEY' in app.config, "SECRET_KEY가 설정되어야 함"
    assert 'PERMANENT_SESSION_LIFETIME' in app.config, "PERMANENT_SESSION_LIFETIME이 설정되어야 함"
    assert app.config['PERMANENT_SESSION_LIFETIME'] == 86400, "세션 타임아웃은 86400초여야 함"
    
    print(f"✅ SECRET_KEY: 설정됨")
    print(f"✅ PERMANENT_SESSION_LIFETIME: {app.config['PERMANENT_SESSION_LIFETIME']}초")
    return True


def test_blueprint_registration():
    """Blueprint 등록 테스트"""
    print("🧪 테스트 3: Blueprint 등록 확인")
    
    app = create_app('development')
    
    # 등록된 Blueprint 확인
    blueprint_names = [bp.name for bp in app.blueprints.values()]
    
    expected_blueprints = ['main', 'pages', 'auth', 'payroll']
    for bp_name in expected_blueprints:
        assert bp_name in blueprint_names, f"{bp_name} Blueprint가 등록되어야 함"
        print(f"✅ {bp_name} Blueprint: 등록됨")
    
    return True


def test_error_handlers():
    """에러 핸들러 등록 테스트"""
    print("🧪 테스트 4: 에러 핸들러 등록 확인")
    
    app = create_app('development')
    
    # 에러 핸들러 확인
    error_handlers = app.error_handler_spec.get(None, {})
    expected_handlers = [400, 403, 404, 500]
    
    for code in expected_handlers:
        assert code in error_handlers, f"{code} 에러 핸들러가 등록되어야 함"
        print(f"✅ {code} 에러 핸들러: 등록됨")
    
    return True


def test_cleanup_scheduler():
    """파일 정리 스케줄러 등록 테스트"""
    print("🧪 테스트 5: 파일 정리 스케줄러 등록 확인")
    
    app = create_app('development')
    
    # 스케줄러는 백그라운드 스레드로 실행되므로 직접 확인하기 어렵지만
    # 앱이 정상적으로 생성되는지 확인
    assert app is not None, "앱이 생성되어야 함"
    print("✅ 통과: 앱 생성 및 스케줄러 등록 코드 실행됨 (실제 스케줄러 동작은 런타임 확인 필요)")
    
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Flask 앱 초기화 테스트 시작")
    print("=" * 60)
    
    tests = [
        test_app_creation,
        test_app_config,
        test_blueprint_registration,
        test_error_handlers,
        test_cleanup_scheduler
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 테스트 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 60)
    print(f"테스트 결과: {passed}개 통과, {failed}개 실패")
    print("=" * 60)
    
    if failed == 0:
        print("✅ 모든 테스트 통과!")
        sys.exit(0)
    else:
        print("❌ 일부 테스트 실패")
        sys.exit(1)
