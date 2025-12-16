#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""모든 테스트 실행 스크립트"""

import os
import sys
import subprocess

def run_test(test_file):
    """테스트 파일 실행"""
    print(f"\n{'='*60}")
    print(f"실행 중: {test_file}")
    print('='*60)
    
    result = subprocess.run(
        [sys.executable, test_file],
        cwd=os.path.dirname(os.path.dirname(__file__)),
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode == 0


if __name__ == '__main__':
    print("=" * 60)
    print("전체 테스트 실행")
    print("=" * 60)
    
    test_files = [
        'tests/test_config.py',
        'tests/test_cleanup.py',
        'tests/test_app_init.py',
        'tests/test_error_handlers.py'
    ]
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        if os.path.exists(test_file):
            if run_test(test_file):
                passed += 1
            else:
                failed += 1
        else:
            print(f"⚠️  파일 없음: {test_file}")
    
    print("\n" + "=" * 60)
    print(f"전체 테스트 결과: {passed}개 통과, {failed}개 실패")
    print("=" * 60)
    
    if failed == 0:
        print("✅ 모든 테스트 통과!")
        sys.exit(0)
    else:
        print("❌ 일부 테스트 실패")
        sys.exit(1)
