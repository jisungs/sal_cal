# calculator.py
try:
    from .config import (
        INSURANCE_RATES, 
        INSURANCE_LIMITS, 
        INCOME_TAX_TABLE, 
        LOCAL_TAX_RATE,
        DEPENDENT_DEDUCTION
    )
    from .logger import setup_logger
except ImportError:
    from config import (
        INSURANCE_RATES, 
        INSURANCE_LIMITS, 
        INCOME_TAX_TABLE, 
        LOCAL_TAX_RATE,
        DEPENDENT_DEDUCTION
    )
    from logger import setup_logger

logger = setup_logger()

class PayrollCalculator:
    def __init__(self):
        self.rates = INSURANCE_RATES
        self.limits = INSURANCE_LIMITS
    
    def calculate_insurance(self, base_salary, insurance_type):
        """4대보험 계산"""
        # 상한액 적용
        taxable_amount = min(base_salary, self.limits[insurance_type])
        return int(taxable_amount * self.rates[insurance_type])
    
    def calculate_income_tax(self, taxable_income):
        """소득세 계산 (간이세액표 기반)"""
        if taxable_income <= 0:
            return 0
        
        for start, end, rate, deduction in INCOME_TAX_TABLE:
            if start <= taxable_income < end:
                income_tax = int(taxable_income * rate - deduction)
                return max(0, income_tax)  # 음수 방지
        
        # 마지막 구간 (15,000,000 이상)
        return int(taxable_income * 0.38 - 1_940_000)
    
    def calculate_deductions(self, employee_data):
        """전체 공제액 계산"""
        base_salary = employee_data.get('기본급', 0)
        overtime_hours = employee_data.get('연장근무시간', 0)
        overtime_rate = employee_data.get('연장근무단가', 0)
        bonus = employee_data.get('상여금', 0)
        dependents = employee_data.get('부양가족수', 0)
        
        # 연장근무수당 계산
        overtime_pay = overtime_hours * overtime_rate if overtime_rate > 0 else 0
        
        # 총 지급액
        total_payment = base_salary + overtime_pay + bonus
        
        # 4대보험 계산 (기본급 기준)
        national_pension = self.calculate_insurance(base_salary, 'national_pension')
        health_insurance = self.calculate_insurance(base_salary, 'health_insurance')
        long_term_care = int(health_insurance * 0.1295)  # 건강보험의 12.95%
        employment_insurance = self.calculate_insurance(base_salary, 'employment_insurance')
        
        # 부양가족 공제액 계산
        dependent_deduction = DEPENDENT_DEDUCTION.get(min(dependents, 4), 600_000)
        
        # 소득세 계산 (과세표준 = 총 지급액 - 4대보험 - 부양가족공제)
        taxable_income = total_payment - (national_pension + health_insurance + 
                                          long_term_care + employment_insurance) - dependent_deduction
        income_tax = self.calculate_income_tax(max(0, taxable_income))
        local_tax = int(income_tax * LOCAL_TAX_RATE)
        
        total_deduction = (national_pension + health_insurance + long_term_care + 
                          employment_insurance + income_tax + local_tax)
        
        return {
            '기본급': base_salary,
            '연장근무수당': overtime_pay,
            '상여금': bonus,
            '총지급액': total_payment,
            '국민연금': national_pension,
            '건강보험': health_insurance,
            '장기요양': long_term_care,
            '고용보험': employment_insurance,
            '부양가족공제': dependent_deduction,
            '소득세': income_tax,
            '지방소득세': local_tax,
            '총공제액': total_deduction,
            '실수령액': total_payment - total_deduction
        }
    
    def calculate_net_pay(self, employee_data):
        """실수령액 계산 (간편 메서드)"""
        result = self.calculate_deductions(employee_data)
        return result['실수령액']

