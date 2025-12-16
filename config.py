#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""설정 파일 - 개발/프로덕션 환경 분리"""

import os
from pathlib import Path

# 프로젝트 루트 경로
basedir = Path(__file__).parent.absolute()


class Config:
    """기본 설정 클래스"""
    # 보안 설정
    # SECRET_KEY는 환경 변수에서 가져오거나 기본값 사용
    # 프로덕션 환경에서는 반드시 환경 변수로 설정해야 함
    _secret_key = os.environ.get('SECRET_KEY')
    if not _secret_key:
        import warnings
        warnings.warn(
            'SECRET_KEY가 환경 변수로 설정되지 않았습니다. '
            '프로덕션 환경에서는 보안을 위해 반드시 환경 변수로 설정하세요.',
            UserWarning
        )
        SECRET_KEY = 'dev-secret-key-change-in-production'
    else:
        SECRET_KEY = _secret_key
    
    # 파일 업로드 설정
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(basedir, 'web', 'uploads')
    OUTPUT_FOLDER = os.path.join(basedir, 'outputs')
    
    # 허용된 파일 확장자
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Flask 설정
    TEMPLATE_FOLDER = os.path.join(basedir, 'web', 'templates')
    STATIC_FOLDER = os.path.join(basedir, 'web', 'static')
    
    # 세션 설정
    SESSION_COOKIE_SECURE = False  # HTTPS 사용 시 True로 변경
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24시간 (초 단위)
    
    # 데이터베이스 설정 (Phase 2에서 사용)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # 이메일 설정 (Phase 2 Day 4)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER 설정 (환경 변수 우선, 없으면 MAIL_USERNAME, 둘 다 없으면 기본값)
    _mail_default_sender = os.environ.get('MAIL_DEFAULT_SENDER')
    if _mail_default_sender:
        MAIL_DEFAULT_SENDER = _mail_default_sender
    elif MAIL_USERNAME:
        MAIL_DEFAULT_SENDER = MAIL_USERNAME
    else:
        MAIL_DEFAULT_SENDER = 'noreply@example.com'
    
    @staticmethod
    def init_app(app):
        """애플리케이션 초기화"""
        # 업로드 및 출력 폴더 생성
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.join(Config.OUTPUT_FOLDER, 'pdf'), exist_ok=True)
        os.makedirs(os.path.join(Config.OUTPUT_FOLDER, 'excel'), exist_ok=True)


class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    TESTING = False
    
    # 개발 환경에서는 SQLite 사용 (선택사항)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "app.db")}'


class ProductionConfig(Config):
    """프로덕션 환경 설정"""
    DEBUG = False
    TESTING = False
    
    # 프로덕션 환경에서는 PostgreSQL 사용 (Railway)
    # SQLALCHEMY_DATABASE_URI는 init_app()에서 동적으로 설정됨
    # (모듈 로드 시점이 아닌 런타임에 환경 변수 확인)
    SQLALCHEMY_DATABASE_URI = None
    
    # 보안 강화: 프로덕션 환경에서는 SECRET_KEY 필수
    # SECRET_KEY는 init_app()에서 동적으로 설정됨
    SECRET_KEY = None
    
    # 보안 강화
    SESSION_COOKIE_SECURE = True  # HTTPS 사용
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    @staticmethod
    def init_app(app):
        """애플리케이션 초기화 - SECRET_KEY 및 DATABASE_URI 동적 설정"""
        # 부모 클래스의 init_app 호출
        Config.init_app(app)
        
        # 프로덕션 환경에서 SECRET_KEY 필수 확인 및 설정
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            raise ValueError(
                '프로덕션 환경에서는 SECRET_KEY 환경 변수가 반드시 설정되어야 합니다. '
                '환경 변수를 설정하거나 .env 파일을 확인하세요.'
            )
        app.config['SECRET_KEY'] = secret_key
        
        # 프로덕션 환경에서 DATABASE_URL 필수 확인 및 설정
        db_uri = os.environ.get('DATABASE_URL') or \
                 os.environ.get('POSTGRES_URL')
        if not db_uri:
            raise ValueError(
                '프로덕션 환경에서는 DATABASE_URL 환경 변수가 반드시 설정되어야 합니다. '
                '환경 변수를 설정하거나 .env 파일을 확인하세요.'
            )
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


class TestingConfig(Config):
    """테스트 환경 설정"""
    TESTING = True
    DEBUG = True
    
    # 테스트용 인메모리 데이터베이스
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# 설정 딕셔너리
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

