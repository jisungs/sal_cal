# PDF Generator IndentationError 분석 및 수정 보고서

**작성일**: 2025-12-16  
**에러 타입**: `IndentationError`  
**파일**: `payroll_generator/pdf_generator.py`  
**상태**: ✅ 수정 완료

---

## 🔍 에러 분석

### 에러 메시지
```
IndentationError: expected an indented block after 'if' statement on line 74
```

### 발생 위치
- **파일**: `payroll_generator/pdf_generator.py`
- **라인**: 74번째 줄
- **컨텍스트**: `if design_name:` 문 다음에 들여쓰기된 블록이 없음

### 원인 분석

`excel_handler.py`에서 발생한 것과 동일한 패턴의 에러입니다. 74번째 줄의 `if design_name:` 문 다음에 오는 코드 블록(75-94번째 줄)이 올바르게 들여쓰기되지 않았습니다.

**문제가 있던 코드 구조**:
```python
64|        if design_name:
65|            # design_1, design_2는 더 이상 지원하지 않음
66|            if design_name in ['design_1', 'design_2']:
67|                logger.warning(...)
72|                design_name = None
73|            
74|            if design_name:  # template_sample1, template_sample2만 처리
75|            logger.info(...)  # ❌ 들여쓰기 누락!
76|            try:              # ❌ 들여쓰기 누락!
77|                from .templates.designs.design_factory import DesignFactory
...
```

**문제점**:
- 74번째 줄의 `if design_name:` 블록 안에 있어야 하는 75-94번째 줄들이 들여쓰기가 되어 있지 않음
- Python은 `if` 문 다음에 반드시 들여쓰기된 블록을 요구함
- 75번째 줄이 `if` 문과 같은 레벨에 있어서 Python 파서가 에러 발생

---

## ✅ 수정 내용

### 수정 전 (74-94번째 줄)
```python
            if design_name:  # template_sample1, template_sample2만 처리
            logger.info(f"[PDF 생성] design_name 파라미터: '{design_name}'")
            try:
                from .templates.designs.design_factory import DesignFactory
                logger.info(f"[PDF 생성] 디자인 팩토리에서 '{design_name}' 가져오기 시도")
                logger.info(f"[PDF 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                
                design = DesignFactory.get_design(design_name)
                logger.info(f"[PDF 생성] 디자인 인스턴스: {design is not None}")
                
                if design:
                    logger.info(f"[PDF 생성] 디자인 '{design_name}' 사용하여 PDF 생성 시작")
                    result = design.generate_pdf(payroll_data, employee_data, output_path, period)
                    logger.info(f"[PDF 생성] 디자인 '{design_name}' 사용하여 PDF 생성 완료")
                    return result
                else:
                    logger.warning(f"[PDF 생성] 디자인 '{design_name}'을 찾을 수 없습니다. 기본 방식 사용")
                    logger.warning(f"[PDF 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
            except Exception as e:
                logger.error(f"[PDF 생성] 디자인 '{design_name}' 생성 실패: {e}", exc_info=True)
                logger.warning(f"[PDF 생성] 기본 방식으로 폴백")
```

### 수정 후 (74-94번째 줄)
```python
            if design_name:  # template_sample1, template_sample2만 처리
                logger.info(f"[PDF 생성] design_name 파라미터: '{design_name}'")
                try:
                    from .templates.designs.design_factory import DesignFactory
                    logger.info(f"[PDF 생성] 디자인 팩토리에서 '{design_name}' 가져오기 시도")
                    logger.info(f"[PDF 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                    
                    design = DesignFactory.get_design(design_name)
                    logger.info(f"[PDF 생성] 디자인 인스턴스: {design is not None}")
                    
                    if design:
                        logger.info(f"[PDF 생성] 디자인 '{design_name}' 사용하여 PDF 생성 시작")
                        result = design.generate_pdf(payroll_data, employee_data, output_path, period)
                        logger.info(f"[PDF 생성] 디자인 '{design_name}' 사용하여 PDF 생성 완료")
                        return result
                    else:
                        logger.warning(f"[PDF 생성] 디자인 '{design_name}'을 찾을 수 없습니다. 기본 방식 사용")
                        logger.warning(f"[PDF 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                except Exception as e:
                    logger.error(f"[PDF 생성] 디자인 '{design_name}' 생성 실패: {e}", exc_info=True)
                    logger.warning(f"[PDF 생성] 기본 방식으로 폴백")
```

