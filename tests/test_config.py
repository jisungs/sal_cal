#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""설정 파일 테스트"""

import os
import sys

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import config, DevelopmentConfig, ProductionConfig


def test_development_config():
    """개발 환경 설정 테스트"""
    print("🧪 테스트 1: 개발 환경 설정")
    
    dev_config = DevelopmentConfig()
    
    # SECRET_KEY 확인
    assert dev_config.SECRET_KEY is not None, "SECRET_KEY가 설정되어야 함"
    print(f"✅ SECRET_KEY: {'설정됨' if dev_config.SECRET_KEY else '없음'}")
    
    # 세션 타임아웃 확인
    assert hasattr(dev_config, 'PERMANENT_SESSION_LIFETIME'), "PERMANENT_SESSION_LIFETIME이 설정되어야 함"
    assert dev_config.PERMANENT_SESSION_LIFETIME == 86400, f"예상: 86400초, 실제: {dev_config.PERMANENT_SESSION_LIFETIME}초"
    print(f"✅ PERMANENT_SESSION_LIFETIME: {dev_config.PERMANENT_SESSION_LIFETIME}초 (24시간)")
    
    # DEBUG 모드 확인
    assert dev_config.DEBUG == True, "개발 환경은 DEBUG=True여야 함"
    print("✅ DEBUG 모드: 활성화")
    
    return True


def test_production_config_without_secret_key():
    """프로덕션 환경 설정 테스트 (SECRET_KEY 없음)"""
    print("🧪 테스트 2: 프로덕션 환경 설정 (SECRET_KEY 없음)")
    
    # SECRET_KEY 환경 변수 제거
    original_secret = os.environ.get('SECRET_KEY')
    if 'SECRET_KEY' in os.environ:
        del os.environ['SECRET_KEY']
    
    # DATABASE_URL 설정 (SECRET_KEY 검증에 집중하기 위해)
    original_db_url = os.environ.get('DATABASE_URL')
    os.environ['DATABASE_URL'] = 'sqlite:///test_production.db'
    
    try:
        # Flask 앱 생성 시도 (init_app에서 에러 발생해야 함)
        from app import create_app
        app = create_app('production')
        print("❌ 실패: SECRET_KEY 없이도 앱이 생성됨 (에러가 발생해야 함)")
        return False
    except ValueError as e:
        # SECRET_KEY 관련 에러인지 확인
        if 'SECRET_KEY' in str(e):
            print(f"✅ 통과: SECRET_KEY 없이 ValueError 발생 (예상된 동작)")
            print(f"   에러 메시지: {str(e)}")
            return True
        else:
            print(f"❌ 예상치 못한 ValueError: {str(e)}")
            return False
    except Exception as e:
        # 다른 에러도 체크 (예: Flask 앱 생성 실패)
        if 'SECRET_KEY' in str(e):
            print(f"✅ 통과: SECRET_KEY 관련 에러 발생")
            print(f"   에러 메시지: {str(e)}")
            return True
        else:
            print(f"❌ 예상치 못한 에러: {str(e)}")
            return False
    finally:
        # 환경 변수 복원
        if original_secret:
            os.environ['SECRET_KEY'] = original_secret
        if original_db_url:
            os.environ['DATABASE_URL'] = original_db_url
        elif 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']


def test_production_config_with_secret_key():
    """프로덕션 환경 설정 테스트 (SECRET_KEY 있음)"""
    print("🧪 테스트 3: 프로덕션 환경 설정 (SECRET_KEY 있음)")
    
    # SECRET_KEY 설정
    test_secret = 'test-secret-key-for-production'
    os.environ['SECRET_KEY'] = test_secret
    
    # DATABASE_URL 설정 (테스트용 SQLite - 프로덕션 환경 테스트를 위해 필요)
    original_db_url = os.environ.get('DATABASE_URL')
    os.environ['DATABASE_URL'] = 'sqlite:///test_production.db'
    
    try:
        # Flask 앱 생성하여 실제 동작 확인
        from app import create_app
        app = create_app('production')
        
        # SECRET_KEY 확인 (app.config에서 확인)
        assert app.config['SECRET_KEY'] == test_secret, f"예상: {test_secret}, 실제: {app.config['SECRET_KEY']}"
        print(f"✅ SECRET_KEY: 정상 설정됨")
        
        # DEBUG 모드 확인
        assert app.config['DEBUG'] == False, "프로덕션 환경은 DEBUG=False여야 함"
        print("✅ DEBUG 모드: 비활성화")
        
        # 세션 쿠키 보안 설정 확인
        assert app.config['SESSION_COOKIE_SECURE'] == True, "프로덕션 환경은 SESSION_COOKIE_SECURE=True여야 함"
        print("✅ SESSION_COOKIE_SECURE: 활성화")
        
        return True
    finally:
        # 환경 변수 복원
        if 'SECRET_KEY' in os.environ:
            del os.environ['SECRET_KEY']
        if original_db_url:
            os.environ['DATABASE_URL'] = original_db_url
        elif 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']


def test_session_timeout():
    """세션 타임아웃 설정 테스트"""
    print("🧪 테스트 4: 세션 타임아웃 설정")
    
    dev_config = DevelopmentConfig()
    
    # 세션 타임아웃 확인
    assert dev_config.PERMANENT_SESSION_LIFETIME == 86400, "세션 타임아웃은 86400초(24시간)여야 함"
    print(f"✅ 세션 타임아웃: {dev_config.PERMANENT_SESSION_LIFETIME}초 (24시간)")
    
    # 세션 쿠키 설정 확인
    assert dev_config.SESSION_COOKIE_HTTPONLY == True, "SESSION_COOKIE_HTTPONLY는 True여야 함"
    assert dev_config.SESSION_COOKIE_SAMESITE == 'Lax', "SESSION_COOKIE_SAMESITE는 'Lax'여야 함"
    print("✅ 세션 쿠키 보안 설정: 정상")
    
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("설정 파일 테스트 시작")
    print("=" * 60)
    
    tests = [
        test_development_config,
        test_production_config_without_secret_key,
        test_production_config_with_secret_key,
        test_session_timeout
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
