# Template Design IndentationError 수정 보고서

**작성일**: 2025-12-16  
**에러 타입**: `IndentationError`  
**파일**: `payroll_generator/templates/designs/template_design.py`  
**상태**: ✅ 수정 완료

---

## 🔍 에러 분석

### 에러 메시지
```
IndentationError: expected an indented block after 'if' statement on line 312
```

### 발생 위치
- **파일**: `payroll_generator/templates/designs/template_design.py`
- **라인**: 312번째 줄
- **컨텍스트**: `if source == 'payroll':` 문 다음에 들여쓰기된 블록이 없음

### 원인 분석

312번째 줄의 `if source == 'payroll':` 문 다음에 오는 코드 블록(313번째 줄)이 올바르게 들여쓰기되지 않았습니다.

**문제가 있던 코드 구조**:
```python
309|        for cell_key, (data_key, label, source) in payment_mapping.items():
310|            if cell_key in self.cell_mapping:
311|                # payroll_data 또는 employee_data에서 값 가져오기
312|                if source == 'payroll':
313|                value = payroll_data.get(data_key, 0)  # ❌ 들여쓰기 누락!
314|                else:  # employee
315|                    # employee_data에서 직접 가져오거나 0으로 설정
316|                    value = employee_data.get(data_key, employee_data.get(f'{data_key}원', 0))
```

**문제점**:
- 312번째 줄의 `if source == 'payroll':` 블록 안에 있어야 하는 313번째 줄이 들여쓰기가 되어 있지 않음
- Python은 `if` 문 다음에 반드시 들여쓰기된 블록을 요구함
- 313번째 줄이 `if` 문과 같은 레벨에 있어서 Python 파서가 에러 발생

### 영향

이 에러로 인해:
1. **템플릿 클래스 import 실패**: `template_sample1.py`에서 `template_design.py`를 import할 수 없음
2. **디자인 팩토리 작동 불가**: `DesignFactory`가 템플릿 클래스를 import할 수 없어 `None` 반환
3. **템플릿 디자인 미적용**: 모든 템플릿 선택이 기본 디자인으로 폴백됨

---

## ✅ 수정 내용

### 수정 전 (312-322번째 줄)
```python
                if source == 'payroll':
                value = payroll_data.get(data_key, 0)  # ❌ 들여쓰기 누락!
                else:  # employee
                    # employee_data에서 직접 가져오거나 0으로 설정
                    value = employee_data.get(data_key, employee_data.get(f'{data_key}원', 0))
                    if isinstance(value, str):
                        try:
                            value = int(value.replace(',', '').replace('원', ''))
                        except (ValueError, AttributeError):
                            value = 0
                    value = value if value else 0
```

### 수정 후 (312-322번째 줄)
```python
                if source == 'payroll':
                    value = payroll_data.get(data_key, 0)  # ✅ 들여쓰기 추가!
                else:  # employee
                    # employee_data에서 직접 가져오거나 0으로 설정
                    value = employee_data.get(data_key, employee_data.get(f'{data_key}원', 0))
                    if isinstance(value, str):
                        try:
                            value = int(value.replace(',', '').replace('원', ''))
                        except (ValueError, AttributeError):
                            value = 0
                    value = value if value else 0
```

### 변경 사항
- 313번째 줄에 **4칸 들여쓰기 추가**
- `if source == 'payroll':` 블록 내부의 코드가 올바르게 들여쓰기됨

---

## 📊 코드 구조 분석

### 전체 들여쓰기 레벨
```
309|        for cell_key, (data_key, label, source) in payment_mapping.items():  # 8칸
310|            if cell_key in self.cell_mapping:  # 12칸
311|                # payroll_data 또는 employee_data에서 값 가져오기  # 16칸
312|                if source == 'payroll':  # 16칸
313|                    value = payroll_data.get(data_key, 0)  # 20칸 (수정 후)
314|                else:  # employee  # 16칸
315|                    # employee_data에서 직접 가져오거나 0으로 설정  # 20칸
316|                    value = employee_data.get(data_key, employee_data.get(f'{data_key}원', 0))  # 20칸
```

