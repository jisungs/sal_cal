#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flask 애플리케이션 팩토리"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from config import config
import os

# 확장 초기화
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_name=None):
    """
    Flask 애플리케이션 팩토리 함수
    
    Args:
        config_name: 설정 이름 ('development', 'production', 'testing')
                    None이면 환경 변수 FLASK_ENV 사용
    """
    # 설정 이름 결정
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Flask 앱 생성
    app = Flask(__name__,
                template_folder=config[config_name].TEMPLATE_FOLDER,
                static_folder=config[config_name].STATIC_FOLDER)
    
    # 설정 로드
    app.config.from_object(config[config_name])
    
    # 설정 초기화 (init_app에서 SECRET_KEY 동적 설정)
    config[config_name].init_app(app)
    
    # 확장 초기화
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    # Flask-Login 설정
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '로그인이 필요합니다.'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
    
    @login_manager.user_loader
    def load_user(user_id):
        """사용자 로드 함수"""
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Blueprint 등록
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # 페이지 라우트 (About, Design, Contact)
    from app.routes.pages import pages_bp
    app.register_blueprint(pages_bp)
    
    # 인증 라우트 (Phase 2)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # 급여 직접 입력 라우트 (웹 직접 입력 기능)
    from app.routes.payroll import payroll_bp
    app.register_blueprint(payroll_bp)
    
    # Phase 3, 4, 5에서 추가될 Blueprint들 (주석 처리)
    # from app.routes.board import board_bp
    # app.register_blueprint(board_bp, url_prefix='/board')
    # 
    # from app.routes.api import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')
    
    # 에러 핸들러 등록
    from app.routes.main import register_error_handlers
    register_error_handlers(app)
    
    # 데이터베이스 연결 및 테이블 확인 (앱 시작 시)
    try:
        with app.app_context():
            # 데이터베이스 연결 테스트
            db.engine.connect()
            app.logger.info("데이터베이스 연결 성공")
            
            # users 테이블 존재 확인
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'users' not in tables:
                app.logger.warning("⚠️ 'users' 테이블이 존재하지 않습니다. 마이그레이션을 실행하세요: flask db upgrade")
            else:
                app.logger.info("✅ 데이터베이스 테이블 확인 완료")
    except Exception as e:
        app.logger.error(f"❌ 데이터베이스 연결 실패: {str(e)}")
        app.logger.error("DATABASE_URL 환경 변수를 확인하고 마이그레이션을 실행하세요: flask db upgrade")
    
    # 파일 정리 스케줄러 등록 (앱 시작 시)
    # Flask 2.2+에서는 @app.before_first_request가 deprecated되었으므로
    # 앱 컨텍스트 내에서 직접 실행
    try:
        import threading
        from app.utils.cleanup import cleanup_old_files
        
        def run_cleanup():
            """파일 정리 실행"""
            with app.app_context():
                try:
                    result = cleanup_old_files(max_age_hours=24)
                    app.logger.info(f"파일 정리 완료: {result['deleted_count']}개 파일 삭제, "
                                  f"총 {result['total_size'] / 1024 / 1024:.2f}MB")
                except Exception as e:
                    app.logger.error(f"파일 정리 중 오류 발생: {str(e)}")
        
        def schedule_cleanup():
            """주기적으로 파일 정리 실행 (6시간마다)"""
            run_cleanup()
            # 6시간 후 다시 실행
            timer = threading.Timer(21600, schedule_cleanup)  # 21600초 = 6시간
            timer.daemon = True
            timer.start()
        
        # 첫 실행은 1시간 후
        timer = threading.Timer(3600, schedule_cleanup)  # 3600초 = 1시간
        timer.daemon = True
        timer.start()
        app.logger.info("파일 정리 스케줄러가 등록되었습니다. (6시간마다 실행)")
    except Exception as e:
        app.logger.warning(f"파일 정리 스케줄러 등록 실패: {str(e)}")
    
    return app

