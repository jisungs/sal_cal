#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UserActivity 모델 - 사용자 활동 로그 저장"""

from app import db
from datetime import datetime
import json


class UserActivity(db.Model):
    """사용자 활동 로그 모델"""
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    # 활동 정보
    activity_type = db.Column(db.String(50), nullable=False, index=True)  # 'page_view', 'button_click', 'form_submit', 'file_upload', 'file_download' 등
    activity_data = db.Column(db.JSON)  # 상세 정보 (JSON)
    
    # 요청 정보
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    request_path = db.Column(db.String(500))  # 요청 경로
    request_method = db.Column(db.String(10))  # GET, POST 등
    
    # 메타데이터
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # 관계
    user = db.relationship('User', backref='activities', lazy=True)
    
    @property
    def data_dict(self):
        """activity_data를 딕셔너리로 변환"""
        if isinstance(self.activity_data, str):
            try:
                return json.loads(self.activity_data)
            except json.JSONDecodeError:
                return {}
        return self.activity_data or {}
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'activity_data': self.data_dict,
            'ip_address': self.ip_address,
            'request_path': self.request_path,
            'request_method': self.request_method,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<UserActivity {self.id} - {self.activity_type} - {self.created_at}>'

