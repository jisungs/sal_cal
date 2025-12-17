#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""인증 라우트 Blueprint - 로그인, 회원가입, 비밀번호 재설정"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models.user import User
from app.forms.auth_forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.utils.email import send_password_reset_email
from datetime import datetime

# Blueprint 생성
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """회원가입"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # 사용자 생성
            user = User(
                email=form.email.data,
                username=form.username.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash('회원가입이 완료되었습니다. 로그인해주세요.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f'회원가입 오류: {str(e)}')
            # 데이터베이스 연결 오류인지 확인
            if 'relation "users" does not exist' in str(e) or 'no such table: users' in str(e):
                flash('데이터베이스 테이블이 생성되지 않았습니다. 관리자에게 문의하세요.', 'danger')
            elif 'could not connect' in str(e).lower() or 'connection' in str(e).lower():
                flash('데이터베이스 연결에 실패했습니다. 잠시 후 다시 시도해주세요.', 'danger')
            else:
                flash('회원가입 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.', 'danger')
    
    return render_template('auth/register.html', form=form, title='회원가입')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """로그인"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # 사용자 조회
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                if not user.is_active:
                    flash('계정이 비활성화되었습니다. 관리자에게 문의하세요.', 'danger')
                    return redirect(url_for('auth.login'))
                
                # 로그인 처리
                login_user(user, remember=form.remember_me.data)
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # 다음 페이지로 리다이렉트
                next_page = request.args.get('next')
                if not next_page or not next_page.startswith('/'):
                    next_page = url_for('main.index')
                
                flash(f'{user.username}님, 환영합니다!', 'success')
                return redirect(next_page)
            else:
                flash('이메일 또는 비밀번호가 올바르지 않습니다.', 'danger')
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(f'로그인 오류: {str(e)}')
            if 'relation "users" does not exist' in str(e) or 'no such table: users' in str(e):
                flash('데이터베이스 테이블이 생성되지 않았습니다. 관리자에게 문의하세요.', 'danger')
            elif 'could not connect' in str(e).lower() or 'connection' in str(e).lower():
                flash('데이터베이스 연결에 실패했습니다. 잠시 후 다시 시도해주세요.', 'danger')
            else:
                flash('로그인 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.', 'danger')
    
    return render_template('auth/login.html', form=form, title='로그인')


@auth_bp.route('/logout')
@login_required
def logout():
    """로그아웃"""
    username = current_user.username
    logout_user()
    flash(f'{username}님, 로그아웃되었습니다.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """비밀번호 재설정 요청"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # 이메일 발송
            if send_password_reset_email(user):
                flash('비밀번호 재설정 링크가 이메일로 전송되었습니다. 이메일을 확인해주세요.', 'info')
            else:
                flash('이메일 발송 중 오류가 발생했습니다. 나중에 다시 시도해주세요.', 'danger')
        else:
            # 보안을 위해 사용자가 없어도 동일한 메시지 표시
            flash('비밀번호 재설정 링크가 이메일로 전송되었습니다. 이메일을 확인해주세요.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html', form=form, title='비밀번호 재설정')


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """비밀번호 재설정 (토큰 기반)"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # 토큰 검증
    user = User.verify_reset_token(token)
    if not user:
        flash('비밀번호 재설정 링크가 유효하지 않거나 만료되었습니다.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # 비밀번호 변경
        user.set_password(form.password.data)
        db.session.commit()
        
        flash('비밀번호가 성공적으로 변경되었습니다. 새로운 비밀번호로 로그인해주세요.', 'success')
        return redirect(url_for('auth.login'))
    
    # 토큰을 템플릿에 전달
    return render_template('auth/reset_password.html', form=form, token=token, title='비밀번호 재설정')

