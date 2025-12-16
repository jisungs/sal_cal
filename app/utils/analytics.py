#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analytics 유틸리티 - 데이터 수집 및 로깅"""

from app import db
from app.models.activity import UserActivity
from app.models.payroll import PayrollCalculation
from app.models.file_generation import FileGeneration
from flask import request, current_app
from datetime import datetime


def log_activity(user_id, activity_type, activity_data=None, request_path=None, request_method=None):
    """
    사용자 활동 로그 저장
    
    Args:
        user_id: 사용자 ID (None 가능 - 비로그인 사용자)
        activity_type: 활동 유형 ('page_view', 'button_click', 'form_submit', 'file_upload', 'file_download' 등)
        activity_data: 상세 정보 (딕셔너리)
        request_path: 요청 경로
        request_method: 요청 메서드 (GET, POST 등)
    """
    try:
        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            activity_data=activity_data or {},
            ip_address=request.remote_addr if request else None,
            user_agent=request.headers.get('User-Agent') if request else None,
            request_path=request_path or (request.path if request else None),
            request_method=request_method or (request.method if request else None)
        )
        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f'활동 로그 저장 오류: {str(e)}')
        db.session.rollback()


def log_payroll_calculation(user_id, calculation_data):
    """
    급여 계산 결과 저장
    
    Args:
        user_id: 사용자 ID (None 가능)
        calculation_data: 계산 결과 딕셔너리
            - employee_count: 직원 수
            - period: 급여 기간
            - results: 각 직원별 계산 결과 리스트
            - total_payroll: 총 지급액 합계
            - total_deductions: 총 공제액 합계
            - total_net_pay: 총 실수령액 합계
    """
    try:
        calculation = PayrollCalculation(
            user_id=user_id,
            employee_count=calculation_data.get('employee_count', 0),
            period=calculation_data.get('period'),
            total_payroll=calculation_data.get('total_payroll', 0),
            total_deductions=calculation_data.get('total_deductions', 0),
            total_net_pay=calculation_data.get('total_net_pay', 0),
            calculation_data=calculation_data
        )
        db.session.add(calculation)
        db.session.commit()
        return calculation
    except Exception as e:
        current_app.logger.error(f'급여 계산 결과 저장 오류: {str(e)}')
        db.session.rollback()
        return None


def log_file_generation(user_id, file_type, file_name, file_size=0, employee_count=0, period=None, file_path=None):
    """
    파일 생성 로그 저장
    
    Args:
        user_id: 사용자 ID (None 가능)
        file_type: 파일 유형 ('excel', 'pdf', 'zip')
        file_name: 파일명
        file_size: 파일 크기 (bytes)
        employee_count: 포함된 직원 수
        period: 급여 기간
        file_path: 파일 경로 (선택사항)
    """
    try:
        file_gen = FileGeneration(
            user_id=user_id,
            file_type=file_type,
            file_name=file_name,
            file_size=file_size,
            file_path=file_path,
            employee_count=employee_count,
            period=period,
            ip_address=request.remote_addr if request else None,
            user_agent=request.headers.get('User-Agent') if request else None
        )
        db.session.add(file_gen)
        db.session.commit()
        return file_gen
    except Exception as e:
        current_app.logger.error(f'파일 생성 로그 저장 오류: {str(e)}')
        db.session.rollback()
        return None


def calculate_totals_from_results(results):
    """
    계산 결과 리스트에서 집계 데이터 계산
    
    Args:
        results: 각 직원별 계산 결과 리스트
            각 항목은 {'payroll_data': {...}} 형태
        
    Returns:
        dict: 집계 데이터
            - total_payroll: 총 지급액 합계
            - total_deductions: 총 공제액 합계
            - total_net_pay: 총 실수령액 합계
    """
    total_payroll = 0
    total_deductions = 0
    total_net_pay = 0
    
    for result in results:
        payroll_data = result.get('payroll_data', {})
        if isinstance(payroll_data, dict):
            # 총 지급액
            total_payment = payroll_data.get('총지급액', 0)
            if isinstance(total_payment, (int, float)):
                total_payroll += total_payment
            
            # 총 공제액
            total_deduction = payroll_data.get('총공제액', 0)
            if isinstance(total_deduction, (int, float)):
                total_deductions += total_deduction
            
            # 실수령액
            net_pay = payroll_data.get('실수령액', 0)
            if isinstance(net_pay, (int, float)):
                total_net_pay += net_pay
    
    return {
        'total_payroll': total_payroll,
        'total_deductions': total_deductions,
        'total_net_pay': total_net_pay
    }

