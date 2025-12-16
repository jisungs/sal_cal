# Sample 엑셀 템플릿 분석 보고서

**작성일**: 2025-12-12  
**분석 대상**: 
- `sample/급여명세서_template.xlsx` (템플릿 1)
- `sample/임금명세서양식_template3.xlsx` (템플릿 2)

---

## 📋 목차

1. [템플릿 개요](#템플릿-개요)
2. [급여명세서 템플릿 분석](#급여명세서-템플릿-분석)
3. [임금명세서 템플릿 분석](#임금명세서-템플릿-분석)
4. [셀 매핑 비교](#셀-매핑-비교)
5. [공통 구조 및 차이점](#공통-구조-및-차이점)
6. [데이터 매핑 현황](#데이터-매핑-현황)
7. [개선 제안](#개선-제안)

---

## 템플릿 개요

### 1. 급여명세서 템플릿 (`급여명세서_template.xlsx`)

**용도**: 급여명세서 작성용 템플릿  
**대상**: `TemplateSample1` 클래스에서 사용  
**매핑 파일**: `payroll_generator/templates/designs/configs/template_sample1_mapping.json`

### 2. 임금명세서 템플릿 (`임금명세서양식_template3.xlsx`)

**용도**: 임금명세서 작성용 템플릿  
**대상**: `TemplateSample2` 클래스에서 사용  
**매핑 파일**: `payroll_generator/templates/designs/configs/template_sample2_mapping.json`  
**참고 문서**: `sample/임금명세서작성방법.md`

---

## 급여명세서 템플릿 분석

### 현재 매핑 정보

**파일**: `payroll_generator/templates/designs/configs/template_sample1_mapping.json`

```json
{
  "cell_mapping": {
    "period": "A2",              // 지급 기간
    "employee_name": "B4",        // 직원 이름
    "resident_number": "B5",      // 주민번호
    "join_date": "B6",           // 입사일
    "basic_salary": "B9",         // 기본급
    "overtime": "B10",            // 연장근무수당
    "bonus": "B11",               // 상여금
    "total_payment": "B12",       // 총지급액
    "national_pension": "B15",    // 국민연금
    "health_insurance": "B16",     // 건강보험
    "long_term_care": "B17",      // 장기요양보험
    "employment_insurance": "B18", // 고용보험
    "income_tax": "B19",          // 소득세
    "local_income_tax": "B20",    // 지방소득세
    "total_deduction": "B21",     // 총공제액
    "net_pay": "A23"              // 실수령액
  }
}
```

### 예상 구조

```
행 1: [헤더/제목]
행 2: [지급 기간] (A2)
행 3: [구분선 또는 빈 행]
행 4-6: [직원 정보]
  - B4: 이름
  - B5: 주민번호
  - B6: 입사일
행 7-8: [구분선 또는 빈 행]
행 9-12: [지급 항목]
  - B9: 기본급
  - B10: 연장근무수당
  - B11: 상여금
  - B12: 총지급액
행 13-14: [구분선 또는 빈 행]
행 15-21: [공제 항목]
  - B15: 국민연금
  - B16: 건강보험
  - B17: 장기요양보험
  - B18: 고용보험
  - B19: 소득세
  - B20: 지방소득세
  - B21: 총공제액
행 22: [구분선 또는 빈 행]
행 23: [실수령액] (A23)
```

### 특징

- **구조**: 간단하고 명확한 구조
- **레이아웃**: A열에 라벨, B열에 데이터
- **병합 셀**: 없음 (현재 매핑 기준)
- **수식**: 없음 (현재 매핑 기준)

---

## 임금명세서 템플릿 분석

### 현재 매핑 정보

**파일**: `payroll_generator/templates/designs/configs/template_sample2_mapping.json`

```json
{
  "cell_mapping": {
    "period": "A2",
    "employee_name": "B4",
    "resident_number": "B5",
    "join_date": "B6",
    "basic_salary": "B9",
    "overtime": "B10",
    "bonus": "B11",
    "total_payment": "B12",
    "national_pension": "B15",
    "health_insurance": "B16",
    "long_term_care": "B17",
    "employment_insurance": "B18",
    "income_tax": "B19",
    "local_income_tax": "B20",
    "total_deduction": "B21",
    "net_pay": "A23"
  }
}
```

### 예상 구조

급여명세서 템플릿과 동일한 구조로 추정됩니다.

### 특징

- **법적 요구사항**: 임금명세서는 근로기준법에 따라 작성
- **필수 항목**:
  - 임금 항목과 지급액
  - 공제 항목과 공제액
  - 계산 방법 (시간급·일급, 연장·야간·휴일근로수당 등)
- **선택 항목**:
  - 고정적으로 지급되는 항목은 계산 방법 생략 가능
  - 연장·야간·휴일근로수당은 계산 방법 명시 필수

### 법적 요구사항 (참고 문서 기준)

1. **임금 항목과 지급액**
   - 매월 지급하는 임금
   - 격월 또는 부정기적으로 지급하는 임금 (명절상여금, 하계휴가비 등)

2. **공제 항목과 공제액**
   - 법령이나 단체협약에 따른 공제 항목과 금액
   - 근로소득세율, 사회보험요율은 계산방법 생략 가능

3. **계산 방법**
   - 시간급·일급, 연장·야간·휴일근로수당 등은 계산방법 작성 필수
   - 예: `18일(근로일수)x7,000원`
   - 예: `연장근로수당 288,000원 = 16시간 X 12,000원 X 1.5`

4. **연장·야간·휴일근로수당**
   - 실제 근로한 시간 수, 통상시급, 가산율 명시
   - 휴일근로수당은 하루 8시간 기준으로 가산율 달리 기재

---

## 셀 매핑 비교

### 공통 매핑

두 템플릿 모두 동일한 셀 매핑을 사용하고 있습니다:

| 항목 | 셀 주소 | 설명 |
|------|---------|------|
| period | A2 | 지급 기간 |
| employee_name | B4 | 직원 이름 |
| resident_number | B5 | 주민번호 |
| join_date | B6 | 입사일 |
| basic_salary | B9 | 기본급 |
| overtime | B10 | 연장근무수당 |
| bonus | B11 | 상여금 |
| total_payment | B12 | 총지급액 |
| national_pension | B15 | 국민연금 |
| health_insurance | B16 | 건강보험 |
| long_term_care | B17 | 장기요양보험 |
| employment_insurance | B18 | 고용보험 |
| income_tax | B19 | 소득세 |
| local_income_tax | B20 | 지방소득세 |
| total_deduction | B21 | 총공제액 |
| net_pay | A23 | 실수령액 |

### 차이점

현재 매핑 파일 기준으로는 **차이점이 없습니다**.  
이는 다음 중 하나일 수 있습니다:

1. 실제 템플릿 파일이 동일한 구조
2. 매핑이 아직 정확히 분석되지 않음
3. 기본 매핑만 설정되어 있음

---

## 공통 구조 및 차이점

### 공통점

1. **레이아웃 구조**
   - A열: 라벨/제목
   - B열: 데이터 값
   - 동일한 행 구조 (직원 정보 → 지급 항목 → 공제 항목 → 실수령액)

2. **데이터 항목**
   - 동일한 필드 사용
   - 동일한 셀 위치

3. **구조적 특징**
   - 병합 셀 없음 (현재 매핑 기준)
   - 수식 없음 (현재 매핑 기준)

### 차이점 (예상)

1. **법적 요구사항**
   - **임금명세서**: 계산 방법 명시 필수
   - **급여명세서**: 계산 방법 명시 선택사항

2. **추가 필드 가능성**
   - 임금명세서에 계산 방법 필드가 추가로 있을 수 있음
   - 예: 연장근로수당 계산 방법 (`16시간 X 12,000원 X 1.5`)

3. **레이아웃 세부사항**
   - 제목, 헤더 스타일 차이
   - 구분선, 테두리 스타일 차이

---

## 데이터 매핑 현황

### 현재 상태

**문제점**:
- 두 템플릿의 매핑이 동일함
- 실제 템플릿 파일 분석이 완료되지 않음
- 매핑 파일에 "기본 매핑입니다. 실제 템플릿 파일을 분석하여 수정이 필요할 수 있습니다." 메모 있음

### 매핑된 필드

#### 직원 정보
- ✅ 이름 (`employee_name`)
- ✅ 주민번호 (`resident_number`)
- ✅ 입사일 (`join_date`)

#### 지급 항목
- ✅ 기본급 (`basic_salary`)
- ✅ 연장근무수당 (`overtime`)
- ✅ 상여금 (`bonus`)
- ✅ 총지급액 (`total_payment`)

#### 공제 항목
- ✅ 국민연금 (`national_pension`)
- ✅ 건강보험 (`health_insurance`)
- ✅ 장기요양보험 (`long_term_care`)
- ✅ 고용보험 (`employment_insurance`)
- ✅ 소득세 (`income_tax`)
- ✅ 지방소득세 (`local_income_tax`)
- ✅ 총공제액 (`total_deduction`)

#### 최종 항목
- ✅ 실수령액 (`net_pay`)

### 누락 가능한 필드

#### 임금명세서 특화 필드
- ❓ 계산 방법 필드 (연장근로수당 계산 방법 등)
- ❓ 은행명 (`bank_name`)
- ❓ 계좌번호 (`account_number`)
- ❓ 부양가족수 (`dependents`)
- ❓ 공제사항 메모 (`deduction_note`)

---

## 개선 제안

### 1. 실제 템플릿 파일 분석 필요

**작업**:
1. `openpyxl` 설치 후 `scripts/analyze_template_cells.py` 실행
2. 실제 셀 구조 확인
3. 병합 셀, 수식 확인
4. 매핑 파일 업데이트

**명령어**:
```bash
# openpyxl 설치
pip install openpyxl

# 템플릿 분석
python scripts/analyze_template_cells.py sample/급여명세서_template.xlsx \
  payroll_generator/templates/designs/configs/template_sample1_mapping.json

python scripts/analyze_template_cells.py sample/임금명세서양식_template3.xlsx \
  payroll_generator/templates/designs/configs/template_sample2_mapping.json
```

### 2. 추가 필드 매핑

**제안 필드**:
- `bank_name`: 은행명
- `account_number`: 계좌번호
- `dependents`: 부양가족수
- `deduction_note`: 공제사항 메모
- `overtime_calculation`: 연장근로수당 계산 방법 (임금명세서용)

### 3. 임금명세서 특화 기능

**계산 방법 필드 추가**:
- 연장근로수당 계산 방법 자동 생성
- 예: `16시간 X 12,000원 X 1.5 = 288,000원`

**구현 예시**:
```python
def generate_overtime_calculation(self, overtime_hours, overtime_rate):
    """연장근로수당 계산 방법 문자열 생성"""
    if overtime_hours > 0 and overtime_rate > 0:
        # 가산율 1.5 (연장근로)
        total = overtime_hours * overtime_rate * 1.5
        return f"{overtime_hours}시간 X {overtime_rate:,}원 X 1.5 = {total:,.0f}원"
    return ""
```

### 4. 매핑 검증 스크립트

**목적**: 생성된 파일이 템플릿 구조와 일치하는지 검증

**기능**:
- 매핑된 셀에 데이터가 올바르게 채워졌는지 확인
- 필수 필드 누락 확인
- 데이터 형식 검증 (숫자, 날짜 등)

### 5. 템플릿 미리보기 기능

**목적**: 사용자가 템플릿을 선택하기 전에 미리보기 제공

**구현**:
- 템플릿 파일의 스크린샷 생성
- 또는 템플릿 구조를 HTML로 렌더링

---

## 결론

### 현재 상태

1. **매핑 파일 존재**: 두 템플릿 모두 기본 매핑 파일이 있음
2. **구조 동일**: 현재 매핑 기준으로 두 템플릿의 구조가 동일함
3. **분석 필요**: 실제 템플릿 파일 분석이 완료되지 않음

### 다음 단계

1. **즉시 작업**:
   - `openpyxl` 설치
   - 실제 템플릿 파일 분석
   - 매핑 파일 업데이트

2. **단기 작업**:
   - 추가 필드 매핑 (은행명, 계좌번호 등)
   - 임금명세서 계산 방법 필드 추가

3. **중기 작업**:
   - 매핑 검증 스크립트 개발
   - 템플릿 미리보기 기능 추가

---

## 참고 자료

- `scripts/analyze_template_cells.py`: 템플릿 분석 스크립트
- `payroll_generator/templates/designs/configs/template_sample1_mapping.json`: 템플릿 1 매핑
- `payroll_generator/templates/designs/configs/template_sample2_mapping.json`: 템플릿 2 매핑
- `sample/임금명세서작성방법.md`: 임금명세서 작성 가이드
- `payroll_generator/templates/designs/template_sample1.py`: 템플릿 1 구현
- `payroll_generator/templates/designs/template_sample2.py`: 템플릿 2 구현
