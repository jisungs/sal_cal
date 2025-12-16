#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""파일 정리 기능 테스트"""

import os
import sys
import tempfile
import time
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.utils.cleanup import cleanup_old_files, cleanup_temp_zip_files


def test_cleanup_old_files():
    """오래된 파일 삭제 테스트"""
    print("🧪 테스트 1: 오래된 파일 삭제 기능")
    
    # 임시 디렉토리 생성
    with tempfile.TemporaryDirectory() as temp_dir:
        upload_folder = os.path.join(temp_dir, 'uploads')
        output_folder = os.path.join(temp_dir, 'outputs')
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)
        
        # 오래된 파일 생성 (25시간 전)
        old_file = os.path.join(upload_folder, 'old_file.txt')
        with open(old_file, 'w') as f:
            f.write('test')
        # 파일 수정 시간을 25시간 전으로 설정
        old_time = time.time() - (25 * 3600)
        os.utime(old_file, (old_time, old_time))
        
        # 최근 파일 생성 (1시간 전)
        recent_file = os.path.join(upload_folder, 'recent_file.txt')
        with open(recent_file, 'w') as f:
            f.write('test')
        recent_time = time.time() - (1 * 3600)
        os.utime(recent_file, (recent_time, recent_time))
        
        # 파일 정리 실행 (24시간 기준)
        result = cleanup_old_files(upload_folder=upload_folder, output_folder=output_folder, max_age_hours=24)
        
        # 검증
        assert result['deleted_count'] == 1, f"예상: 1개 삭제, 실제: {result['deleted_count']}개"
        assert os.path.exists(old_file) == False, "오래된 파일이 삭제되어야 함"
        assert os.path.exists(recent_file) == True, "최근 파일은 유지되어야 함"
        
        print("✅ 통과: 오래된 파일만 삭제됨")
        return True


def test_cleanup_temp_zip_files():
    """임시 ZIP 파일 정리 테스트"""
    print("🧪 테스트 2: 임시 ZIP 파일 정리 기능")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        output_folder = os.path.join(temp_dir, 'outputs')
        os.makedirs(output_folder, exist_ok=True)
        
        # 오래된 ZIP 파일 생성 (2시간 전)
        old_zip = os.path.join(output_folder, 'old.zip')
        with open(old_zip, 'w') as f:
            f.write('test')
        old_time = time.time() - (2 * 3600)
        os.utime(old_zip, (old_time, old_time))
        
        # 최근 ZIP 파일 생성 (30분 전)
        recent_zip = os.path.join(output_folder, 'recent.zip')
        with open(recent_zip, 'w') as f:
            f.write('test')
        recent_time = time.time() - (30 * 60)
        os.utime(recent_zip, (recent_time, recent_time))
        
        # 임시 ZIP 파일 정리 실행 (1시간 기준)
        result = cleanup_temp_zip_files(output_folder=output_folder, max_age_hours=1)
        
        # 검증
        assert result['deleted_count'] == 1, f"예상: 1개 삭제, 실제: {result['deleted_count']}개"
        assert os.path.exists(old_zip) == False, "오래된 ZIP 파일이 삭제되어야 함"
        assert os.path.exists(recent_zip) == True, "최근 ZIP 파일은 유지되어야 함"
        
        print("✅ 통과: 오래된 ZIP 파일만 삭제됨")
        return True


def test_cleanup_without_app_context():
    """앱 컨텍스트 없이 실행 테스트"""
    print("🧪 테스트 3: 앱 컨텍스트 없이 실행")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        upload_folder = os.path.join(temp_dir, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # 파일 생성
        test_file = os.path.join(upload_folder, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        # 앱 컨텍스트 없이 실행 (에러 없이 작동해야 함)
        try:
            result = cleanup_old_files(upload_folder=upload_folder, max_age_hours=0.001)  # 매우 짧은 시간
            print("✅ 통과: 앱 컨텍스트 없이도 정상 작동")
            return True
        except Exception as e:
            print(f"❌ 실패: {str(e)}")
            return False


def test_cleanup_error_handling():
    """에러 처리 테스트"""
    print("🧪 테스트 4: 에러 처리")
    
    # 존재하지 않는 폴더로 테스트
    result = cleanup_old_files(upload_folder='/nonexistent/path', output_folder='/nonexistent/path')
    
    # 에러가 발생해도 안전하게 처리되어야 함
    assert 'error' not in result or result.get('deleted_count', 0) == 0
    print("✅ 통과: 에러 발생 시 안전하게 처리됨")
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("파일 정리 기능 테스트 시작")
    print("=" * 60)
    
    tests = [
        test_cleanup_old_files,
        test_cleanup_temp_zip_files,
        test_cleanup_without_app_context,
        test_cleanup_error_handling
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
