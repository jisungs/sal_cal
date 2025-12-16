#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""인증 관련 폼 클래스"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User


class RegistrationForm(FlaskForm):
    """회원가입 폼"""
    email = StringField('이메일', 
                       validators=[DataRequired(message='이메일을 입력해주세요.'), 
                                  Email(message='올바른 이메일 형식이 아닙니다.')])
    username = StringField('사용자명', 
                           validators=[DataRequired(message='사용자명을 입력해주세요.'), 
                                      Length(min=2, max=20, message='사용자명은 2-20자 사이여야 합니다.')])
    password = PasswordField('비밀번호', 
                             validators=[DataRequired(message='비밀번호를 입력해주세요.'), 
                                        Length(min=6, message='비밀번호는 최소 6자 이상이어야 합니다.')])
    password2 = PasswordField('비밀번호 확인', 
                             validators=[DataRequired(message='비밀번호 확인을 입력해주세요.'), 
                                        EqualTo('password', message='비밀번호가 일치하지 않습니다.')])
    submit = SubmitField('회원가입')
    
    def validate_email(self, email):
        """이메일 중복 검증"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('이미 사용 중인 이메일입니다.')


class LoginForm(FlaskForm):
    """로그인 폼"""
    email = StringField('이메일', 
                       validators=[DataRequired(message='이메일을 입력해주세요.'), 
                                  Email(message='올바른 이메일 형식이 아닙니다.')])
    password = PasswordField('비밀번호', 
                             validators=[DataRequired(message='비밀번호를 입력해주세요.')])
    remember_me = BooleanField('로그인 상태 유지')
    submit = SubmitField('로그인')


class ResetPasswordRequestForm(FlaskForm):
    """비밀번호 재설정 요청 폼"""
    email = StringField('이메일', 
                       validators=[DataRequired(message='이메일을 입력해주세요.'), 
                                  Email(message='올바른 이메일 형식이 아닙니다.')])
    submit = SubmitField('재설정 링크 전송')


class ResetPasswordForm(FlaskForm):
    """비밀번호 재설정 폼"""
    password = PasswordField('새 비밀번호', 
                           validators=[DataRequired(message='비밀번호를 입력해주세요.'), 
                                      Length(min=6, message='비밀번호는 최소 6자 이상이어야 합니다.')])
    password2 = PasswordField('비밀번호 확인', 
                             validators=[DataRequired(message='비밀번호 확인을 입력해주세요.'), 
                                        EqualTo('password', message='비밀번호가 일치하지 않습니다.')])
    submit = SubmitField('비밀번호 변경')

