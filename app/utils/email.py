#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""이메일 유틸리티 - 비밀번호 재설정 이메일 발송"""

from flask import render_template, current_app
from flask_mail import Message
from app import mail
from itsdangerous import URLSafeTimedSerializer


def generate_reset_token(email):
    """
    비밀번호 재설정 토큰 생성
    
    Args:
        email: 사용자 이메일
        
    Returns:
        str: 토큰 문자열
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')


def verify_reset_token(token, max_age=3600):
    """
    비밀번호 재설정 토큰 검증
    
    Args:
        token: 토큰 문자열
        max_age: 토큰 유효 시간 (초), 기본 1시간
        
    Returns:
        str: 이메일 주소 (성공 시), None (실패 시)
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=max_age)
        return email
    except Exception:
        return None


def send_password_reset_email(user):
    """
    비밀번호 재설정 이메일 발송
    
    Args:
        user: User 모델 인스턴스
        
    Returns:
        bool: 발송 성공 여부
    """
    try:
        token = generate_reset_token(user.email)
        reset_url = f"{current_app.config.get('BASE_URL', 'http://localhost:5001')}/auth/reset_password/{token}"
        
        # 발신자 설정
        sender = current_app.config.get('MAIL_DEFAULT_SENDER')
        if not sender:
            sender = current_app.config.get('MAIL_USERNAME') or 'noreply@example.com'
        
        msg = Message(
            subject='비밀번호 재설정 요청 - 급여명세서 자동생성기',
            recipients=[user.email],
            sender=sender,
            html=render_template('auth/email/reset_password.html', 
                               user=user, 
                               reset_url=reset_url,
                               token=token)
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f'이메일 발송 오류: {str(e)}')
        return False

