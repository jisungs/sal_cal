#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""에러 핸들러 테스트"""

import os
import sys

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app


def test_400_error_handler():
    """400 에러 핸들러 테스트"""
    print("🧪 테스트 1: 400 에러 핸들러")
    
    app = create_app('development')
    client = app.test_client()
    
    # 잘못된 요청으로 400 에러 발생 시도
    # 실제로는 JSON 요청이 필요하지만, 기본 동작 확인
    error_handlers = app.error_handler_spec.get(None, {})
    assert 400 in error_handlers, "400 에러 핸들러가 등록되어야 함"
    print("✅ 통과: 400 에러 핸들러 등록됨")
    
    return True


def test_403_error_handler():
    """403 에러 핸들러 테스트"""
    print("🧪 테스트 2: 403 에러 핸들러")
    
    app = create_app('development')
    error_handlers = app.error_handler_spec.get(None, {})
    assert 403 in error_handlers, "403 에러 핸들러가 등록되어야 함"
    print("✅ 통과: 403 에러 핸들러 등록됨")
    
    return True


def test_404_error_handler():
    """404 에러 핸들러 테스트"""
    print("🧪 테스트 3: 404 에러 핸들러")
    
    app = create_app('development')
    client = app.test_client()
    
    # 존재하지 않는 페이지 요청
    response = client.get('/nonexistent-page')
    assert response.status_code == 404, "404 상태 코드가 반환되어야 함"
    print("✅ 통과: 404 에러 핸들러 정상 작동")
    
    return True


def test_500_error_handler():
    """500 에러 핸들러 테스트"""
    print("🧪 테스트 4: 500 에러 핸들러")
    
    app = create_app('development')
    error_handlers = app.error_handler_spec.get(None, {})
    assert 500 in error_handlers, "500 에러 핸들러가 등록되어야 함"
    print("✅ 통과: 500 에러 핸들러 등록됨")
    
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("에러 핸들러 테스트 시작")
    print("=" * 60)
    
    tests = [
        test_400_error_handler,
        test_403_error_handler,
        test_404_error_handler,
        test_500_error_handler
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
