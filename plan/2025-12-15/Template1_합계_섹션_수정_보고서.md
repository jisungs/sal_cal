# Template1 합계 섹션 수정 보고서

**작성일**: 2025-12-15  
**문제**: Template1로 생성된 급여명세서에서 지급합계, 공제합계, 실지급액이 음영 박스에 0으로 표시됨  
**상태**: ✅ 완료  
**브랜치**: `fix/template1-summary-amounts`

---

## 📋 문제 개요

### 발견된 문제

Template1로 생성된 급여명세서에서 하단 합계 섹션의 음영 박스에 0이 표시되었습니다.

**생성된 급여명세서** (수정 전):
- ❌ 지급합계 (H23): 0
- ❌ 공제합계 (H24): 0
- ✅ 실지급액 (H25): 올바르게 표시됨 (수식으로 계산)

**요구사항**:
- 지급합계 (H23): 계산된 총지급액 표시
- 공제합계 (H24): 계산된 총공제액 표시
- 실지급액 (H25): 이미 올바르게 표시됨

---

## 🔍 원인 분석

### 문제 원인

1. **매핑 파일의 잘못된 셀 주소**
   - `total_payment`: "G23" (F23:G23 병합 셀의 일부)
   - `total_deduction`: "G24" (F24:G24 병합 셀의 일부)
   - 실제로는 H23, H24에 값을 써야 함

2. **병합 셀 처리 로직의 영향**
   - `total_payment`와 `total_deduction`가 병합 셀 처리 로직을 거치면서
   - F23:G23, F24:G24 병합 셀에 제목과 함께 쓰려고 시도
   - 하지만 실제 음영 박스는 H23, H24에 있음

3. **템플릿 구조**
   - F23:G23 병합 = "지급합계" (라벨)
   - F24:G24 병합 = "공제합계" (라벨)
   - F25:G25 병합 = "실지급액" (라벨)
   - H23 = 음영 박스 (지급합계 값)
   - H24 = 음영 박스 (공제합계 값)
   - H25 = 음영 박스 (실지급액 값, 수식 =H23-H24)

---

## ✅ 해결 방법

### 1. 매핑 파일 수정

**파일**: `payroll_generator/templates/designs/configs/template_sample1_mapping.json`

**변경 사항**:
- `total_payment`: "G23" → "H23"
- `total_deduction`: "G24" → "H24"
- `net_pay`: "H25" (변경 없음)

```json
{
  "total_payment": "H23",
  "total_deduction": "H24",
  "net_pay": "H25"
}
```

### 2. 코드 수정

**파일**: `payroll_generator/templates/designs/template_design.py`

**변경 사항**:
- `total_payment`와 `total_deduction`를 병합 셀 처리 로직에서 제외
- H23, H24에 숫자만 직접 표시

**코드 변경**:
```python
# total_payment는 H23에 숫자만 표시 (병합 셀 처리 제외)
if cell_key == 'total_payment':
    self._safe_set_cell_value(ws, cell_addr, value)
    continue

# total_deduction는 H24에 숫자만 표시 (병합 셀 처리 제외)
if cell_key == 'total_deduction':
    self._safe_set_cell_value(ws, cell_addr, value)
    continue
```

---

## 📊 수정 결과

### 테스트 결과

**생성된 파일의 합계 섹션 확인**:
- ✅ H23 (지급합계): 1,020,000
- ✅ H24 (공제합계): 155,152
- ✅ H25 (실지급액): 864,848

**결과**: ✅ 모든 합계 값이 올바르게 표시됩니다!

---

## 📁 변경된 파일

### 수정된 파일
1. **`payroll_generator/templates/designs/configs/template_sample1_mapping.json`**
   - `total_payment`: "G23" → "H23"
   - `total_deduction`: "G24" → "H24"

2. **`payroll_generator/templates/designs/template_design.py`**
   - `total_payment`와 `total_deduction`를 병합 셀 처리 로직에서 제외
   - H23, H24에 숫자만 직접 표시

---

## 🎯 개선 사항

### Before (수정 전)
- 지급합계 (H23): 0
- 공제합계 (H24): 0
- 실지급액 (H25): 올바르게 표시됨

### After (수정 후)
- ✅ 지급합계 (H23): 계산된 총지급액 표시
- ✅ 공제합계 (H24): 계산된 총공제액 표시
- ✅ 실지급액 (H25): 올바르게 표시됨 (수식 또는 직접 값)

---

## 🔍 기술적 세부사항

### 셀 구조

1. **라벨 셀 (병합)**
   - F23:G23 = "지급합계"
   - F24:G24 = "공제합계"
   - F25:G25 = "실지급액"

2. **값 셀 (음영 박스)**
   - H23 = 지급합계 값 (숫자만)
   - H24 = 공제합계 값 (숫자만)
   - H25 = 실지급액 값 (수식 =H23-H24 또는 직접 값)

### 처리 로직

1. **일반 지급/공제 항목**
   - 병합 셀 (B:C 또는 F:G)에 "제목 : 값" 형식으로 표시

2. **합계 항목**
   - 병합되지 않은 셀 (H23, H24, H25)에 숫자만 표시
   - 병합 셀 처리 로직에서 제외

---

## 📝 참고사항

### 수식 처리

- H25는 템플릿에 `=H23-H24` 수식이 있음
- 하지만 안정성을 위해 직접 값도 씀
- 수식과 직접 값 모두 올바르게 작동함

### 형식 통일

- 합계 섹션은 숫자만 표시 (천 단위 구분 없음)
- 라벨은 F23:G23, F24:G24, F25:G25 병합 셀에 표시
- 값은 H23, H24, H25에 표시

---

**작성자**: AI Assistant  
**작성 일시**: 2025-12-15  
**검증 상태**: ✅ 완료
