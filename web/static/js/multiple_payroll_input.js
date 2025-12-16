// 다중 직원 입력 폼 관리
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('employeesContainer');
    const addBtn = document.getElementById('addEmployeeBtn');
    const template = document.getElementById('employeeTemplate');
    let employeeCount = 1; // 첫 번째 직원은 이미 있음
    
    if (!container || !addBtn || !template) {
        return;
    }
    
    // 직원 추가 버튼 클릭 이벤트
    addBtn.addEventListener('click', function() {
        addEmployeeForm();
    });
    
    // 삭제 버튼 이벤트 위임
    container.addEventListener('click', function(e) {
        if (e.target.closest('.remove-employee-btn')) {
            const employeeForm = e.target.closest('.employee-form');
            if (employeeForm) {
                removeEmployeeForm(employeeForm);
            }
        }
    });
    
    /**
     * 직원 폼 추가
     */
    function addEmployeeForm() {
        employeeCount++;
        const clone = template.content.cloneNode(true);
        const employeeForm = clone.querySelector('.employee-form');
        
        // 인덱스 설정
        employeeForm.setAttribute('data-employee-index', employeeCount - 1);
        
        // 직원 번호 업데이트
        employeeForm.querySelector('.employee-number').textContent = employeeCount;
        
        // 모든 입력 필드의 name 속성 업데이트
        const inputs = employeeForm.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            const name = input.getAttribute('name');
            if (name) {
                // employees[][field] -> employees[index][field]
                const newName = name.replace(/employees\[\]/, `employees[${employeeCount - 1}]`);
                input.setAttribute('name', newName);
            }
        });
        
        // 삭제 버튼 활성화
        const removeBtn = employeeForm.querySelector('.remove-employee-btn');
        if (removeBtn) {
            removeBtn.disabled = false;
        }
        
        // 컨테이너에 추가
        container.appendChild(employeeForm);
        
        // 스크롤을 새로 추가된 폼으로 이동
        employeeForm.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    /**
     * 직원 폼 제거
     */
    function removeEmployeeForm(employeeForm) {
        const forms = container.querySelectorAll('.employee-form');
        
        // 최소 1개는 유지
        if (forms.length <= 1) {
            alert('최소 1명의 직원 정보는 필요합니다.');
            return;
        }
        
        // 확인 대화상자
        if (!confirm('이 직원 정보를 삭제하시겠습니까?')) {
            return;
        }
        
        // 폼 제거
        employeeForm.remove();
        
        // 직원 번호 재정렬
        renumberEmployees();
    }
    
    /**
     * 직원 번호 재정렬
     */
    function renumberEmployees() {
        const forms = container.querySelectorAll('.employee-form');
        forms.forEach((form, index) => {
            const numberSpan = form.querySelector('.employee-number');
            if (numberSpan) {
                numberSpan.textContent = index + 1;
            }
            
            // 인덱스 업데이트
            form.setAttribute('data-employee-index', index);
            
            // name 속성 업데이트
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                const name = input.getAttribute('name');
                if (name && name.includes('employees[')) {
                    // employees[old_index][field] -> employees[new_index][field]
                    const newName = name.replace(/employees\[\d+\]/, `employees[${index}]`);
                    input.setAttribute('name', newName);
                }
            });
        });
        
        employeeCount = forms.length;
    }
    
    // 기본급 변경 시 연장근무단가 권장값 자동 계산 (이벤트 위임)
    container.addEventListener('input', function(e) {
        const target = e.target;
        if (target.classList.contains('employee-base-salary')) {
            const employeeForm = target.closest('.employee-form');
            if (employeeForm) {
                calculateRecommendedOvertimeRateForEmployee(employeeForm);
            }
        }
    });
    
    // 연장근무단가 필드 포커스 시 권장값 계산
    container.addEventListener('focus', function(e) {
        const target = e.target;
        if (target.classList.contains('employee-overtime-rate')) {
            const employeeForm = target.closest('.employee-form');
            if (employeeForm && (!target.value || target.value === '0')) {
                calculateRecommendedOvertimeRateForEmployee(employeeForm);
            }
        }
    }, true);
    
    /**
     * 특정 직원 폼의 연장근무단가 권장값 계산
     */
    function calculateRecommendedOvertimeRateForEmployee(employeeForm) {
        const baseSalaryField = employeeForm.querySelector('.employee-base-salary');
        const overtimeRateField = employeeForm.querySelector('.employee-overtime-rate');
        
        if (!baseSalaryField || !overtimeRateField) {
            return;
        }
        
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
            // 힌트 요소 찾기 또는 생성
            let hintElement = employeeForm.querySelector('.overtime-rate-hint');
            if (!hintElement) {
                hintElement = document.createElement('div');
                hintElement.className = 'form-text text-primary overtime-rate-hint';
                hintElement.style.cursor = 'pointer';
                overtimeRateField.parentElement.appendChild(hintElement);
            }
            
            hintElement.textContent = `💡 권장값: ${recommendedRate.toLocaleString()}원/시간 (기본급 기준 1.5배)`;
            hintElement.style.display = 'block';
            
            // 클릭 시 자동 입력
            hintElement.onclick = function() {
                overtimeRateField.value = recommendedRate;
                hintElement.style.display = 'none';
            };
        }
    }
    
    // 폼 제출 전 검증
    const form = document.getElementById('multiplePayrollForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const forms = container.querySelectorAll('.employee-form');
            
            // 최소 1명 확인
            if (forms.length === 0) {
                e.preventDefault();
                alert('최소 1명의 직원 정보를 입력해주세요.');
                return false;
            }
            
            // 각 직원의 필수 필드 검증
            let hasError = false;
            forms.forEach((form, index) => {
                const name = form.querySelector('.employee-name')?.value.trim();
                const residentNumber = form.querySelector('.employee-resident-number')?.value.trim();
                const hireDate = form.querySelector('.employee-hire-date')?.value;
                const baseSalary = form.querySelector('.employee-base-salary')?.value;
                
                if (!name || !residentNumber || !hireDate || !baseSalary) {
                    hasError = true;
                    form.classList.add('border-danger');
                    
                    // 에러 메시지 표시
                    if (!form.querySelector('.alert-danger')) {
                        const alert = document.createElement('div');
                        alert.className = 'alert alert-danger mt-2';
                        alert.textContent = `직원 ${index + 1}: 필수 정보를 모두 입력해주세요.`;
                        form.querySelector('.card-body').appendChild(alert);
                    }
                } else {
                    form.classList.remove('border-danger');
                    const alert = form.querySelector('.alert-danger');
                    if (alert) {
                        alert.remove();
                    }
                }
            });
            
            if (hasError) {
                e.preventDefault();
                alert('모든 직원의 필수 정보를 입력해주세요.');
                return false;
            }
        });
    }
});

