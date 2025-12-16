#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""파일 정리 유틸리티 - 오래된 파일 자동 삭제"""

import os
import time
import glob
from pathlib import Path
from datetime import datetime, timedelta
from flask import current_app


def cleanup_old_files(upload_folder=None, output_folder=None, max_age_hours=24):
    """
    오래된 파일을 삭제하는 함수
    
    Args:
        upload_folder: 업로드 폴더 경로 (None이면 설정에서 가져옴)
        output_folder: 출력 폴더 경로 (None이면 설정에서 가져옴)
        max_age_hours: 파일 보관 시간 (시간 단위, 기본 24시간)
    
    Returns:
        dict: 삭제된 파일 정보
            - deleted_count: 삭제된 파일 수
            - deleted_files: 삭제된 파일 목록
            - total_size: 삭제된 파일 총 크기 (bytes)
    """
    try:
        # Flask 앱 컨텍스트가 없으면 설정에서 직접 가져오기
        if upload_folder is None:
            try:
                upload_folder = current_app.config.get('UPLOAD_FOLDER')
            except RuntimeError:
                # 앱 컨텍스트 외부에서는 기본 경로 사용
                upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'web', 'uploads')
        
        if output_folder is None:
            try:
                output_folder = current_app.config.get('OUTPUT_FOLDER')
            except RuntimeError:
                output_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'outputs')
        
        deleted_count = 0
        deleted_files = []
        total_size = 0
        cutoff_time = time.time() - (max_age_hours * 3600)  # 초 단위로 변환
        
        # 업로드 폴더 정리
        if os.path.exists(upload_folder):
            for file_path in glob.glob(os.path.join(upload_folder, '*')):
                if os.path.isfile(file_path):
                    file_mtime = os.path.getmtime(file_path)
                    if file_mtime < cutoff_time:
                        try:
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            deleted_count += 1
                            deleted_files.append(file_path)
                            total_size += file_size
                        except OSError as e:
                            # 삭제 실패 시 로그만 기록하고 계속 진행
                            try:
                                if current_app:
                                    current_app.logger.warning(f"파일 삭제 실패: {file_path} - {str(e)}")
                            except RuntimeError:
                                # 앱 컨텍스트가 없으면 무시
                                pass
        
        # 출력 폴더의 임시 파일 정리 (ZIP 파일 등)
        if os.path.exists(output_folder):
            # 임시 ZIP 파일 찾기 (일반적으로 outputs 폴더에 직접 생성되는 경우)
            for file_path in glob.glob(os.path.join(output_folder, '*.zip')):
                if os.path.isfile(file_path):
                    file_mtime = os.path.getmtime(file_path)
                    if file_mtime < cutoff_time:
                        try:
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            deleted_count += 1
                            deleted_files.append(file_path)
                            total_size += file_size
                        except OSError as e:
                            if current_app:
                                current_app.logger.warning(f"파일 삭제 실패: {file_path} - {str(e)}")
        
        return {
            'deleted_count': deleted_count,
            'deleted_files': deleted_files,
            'total_size': total_size,
            'cleanup_time': datetime.now().isoformat()
        }
    
    except Exception as e:
        # 에러 발생 시 로그 기록
        try:
            if current_app:
                current_app.logger.error(f"파일 정리 중 오류 발생: {str(e)}")
        except RuntimeError:
            # 앱 컨텍스트가 없으면 무시
            pass
        return {
            'deleted_count': 0,
            'deleted_files': [],
            'total_size': 0,
            'error': str(e),
            'cleanup_time': datetime.now().isoformat()
        }


def cleanup_temp_zip_files(output_folder=None, max_age_hours=1):
    """
    임시 ZIP 파일만 정리하는 함수 (더 짧은 시간)
    
    Args:
        output_folder: 출력 폴더 경로
        max_age_hours: 파일 보관 시간 (시간 단위, 기본 1시간)
    
    Returns:
        dict: 삭제된 파일 정보
    """
    try:
        if output_folder is None:
            try:
                output_folder = current_app.config.get('OUTPUT_FOLDER')
            except RuntimeError:
                output_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'outputs')
        
        deleted_count = 0
        deleted_files = []
        total_size = 0
        cutoff_time = time.time() - (max_age_hours * 3600)
        
        if os.path.exists(output_folder):
            for file_path in glob.glob(os.path.join(output_folder, '*.zip')):
                if os.path.isfile(file_path):
                    file_mtime = os.path.getmtime(file_path)
                    if file_mtime < cutoff_time:
                        try:
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            deleted_count += 1
                            deleted_files.append(file_path)
                            total_size += file_size
                        except OSError as e:
                            try:
                                if current_app:
                                    current_app.logger.warning(f"임시 파일 삭제 실패: {file_path} - {str(e)}")
                            except RuntimeError:
                                # 앱 컨텍스트가 없으면 무시
                                pass
        
        return {
            'deleted_count': deleted_count,
            'deleted_files': deleted_files,
            'total_size': total_size,
            'cleanup_time': datetime.now().isoformat()
        }
    
    except Exception as e:
        try:
            if current_app:
                current_app.logger.error(f"임시 파일 정리 중 오류 발생: {str(e)}")
        except RuntimeError:
            # 앱 컨텍스트가 없으면 무시
            pass
        return {
            'deleted_count': 0,
            'deleted_files': [],
            'total_size': 0,
            'error': str(e),
            'cleanup_time': datetime.now().isoformat()
        }
