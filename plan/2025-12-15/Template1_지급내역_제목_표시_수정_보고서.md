# Template1 지급내역 제목 표시 수정 보고서

**작성일**: 2025-12-15  
**문제**: Template1로 생성된 급여명세서에서 지급내역 항목 제목이 누락됨  
**상태**: ✅ 완료  
**브랜치**: `fix/template1-payment-labels`

---

## 📋 문제 개요

### 발견된 문제

Template1로 생성된 급여명세서에서 지급내역 섹션의 항목 제목이 누락되어 있었습니다.

**템플릿 파일** (`sample/급여명세서_template.xlsx`):
- ✅ 모든 지급 항목의 제목이 있음 (기본급, 식대, 차량유지비, 직책수당, 근속수당, 연장수당, 당직수당, 상여금, 기타)

**생성된 급여명세서**:
- ❌ 지급 항목의 제목이 없고 숫자만 표시됨
- 예: "1,000,000"만 표시되고 "기본급" 제목이 없음

**요구사항**:
- "기본급 : 1,000,000원" 형식으로 제목과 값 함께 표시

---

## 🔍 원인 분석

### 문제 원인

1. **병합된 셀 구조**
   - 템플릿에서 지급 항목은 B열과 C열이 병합된 셀로 구성됨
   - 예: B7:C7 = "기본급" (제목), C7 = 값 셀

2. **기존 코드의 문제**
   - 기존 코드는 C열에 값만 채우고 있었음
   - 병합된 셀의 첫 번째 셀(B열)에 제목이 있었지만, C열에 값을 쓰면서 제목이 덮어써짐

3. **매핑 파일의 한계**
   - `template_sample1_mapping.json`에는 일부 지급 항목만 매핑되어 있음
   - 식대, 차량유지비, 직책수당, 근속수당, 당직수당, 기타 항목이 매핑에 없었음

---

## ✅ 해결 방법

### 1. 병합된 셀 처리 로직 개선

**파일**: `payroll_generator/templates/designs/template_design.py`

**변경 사항**:
- 지급 항목 처리 시 병합된 셀인지 확인
- 병합된 셀인 경우 첫 번째 셀(B열)에 제목과 값 함께 표시
- 형식: "제목 : 값원" (예: "기본급 : 1,000,000원")
- 값이 없으면 제목만 표시

**코드 변경**:
```python
# 지급 항목 매핑 (제목과 값 함께 표시)
payment_mapping = {
    'basic_salary': ('기본급', '기본급', 'payroll'),
    'meal_allowance': ('식대', '식대', 'employee'),
    'vehicle_maintenance': ('차량유지비', '차량유지비', 'employee'),
    'position_allowance': ('직책수당', '직책수당', 'employee'),
    'service_allowance': ('근속수당', '근속수당', 'employee'),
    'overtime': ('연장근무수당', '연장수당', 'payroll'),
    'oncall_allowance': ('당직수당', '당직수당', 'employee'),
    'bonus': ('상여금', '상여금', 'payroll'),
    'other': ('기타', '기타', 'employee'),
}

# 병합된 셀 확인 및 처리
for merged_range in ws.merged_cells.ranges:
    if merged_range.min_row == row and \
       merged_range.min_col == 2 and merged_range.max_col == 3:  # B:C 병합
        first_cell = ws.cell(merged_range.min_row, merged_range.min_col)
        if value and value > 0:
            first_cell.value = f"{label} : {value:,}원"
        else:
            first_cell.value = label  # 값이 없어도 제목은 유지
```

### 2. 매핑 파일 업데이트

**파일**: `payroll_generator/templates/designs/configs/template_sample1_mapping.json`

**추가된 매핑**:
```json
{
  "meal_allowance": "C8",
  "vehicle_maintenance": "C9",
  "position_allowance": "C10",
  "service_allowance": "C11",
  "oncall_allowance": "C13",
  "other": "C15"
}
```

### 3. 데이터 소스 처리

**변경 사항**:
- `payroll_data`에서 가져오는 항목: 기본급, 연장근무수당, 상여금
- `employee_data`에서 가져오는 항목: 식대, 차량유지비, 직책수당, 근속수당, 당직수당, 기타
- 값이 없으면 0으로 처리하고 제목만 표시

---

## 📊 수정 결과

### 테스트 결과