### 변경 사항
- 75번째 줄부터 94번째 줄까지 **4칸 들여쓰기 추가**
- `if design_name:` 블록 내부의 모든 코드가 올바르게 들여쓰기됨

---

## 📊 코드 구조 분석

### 전체 들여쓰기 레벨
```
49|    def generate_payslip(...):  # 0칸 (메서드 정의)
63|        # 디자인 선택 시 디자인 클래스 사용  # 4칸
64|        if design_name:  # 4칸
65|            # design_1, design_2는 더 이상 지원하지 않음  # 8칸
66|            if design_name in ['design_1', 'design_2']:  # 8칸
67|                logger.warning(...)  # 12칸
72|                design_name = None  # 12칸
74|            if design_name:  # 8칸
75|                logger.info(...)  # 12칸 (수정 후)
76|                try:  # 12칸 (수정 후)
77|                    from .templates.designs.design_factory import DesignFactory  # 16칸
...
```

### 중첩 구조
1. **메서드 레벨** (4칸): `generate_payslip` 메서드
2. **첫 번째 if 블록** (8칸): `if design_name:`
3. **두 번째 if 블록** (12칸): `if design_name:` (74번째 줄)
4. **try 블록** (16칸): `try:` 문
5. **내부 if 블록** (20칸): `if design:`

---

## 🔗 관련 파일

이 에러는 `excel_handler.py`에서 발생한 것과 동일한 패턴입니다:

1. **`payroll_generator/excel_handler.py`** ✅ (이미 수정 완료)
   - 77번째 줄 `if design_name:` 블록
   - 78-97번째 줄 들여쓰기 수정

2. **`payroll_generator/pdf_generator.py`** ✅ (방금 수정 완료)
   - 74번째 줄 `if design_name:` 블록
   - 75-94번째 줄 들여쓰기 수정

두 파일 모두 동일한 로직 구조를 가지고 있어서 같은 패턴의 에러가 발생했습니다.

---

## ✅ 검증 결과

### 린터 검사
```
✅ No linter errors found.
```

### 문법 검사
- Python 파서가 코드를 정상적으로 파싱할 수 있음
- 들여쓰기가 일관되게 적용됨

### 유사 패턴 검사
- `payroll_generator` 디렉토리 내 다른 파일에서 유사한 패턴이 더 이상 없음 확인

---

## 🎯 수정 완료 확인

1. ✅ **들여쓰기 오류 수정**: 75-94번째 줄이 올바르게 들여쓰기됨
2. ✅ **코드 구조 유지**: 기존 로직은 변경 없이 들여쓰기만 수정
3. ✅ **린터 통과**: 문법 오류 없음
4. ✅ **중첩 구조 정상**: if-try-except 블록이 올바르게 중첩됨
5. ✅ **유사 패턴 확인**: 다른 파일에서 동일한 문제 없음

---

## 📝 참고 사항

### 동일한 패턴의 에러가 두 파일에서 발생한 이유

`excel_handler.py`와 `pdf_generator.py`는 모두 디자인 팩토리 패턴을 사용하여 엑셀/PDF를 생성하는 로직을 가지고 있습니다. 두 파일 모두:

1. `design_name` 파라미터를 받아서 처리
2. `design_1`, `design_2`는 더 이상 지원하지 않음 (폴백)
3. `template_sample1`, `template_sample2`만 처리
4. 동일한 중첩 if 구조 사용

따라서 코드를 복사/붙여넣기하거나 유사하게 작성하는 과정에서 동일한 들여쓰기 실수가 발생한 것으로 보입니다.

---

## 🚀 다음 단계

이제 애플리케이션을 정상적으로 실행할 수 있습니다:

```bash
python app.py
```

두 파일 모두 수정되었으므로 애플리케이션이 정상적으로 시작될 것입니다.

---

## 📋 수정 요약

| 파일 | 라인 | 문제 | 상태 |
|------|------|------|------|
| `excel_handler.py` | 77-97 | `if design_name:` 블록 들여쓰기 누락 | ✅ 수정 완료 |
| `pdf_generator.py` | 74-94 | `if design_name:` 블록 들여쓰기 누락 | ✅ 수정 완료 |

두 파일 모두 동일한 패턴의 에러였으며, 모두 수정 완료되었습니다.

