#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FileGeneration 모델 - 파일 생성 로그 저장"""

from app import db
from datetime import datetime


class FileGeneration(db.Model):
    """파일 생성 로그 모델"""
    __tablename__ = 'file_generations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    # 파일 정보
    file_type = db.Column(db.String(20), nullable=False, index=True)  # 'excel', 'pdf', 'zip'
    file_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, default=0)  # 파일 크기 (bytes)
    file_path = db.Column(db.String(500))  # 저장 경로 (보안상 상세 경로는 저장하지 않을 수도 있음)
    
    # 생성 정보
    employee_count = db.Column(db.Integer, default=0)  # 포함된 직원 수
    period = db.Column(db.String(20), nullable=True, index=True)  # 급여 기간
    
    # 메타데이터
    ip_address = db.Column(db.String(45))  # 요청 IP
    user_agent = db.Column(db.Text)  # 사용자 에이전트
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # 관계
    user = db.relationship('User', backref='file_generations', lazy=True)
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'file_type': self.file_type,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'employee_count': self.employee_count,
            'period': self.period,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<FileGeneration {self.id} - {self.file_type} - {self.file_name}>'

