#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PayrollCalculation 모델 - 급여 계산 결과 저장"""

from app import db
from datetime import datetime
import json


class PayrollCalculation(db.Model):
    """급여 계산 결과 모델"""
    __tablename__ = 'payroll_calculations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    # 기본 정보
    employee_count = db.Column(db.Integer, nullable=False, default=0)  # 처리된 직원 수
    period = db.Column(db.String(20), nullable=True, index=True)  # 급여 기간 (예: "2025-01")
    
    # 집계 데이터
    total_payroll = db.Column(db.Numeric(15, 2), default=0)  # 총 지급액 합계
    total_deductions = db.Column(db.Numeric(15, 2), default=0)  # 총 공제액 합계
    total_net_pay = db.Column(db.Numeric(15, 2), default=0)  # 총 실수령액 합계
    
    # 상세 계산 데이터 (JSON)
    calculation_data = db.Column(db.JSON)  # 전체 계산 결과 상세 정보
    
    # 메타데이터
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    user = db.relationship('User', backref='payroll_calculations', lazy=True)
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'employee_count': self.employee_count,
            'period': self.period,
            'total_payroll': float(self.total_payroll) if self.total_payroll else 0,
            'total_deductions': float(self.total_deductions) if self.total_deductions else 0,
            'total_net_pay': float(self.total_net_pay) if self.total_net_pay else 0,
            'calculation_data': self.calculation_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PayrollCalculation {self.id} - {self.employee_count}명 - {self.period}>'

