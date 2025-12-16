# IndentationError 분석 및 수정 보고서

**작성일**: 2025-12-16  
**에러 타입**: `IndentationError`  
**파일**: `payroll_generator/excel_handler.py`  
**상태**: ✅ 수정 완료

---

## 🔍 에러 분석

### 에러 메시지
```
IndentationError: expected an indented block after 'if' statement on line 77
```

### 발생 위치
- **파일**: `payroll_generator/excel_handler.py`
- **라인**: 77번째 줄
- **컨텍스트**: `if design_name:` 문 다음에 들여쓰기된 블록이 없음

### 원인 분석

77번째 줄의 `if design_name:` 문 다음에 오는 코드 블록(78-97번째 줄)이 올바르게 들여쓰기되지 않았습니다.

**문제가 있던 코드 구조**:
```python
67|        if design_name:
68|            # design_1, design_2는 더 이상 지원하지 않음
69|            if design_name in ['design_1', 'design_2']:
70|                logger.warning(...)
75|                design_name = None
76|            
77|            if design_name:  # template_sample1, template_sample2만 처리
78|            logger.info(...)  # ❌ 들여쓰기 누락!
79|            try:              # ❌ 들여쓰기 누락!
80|                from .templates.designs.design_factory import DesignFactory
...
```

**문제점**:
- 77번째 줄의 `if design_name:` 블록 안에 있어야 하는 78-97번째 줄들이 들여쓰기가 되어 있지 않음
- Python은 `if` 문 다음에 반드시 들여쓰기된 블록을 요구함
- 78번째 줄이 `if` 문과 같은 레벨에 있어서 Python 파서가 에러 발생

---

## ✅ 수정 내용

### 수정 전 (77-97번째 줄)
```python
            if design_name:  # template_sample1, template_sample2만 처리
            logger.info(f"[Excel 생성] design_name 파라미터: '{design_name}'")
            try:
                from .templates.designs.design_factory import DesignFactory
                logger.info(f"[Excel 생성] 디자인 팩토리에서 '{design_name}' 가져오기 시도")
                logger.info(f"[Excel 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                
                design = DesignFactory.get_design(design_name)
                logger.info(f"[Excel 생성] 디자인 인스턴스: {design is not None}")
                
                if design:
                    logger.info(f"[Excel 생성] 디자인 '{design_name}' 사용하여 엑셀 생성 시작")
                    result = design.generate_excel(payroll_data, employee_data, output_path, period)
                    logger.info(f"[Excel 생성] 디자인 '{design_name}' 사용하여 엑셀 생성 완료")
                    return result
                else:
                    logger.warning(f"[Excel 생성] 디자인 '{design_name}'을 찾을 수 없습니다. 기본 방식 사용")
                    logger.warning(f"[Excel 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
            except Exception as e:
                logger.error(f"[Excel 생성] 디자인 '{design_name}' 생성 실패: {e}", exc_info=True)
                logger.warning(f"[Excel 생성] 기본 방식으로 폴백")
```

### 수정 후 (77-97번째 줄)
```python
            if design_name:  # template_sample1, template_sample2만 처리
                logger.info(f"[Excel 생성] design_name 파라미터: '{design_name}'")
                try:
                    from .templates.designs.design_factory import DesignFactory
                    logger.info(f"[Excel 생성] 디자인 팩토리에서 '{design_name}' 가져오기 시도")
                    logger.info(f"[Excel 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                    
                    design = DesignFactory.get_design(design_name)
                    logger.info(f"[Excel 생성] 디자인 인스턴스: {design is not None}")
                    
                    if design:
                        logger.info(f"[Excel 생성] 디자인 '{design_name}' 사용하여 엑셀 생성 시작")
                        result = design.generate_excel(payroll_data, employee_data, output_path, period)
                        logger.info(f"[Excel 생성] 디자인 '{design_name}' 사용하여 엑셀 생성 완료")
                        return result
                    else:
                        logger.warning(f"[Excel 생성] 디자인 '{design_name}'을 찾을 수 없습니다. 기본 방식 사용")
                        logger.warning(f"[Excel 생성] 사용 가능한 디자인: {DesignFactory.list_available_designs()}")
                except Exception as e:
                    logger.error(f"[Excel 생성] 디자인 '{design_name}' 생성 실패: {e}", exc_info=True)
                    logger.warning(f"[Excel 생성] 기본 방식으로 폴백")
```

### 변경 사항
- 78번째 줄부터 97번째 줄까지 **4칸 들여쓰기 추가**
- `if design_name:` 블록 내부의 모든 코드가 올바르게 들여쓰기됨

---

## 📊 코드 구조 분석

### 전체 들여쓰기 레벨
```
52|    def write_payroll(...):  # 0칸 (메서드 정의)
66|        # 디자인 선택 시 디자인 클래스 사용  # 4칸
67|        if design_name:  # 4칸
68|            # design_1, design_2는 더 이상 지원하지 않음  # 8칸
69|            if design_name in ['design_1', 'design_2']:  # 8칸
70|                logger.warning(...)  # 12칸
75|                design_name = None  # 12칸
77|            if design_name:  # 8칸
78|                logger.info(...)  # 12칸 (수정 후)
79|                try:  # 12칸 (수정 후)
80|                    from .templates.designs.design_factory import DesignFactory  # 16칸
...
```

### 중첩 구조
1. **메서드 레벨** (4칸): `write_payroll` 메서드
2. **첫 번째 if 블록** (8칸): `if design_name:`
3. **두 번째 if 블록** (12칸): `if design_name:` (77번째 줄)
4. **try 블록** (16칸): `try:` 문
5. **내부 if 블록** (20칸): `if design:`

---

## ✅ 검증 결과

### 린터 검사
```
✅ No linter errors found.
```

### 문법 검사
- Python 파서가 코드를 정상적으로 파싱할 수 있음
- 들여쓰기가 일관되게 적용됨

---

## 🎯 수정 완료 확인

1. ✅ **들여쓰기 오류 수정**: 78-97번째 줄이 올바르게 들여쓰기됨
2. ✅ **코드 구조 유지**: 기존 로직은 변경 없이 들여쓰기만 수정
3. ✅ **린터 통과**: 문법 오류 없음
4. ✅ **중첩 구조 정상**: if-try-except 블록이 올바르게 중첩됨

---

## 📝 참고 사항

### Python 들여쓰기 규칙
- Python은 들여쓰기를 사용하여 코드 블록을 구분함
- `if`, `for`, `while`, `try`, `except`, `def`, `class` 등의 문 다음에는 반드시 들여쓰기된 블록이 필요함
- 들여쓰기는 일관되게 사용해야 함 (보통 4칸 스페이스 또는 탭)

### 이 에러가 발생하는 경우
1. `if` 문 다음에 코드가 같은 레벨에 있을 때
2. 들여쓰기가 불일치할 때
3. 빈 블록이 필요할 때 `pass`를 사용하지 않았을 때

---

## 🚀 다음 단계

이제 애플리케이션을 정상적으로 실행할 수 있습니다:

```bash
python app.py
```

에러가 해결되었으므로 애플리케이션이 정상적으로 시작될 것입니다.