### 중첩 구조
1. **for 루프** (8칸): `for cell_key, ... in payment_mapping.items():`
2. **첫 번째 if 블록** (12칸): `if cell_key in self.cell_mapping:`
3. **두 번째 if 블록** (16칸): `if source == 'payroll':`
4. **if 블록 내부** (20칸): `value = payroll_data.get(data_key, 0)`

---

## ✅ 검증 결과

### 린터 검사
```
✅ No linter errors found.
```

### 문법 검사
- Python 파서가 코드를 정상적으로 파싱할 수 있음
- 들여쓰기가 일관되게 적용됨

### 기능 테스트
```python
# 디자인 팩토리 테스트
from payroll_generator.templates.designs.design_factory import DesignFactory

# 사용 가능한 디자인 확인
designs = DesignFactory.list_available_designs()
# 결과: ['template_sample1', 'template_sample2'] ✅

# 템플릿1 디자인 가져오기
design = DesignFactory.get_design('template_sample1')
# 결과: <payroll_generator.templates.designs.template_sample1.TemplateSample1 object> ✅

# 템플릿 경로 확인
template_path = design._get_template_path()
# 결과: /Users/jisungs/Documents/dev/sideprojects/salary_cal/sample/급여명세서_template.xlsx ✅

# 파일 존재 확인
import os
os.path.exists(template_path)
# 결과: True ✅
```

---

## 🔗 관련 파일

이 에러는 이전에 수정한 들여쓰기 오류들과 동일한 패턴입니다:

1. **`payroll_generator/excel_handler.py`** ✅ (이미 수정 완료)
   - 77번째 줄 `if design_name:` 블록
   - 78-97번째 줄 들여쓰기 수정

2. **`payroll_generator/pdf_generator.py`** ✅ (이미 수정 완료)
   - 74번째 줄 `if design_name:` 블록
   - 75-94번째 줄 들여쓰기 수정

3. **`payroll_generator/templates/designs/template_design.py`** ✅ (방금 수정 완료)
   - 312번째 줄 `if source == 'payroll':` 블록
   - 313번째 줄 들여쓰기 수정

세 파일 모두 동일한 패턴의 에러였으며, 모두 수정 완료되었습니다.

---

## 🎯 문제 해결 확인

### 수정 전 상태
- ❌ 템플릿 클래스 import 실패
- ❌ 디자인 팩토리 작동 불가
- ❌ 템플릿 디자인 미적용

### 수정 후 상태
- ✅ 템플릿 클래스 import 성공
- ✅ 디자인 팩토리 정상 작동
- ✅ 템플릿 경로 올바르게 찾음
- ✅ 템플릿 디자인 적용 가능

---

## 📝 요약

**핵심 문제**:
- `template_design.py` 파일의 312번째 줄에 들여쓰기 오류가 있어 템플릿 클래스를 import할 수 없었음
- 이로 인해 디자인 팩토리가 템플릿 디자인을 가져올 수 없어 항상 `None` 반환
- 결과적으로 모든 템플릿 선택이 기본 디자인으로 폴백됨

**해결 방법**:
- 313번째 줄에 4칸 들여쓰기 추가
- `if source == 'payroll':` 블록 내부 코드가 올바르게 들여쓰기됨

**검증 결과**:
- ✅ 문법 오류 해결
- ✅ 템플릿 클래스 import 성공
- ✅ 디자인 팩토리 정상 작동
- ✅ 템플릿 경로 올바르게 찾음

이제 직접 입력 폼에서 템플릿1을 선택하면 정상적으로 템플릿 디자인이 적용될 것입니다.

---

## 🚀 다음 단계

1. **애플리케이션 재시작**: 변경사항 적용을 위해 애플리케이션 재시작
2. **기능 테스트**: 직접 입력 폼에서 템플릿1 선택 후 엑셀 생성 테스트
3. **로그 확인**: 템플릿 디자인이 올바르게 적용되는지 로그 확인

---

**작성자**: AI Assistant  
**작성 일시**: 2025-12-16  
**상태**: ✅ 수정 완료 및 검증 완료