**생성된 파일의 지급내역 확인**:
- ✅ B7: 기본급 : 1,000,000원
- ✅ B8: 식대 : 100,000원 (employee_data에서 가져옴)
- ✅ B9: 차량유지비 : 50,000원 (employee_data에서 가져옴)
- ✅ B10: 직책수당 : 200,000원 (employee_data에서 가져옴)
- ✅ B11: 근속수당 : 100,000원 (employee_data에서 가져옴)
- ✅ B12: 연장수당 : 100,000원 (payroll_data에서 가져옴)
- ✅ B13: 당직수당 : 30,000원 (employee_data에서 가져옴)
- ✅ B14: 상여금 : 50,000원 (payroll_data에서 가져옴)
- ✅ B15: 기타 (값 없음, 제목만 표시)

**결과**: ✅ 모든 지급 항목 제목이 올바른 형식으로 표시됩니다!

---

## 📁 변경된 파일

### 수정된 파일
1. **`payroll_generator/templates/designs/template_design.py`**
   - 지급 항목 처리 로직 개선
   - 병합된 셀에 제목과 값 함께 표시
   - employee_data에서 추가 지급 항목 값 가져오기 지원

2. **`payroll_generator/templates/designs/configs/template_sample1_mapping.json`**
   - `meal_allowance`: C8 추가
   - `vehicle_maintenance`: C9 추가
   - `position_allowance`: C10 추가
   - `service_allowance`: C11 추가
   - `oncall_allowance`: C13 추가
   - `other`: C15 추가

---

## 🎯 개선 사항

### Before (수정 전)
- 지급 항목의 제목이 누락됨
- 숫자만 표시되어 가독성 저하
- 일부 지급 항목 매핑 없음

### After (수정 후)
- ✅ 모든 지급 항목의 제목이 표시됨
- ✅ "제목 : 값원" 형식으로 표시되어 가독성 향상
- ✅ 모든 지급 항목 매핑 완료
- ✅ employee_data에서 추가 지급 항목 지원

---

## 🔍 기술적 세부사항

### 병합된 셀 처리

템플릿에서 지급 항목은 다음과 같이 병합되어 있습니다:
- B7:C7 = 기본급
- B8:C8 = 식대
- B9:C9 = 차량유지비
- B10:C10 = 직책수당
- B11:C11 = 근속수당
- B12:C12 = 연장수당
- B13:C13 = 당직수당
- B14:C14 = 상여금
- B15:C15 = 기타

### 처리 로직

1. 셀 주소에서 행 번호 추출 (예: C7 → 7)
2. 해당 행의 B:C 병합 여부 확인
3. 병합된 경우 첫 번째 셀(B열)에 제목과 값 함께 표시
4. 값이 있으면 "제목 : 값원" 형식, 없으면 "제목"만 표시

### 데이터 소스

- **payroll_data**: 계산된 지급 항목 (기본급, 연장근무수당, 상여금)
- **employee_data**: 사용자 입력 지급 항목 (식대, 차량유지비, 직책수당, 근속수당, 당직수당, 기타)

---

## 📝 참고사항

### 값 표시 형식

- **값이 있는 경우**: "기본급 : 1,000,000원" (제목 + " : " + 쉼표 구분 숫자 + "원")
- **값이 없는 경우**: "기타" (제목만)

### 하위 호환성

- 기존 코드와 호환됨
- 값이 있는 항목은 기존과 동일하게 계산됨
- 값이 없는 항목은 제목만 표시됨
- employee_data에 추가 지급 항목이 없어도 정상 작동

---

## 🚀 사용 예시

### employee_data에 추가 지급 항목 포함

```python
employee_data = {
    '이름': '홍길동',
    '기본급': 1000000,
    '식대': 100000,
    '차량유지비': 50000,
    '직책수당': 200000,
    '근속수당': 100000,
    '당직수당': 30000,
    '상여금': 50000,
    '기타': 0
}
```

**결과**:
- 기본급 : 1,000,000원
- 식대 : 100,000원
- 차량유지비 : 50,000원
- 직책수당 : 200,000원
- 근속수당 : 100,000원
- 연장수당 : 100,000원 (계산됨)
- 당직수당 : 30,000원
- 상여금 : 50,000원
- 기타 (값 없음)

---

**작성자**: AI Assistant  
**작성 일시**: 2025-12-15  
**검증 상태**: ✅ 완료
