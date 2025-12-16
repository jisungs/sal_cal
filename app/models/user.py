#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""User 모델 - 사용자 인증 및 관리"""

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    """사용자 모델"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # 관계 (Phase 3, 4에서 사용)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    # activities는 UserActivity 모델에서 backref로 정의됨
    
    def set_password(self, password):
        """비밀번호 설정 (해싱)"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """비밀번호 확인"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def get_reset_token(self, expires_in=3600):
        """
        비밀번호 재설정 토큰 생성
        
        Args:
            expires_in: 토큰 유효 시간 (초), 기본 1시간
            
        Returns:
            str: 토큰 문자열
        """
        from app.utils.email import generate_reset_token
        return generate_reset_token(self.email)
    
    @staticmethod
    def verify_reset_token(token):
        """
        비밀번호 재설정 토큰 검증 (정적 메서드)
        
        Args:
            token: 토큰 문자열
            
        Returns:
            User: 사용자 객체 (성공 시), None (실패 시)
        """
        from app.utils.email import verify_reset_token
        email = verify_reset_token(token)
        if email:
            return User.query.filter_by(email=email).first()
        return None
    
    def __repr__(self):
        return f'<User {self.email}>'

