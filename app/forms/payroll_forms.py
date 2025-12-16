#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""급여 입력 폼 - 웹 직접 입력 기능용"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp
from datetime import datetime


class EmployeeInputForm(FlaskForm):
    """직원 정보 입력 폼"""
    
    # 필수 필드
    name = StringField('이름', validators=[
        DataRequired(message='이름을 입력해주세요.'),
        Length(min=1, max=50, message='이름은 1-50자 사이여야 합니다.')
    ])
    
    resident_number = StringField('주민번호 앞자리', validators=[
        DataRequired(message='주민번호 앞자리를 입력해주세요.'),
        Regexp(r'^\d{6}$', message='주민번호 앞자리는 6자리 숫자여야 합니다.')
    ])
    
    hire_date = DateField('입사일', validators=[
        DataRequired(message='입사일을 입력해주세요.')
    ], format='%Y-%m-%d')
    
    base_salary = IntegerField('기본급 (원)', validators=[
        DataRequired(message='기본급을 입력해주세요.'),
        NumberRange(min=0, message='기본급은 0 이상이어야 합니다.')
    ])
    
    dependents = IntegerField('부양가족수', validators=[
        # DataRequired() 제거 - 0도 유효한 값이므로
        NumberRange(min=0, max=10, message='부양가족수는 0-10 사이여야 합니다.')
    ], default=0)
    
    # 소속/직급 필드 (템플릿 디자인용)
    department = StringField('소속', validators=[
        Optional(),
        Length(max=50, message='소속은 50자 이하여야 합니다.')
    ])
    
    position = StringField('직급', validators=[
        Optional(),
        Length(max=50, message='직급은 50자 이하여야 합니다.')
    ])
    
    # 선택 필드
    bank_name = StringField('은행명', validators=[
        Optional(),
        Length(max=50, message='은행명은 50자 이하여야 합니다.')
    ])
    
    account_number = StringField('계좌번호', validators=[
        Optional(),
        Length(max=50, message='계좌번호는 50자 이하여야 합니다.')
    ])
    
    overtime_hours = IntegerField('연장근무시간', validators=[
        Optional(),
        NumberRange(min=0, message='연장근무시간은 0 이상이어야 합니다.')
    ], default=0)
    
    overtime_rate = IntegerField('연장근무단가 (원/시간)', validators=[
        Optional(),
        NumberRange(min=0, message='연장근무단가는 0 이상이어야 합니다.')
    ], default=0)
    
    bonus = IntegerField('상여금 (원)', validators=[
        Optional(),
        NumberRange(min=0, message='상여금은 0 이상이어야 합니다.')
    ], default=0)
    
    deduction_note = TextAreaField('공제사항 메모', validators=[
        Optional(),
        Length(max=200, message='공제사항 메모는 200자 이하여야 합니다.')
    ])
    
    period = StringField('지급 기간', validators=[
        DataRequired(message='지급 기간을 입력해주세요.'),
        Regexp(r'^\d{4}-\d{2}$', message='지급 기간은 YYYY-MM 형식이어야 합니다.')
    ], default=lambda: datetime.now().strftime('%Y-%m'))
    
    output_format = StringField('출력 형식', validators=[
        DataRequired()
    ], default='both')
    
    design_name = StringField('디자인 선택', validators=[
        Optional()
    ], default='default')
    
    submit = SubmitField('급여명세서 생성')

