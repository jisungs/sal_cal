// 실시간 계산 미리보기 및 자동 계산 기능
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('payrollForm');
    const previewArea = document.getElementById('previewArea');
    const previewContent = document.getElementById('previewContent');
    
    if (!form || !previewArea || !previewContent) {
        return; // 필수 요소가 없으면 종료
    }
    
    const fields = ['base_salary', 'overtime_hours', 'overtime_rate', 'bonus', 'dependents'];
    let previewTimeout;
    
    // 기본급 변경 시 연장근무단가 권장값 자동 계산
    const baseSalaryField = document.getElementById('base_salary');
    const overtimeRateField = document.getElementById('overtime_rate');
    
    if (baseSalaryField && overtimeRateField) {
        baseSalaryField.addEventListener('input', function() {
            calculateRecommendedOvertimeRate();
            clearTimeout(previewTimeout);
            previewTimeout = setTimeout(updatePreview, 500);
        });
        
        // 연장근무단가가 비어있을 때만 자동 계산
        overtimeRateField.addEventListener('focus', function() {
            if (!this.value || this.value === '0') {
                calculateRecommendedOvertimeRate();
            }
        });
    }
    
    fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', function() {
                clearTimeout(previewTimeout);
                previewTimeout = setTimeout(updatePreview, 500); // 500ms 디바운스
            });
        }
    });
    
    /**
     * 연장근무단가 권장값 자동 계산
     * 계산식: (기본급 / 20일 / 8시간) * 1.5
     */
    function calculateRecommendedOvertimeRate() {
        const baseSalary = parseInt(baseSalaryField.value) || 0;
        if (baseSalary <= 0) {
            return;
        }
        
        // 월 20일 근무, 일 8시간 기준
        const dailySalary = baseSalary / 20;
        const hourlyRate = dailySalary / 8;
        const recommendedRate = Math.round(hourlyRate * 1.5);
        
        // 연장근무단가가 비어있거나 0일 때만 제안
        if (!overtimeRateField.value || overtimeRateField.value === '0') {
            // 툴팁이나 힌트로 표시
            const hintElement = document.getElementById('overtime_rate_hint');
            if (hintElement) {
                hintElement.textContent = `💡 권장값: ${recommendedRate.toLocaleString()}원/시간 (기본급 기준 1.5배)`;
                hintElement.style.display = 'block';
                
                // 클릭 시 자동 입력
                hintElement.style.cursor = 'pointer';
                hintElement.style.color = '#0d6efd';
                hintElement.onclick = function() {
                    overtimeRateField.value = recommendedRate;
                    updatePreview();
                    hintElement.style.display = 'none';
                };
            }
        }
    }
    
    function updatePreview() {
        const baseSalaryField = document.getElementById('base_salary');
        if (!baseSalaryField) {
            return;
        }
        
        const data = {
            base_salary: parseInt(baseSalaryField.value) || 0,
            overtime_hours: parseInt(document.getElementById('overtime_hours')?.value) || 0,
            overtime_rate: parseInt(document.getElementById('overtime_rate')?.value) || 0,
            bonus: parseInt(document.getElementById('bonus')?.value) || 0,
            dependents: parseInt(document.getElementById('dependents')?.value) || 0
        };
        
        // 최소한 기본급이 있어야 미리보기 표시
        if (data.base_salary <= 0) {
            previewArea.classList.add('d-none');
            return;
        }
        
        fetch('/input/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success && result.payroll_data) {
                const pd = result.payroll_data;
                // 상세 계산 결과 표시
                const totalPayment = pd.총지급액 || 0;
                const totalDeduction = pd.총공제액 || 0;
                const netPay = pd.실수령액 || 0;
                
                previewContent.innerHTML = `
                    <div class="row">
                        <div class="col-md-6">
                            <h6 class="text-muted mb-2">💰 지급 내역</h6>
                            <div class="mb-2">
                                <small class="text-muted">기본급:</small> ${formatNumber(pd.기본급 || 0)}원
                            </div>
                            ${(pd.연장근무수당 || 0) > 0 ? `
                            <div class="mb-2">
                                <small class="text-muted">연장근무수당:</small> ${formatNumber(pd.연장근무수당 || 0)}원
                            </div>
                            ` : ''}
                            ${(pd.상여금 || 0) > 0 ? `
                            <div class="mb-2">
                                <small class="text-muted">상여금:</small> ${formatNumber(pd.상여금 || 0)}원
                            </div>
                            ` : ''}
                            <hr class="my-2">
                            <div class="mb-2">
                                <strong>총 지급액:</strong> <span class="text-success">${formatNumber(totalPayment)}원</span>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-muted mb-2">📋 공제 내역</h6>
                            <div class="mb-2">
                                <small class="text-muted">국민연금:</small> ${formatNumber(pd.국민연금 || 0)}원
                            </div>
                            <div class="mb-2">
                                <small class="text-muted">건강보험:</small> ${formatNumber(pd.건강보험 || 0)}원
                            </div>
                            <div class="mb-2">
                                <small class="text-muted">장기요양:</small> ${formatNumber(pd.장기요양 || 0)}원
                            </div>
                            <div class="mb-2">
                                <small class="text-muted">고용보험:</small> ${formatNumber(pd.고용보험 || 0)}원
                            </div>
                            <div class="mb-2">
                                <small class="text-muted">소득세:</small> ${formatNumber(pd.소득세 || 0)}원
                            </div>
                            <div class="mb-2">
                                <small class="text-muted">지방소득세:</small> ${formatNumber(pd.지방소득세 || 0)}원
                            </div>
                            <hr class="my-2">
                            <div class="mb-2">
                                <strong>총 공제액:</strong> <span class="text-danger">${formatNumber(totalDeduction)}원</span>
                            </div>
                        </div>
                    </div>
                    <hr class="my-3">
                    <div class="text-center">
                        <h5 class="mb-0">
                            <strong>실수령액:</strong> 
                            <span class="text-primary fs-3">${formatNumber(netPay)}원</span>
                        </h5>
                    </div>
                `;
                previewArea.classList.remove('d-none');
            } else {
                previewArea.classList.add('d-none');
            }
        })
        .catch(error => {
            console.error('미리보기 오류:', error);
            previewArea.classList.add('d-none');
        });
    }
    
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
    
    // 초기 로드 시 기본급이 있으면 권장값 계산
    if (baseSalaryField && baseSalaryField.value) {
        calculateRecommendedOvertimeRate();
    }
});

