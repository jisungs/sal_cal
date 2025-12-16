# Sample 템플릿 기본 디자인 통합 실행 계획 v2.0

**작성일**: 2025-12-12  
**버전**: 2.0 (프로 개발자 관점 개선)  
**목적**: Sample 폴더의 두 엑셀 템플릿을 기본 디자인 옵션으로 추가  
**원칙**: 기존 기능 유지하면서 확장, 실현 가능한 기술 스택 사용, 프로덕션 품질 보장

> **⚠️ 중요**: 이 문서는 v1.0을 프로 개발자 관점에서 실현 가능하도록 업그레이드한 버전입니다. 자동화된 분석 도구, 강화된 에러 처리, 구체적인 테스트 전략, 그리고 실제 구현 가능한 코드 예시를 포함합니다.

---

## 📋 변경 사항 요약 (v1.0 → v2.0)

### 주요 개선 사항

1. **자동화된 템플릿 분석**
   - 수동 분석 대신 Python 스크립트를 통한 자동 셀 매핑 추출
   - 템플릿 구조 분석 및 검증 자동화

2. **강화된 에러 처리**
   - 템플릿 파일 누락 시 폴백 전략
   - 셀 매핑 검증 로직
   - 상세한 에러 메시지 및 로깅

3. **기존 코드 재사용**
   - `ExcelHandler._write_payroll_from_template` 로직 재사용
   - 중복 코드 최소화

4. **구체적인 테스트 전략**
   - 단위 테스트, 통합 테스트, 회귀 테스트 명확히 구분
   - 테스트 케이스 예시 포함

5. **실제 구현 가능한 코드**
   - 프로덕션 품질의 코드 예시
   - 에러 처리, 로깅, 검증 포함

---

## 🌿 Git 브랜치 전략

### 브랜치 구조

```
master (메인 브랜치)
  │
  ├── develop (개발 브랜치)
  │     │
  │     └── feature/template-designs (새 기능 브랜치)
  │           │
  │           ├── feature/template-designs-phase-0 (준비 작업)
  │           ├── feature/template-designs-phase-1 (템플릿 디자인 클래스)
  │           ├── feature/template-designs-phase-2 (DesignFactory 등록)
  │           ├── feature/template-designs-phase-3 (UI 업데이트)
  │           └── feature/template-designs-phase-4 (테스트 및 검증)
```

### 브랜치 명명 규칙

- **기능 브랜치**: `feature/template-designs` (메인 기능 브랜치)
- **단계별 브랜치**: `feature/template-designs-phase-{N}` (각 Phase별 작업)

### 커밋 메시지 규칙

- `feat(template): Phase N - 작업 내용` (기능 추가)
- `fix(template): 버그 수정 내용` (버그 수정)
- `docs(template): 문서 추가/수정` (문서)
- `refactor(template): 리팩토링 내용` (리팩토링)
- `test(template): 테스트 추가` (테스트)

### 머지 전략

- 각 Phase 완료 후 `feature/template-designs-phase-{N}` → `feature/template-designs` 머지 (`--no-ff`)
- 최종 완료 후 `feature/template-designs` → `develop` 머지 (`--no-ff`)
- 배포 준비 완료 후 `develop` → `master` 머지 (`--no-ff`)

---

## 📋 개요

### 목표
- `sample/급여명세서_template.xlsx`를 기본 디자인 옵션으로 추가
- `sample/임금명세서양식_template3.xlsx`를 기본 디자인 옵션으로 추가
- 기존 기능(기본 디자인, design_1, design_2) 유지

### 현재 상태
- **기본 디자인**: `payroll_template.xlsx` 사용 (하드코딩된 셀 위치)
- **design_1, design_2**: YAML 설정 기반 직접 생성
- **디자인 선택**: 웹/데스크톱 인터페이스에서 선택 가능

### 추가할 디자인
- **template_sample1**: `sample/급여명세서_template.xlsx` 사용
- **template_sample2**: `sample/임금명세서양식_template3.xlsx` 사용

---

## 🏗️ 아키텍처 설계

### 최종 선택: 템플릿 기반 디자인 클래스 생성

```
BaseDesign (추상 클래스)
├── Design1 (YAML 기반)
├── Design2 (YAML 기반)
└── TemplateDesign (템플릿 기반, 새로 추가)
    ├── TemplateSample1 (급여명세서_template.xlsx)
    └── TemplateSample2 (임금명세서양식_template3.xlsx)
```

**장점**:
- 기존 구조와 일관성 유지
- 확장성 좋음 (새 템플릿 추가 용이)
- `DesignFactory`를 통한 통합 관리
- 기존 `ExcelHandler` 로직 재사용 가능

---

## 📝 실행 계획 (Git 브랜치 전략 포함)

### Phase 0: 준비 작업 및 템플릿 분석

**브랜치**: `feature/template-designs-phase-0`

#### Git 명령어
```bash
# 기능 브랜치 생성
git checkout develop
git checkout -b feature/template-designs
git checkout -b feature/template-designs-phase-0
```

#### 0.1 템플릿 분석 스크립트 개선
**파일**: `scripts/analyze_template_cells.py` (새로 생성)

**기능**:
- 템플릿 파일의 셀 구조 자동 분석
- 데이터 셀 위치 자동 추출
- 병합된 셀 정보 추출
- 수식이 있는 셀 식별
- 셀 매핑 딕셔너리 자동 생성

**구현 예시**:
```python
# scripts/analyze_template_cells.py
import openpyxl
from openpyxl.utils import get_column_letter
import json
import sys

def analyze_template(template_path, output_path=None):
    """템플릿 파일 분석 및 셀 매핑 생성"""
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active
    
    cell_mapping = {}
    merged_cells = []
    formula_cells = []
    
    # 모든 셀 순회
    for row in ws.iter_rows():
        for cell in row:
            if cell.value:
                value_str = str(cell.value).lower()
                cell_addr = cell.coordinate
                
                # 키워드 기반 자동 매핑
                if '기간' in value_str or 'period' in value_str:
                    cell_mapping['period'] = cell_addr
                elif '이름' in value_str or 'name' in value_str:
                    cell_mapping['employee_name'] = cell_addr
                elif '주민' in value_str or 'resident' in value_str:
                    cell_mapping['resident_number'] = cell_addr
                elif '입사' in value_str or 'join' in value_str:
                    cell_mapping['join_date'] = cell_addr
                elif '기본급' in value_str or 'basic' in value_str:
                    cell_mapping['basic_salary'] = cell_addr
                # ... 나머지 매핑
                
                # 수식 확인
                if cell.data_type == 'f':
                    formula_cells.append(cell_addr)
    
    # 병합된 셀 확인
    for merged_range in ws.merged_cells.ranges:
        merged_cells.append(str(merged_range))
    
    result = {
        'cell_mapping': cell_mapping,
        'merged_cells': merged_cells,
        'formula_cells': formula_cells,
        'sheet_name': ws.title
    }
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result

if __name__ == '__main__':
    template_path = sys.argv[1] if len(sys.argv) > 1 else 'sample/급여명세서_template.xlsx'
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    result = analyze_template(template_path, output_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

#### 0.2 템플릿 파일 분석 실행
```bash
# 템플릿 1 분석
python scripts/analyze_template_cells.py sample/급여명세서_template.xlsx \
    payroll_generator/templates/designs/configs/template_sample1_mapping.json

# 템플릿 2 분석
python scripts/analyze_template_cells.py sample/임금명세서양식_template3.xlsx \
    payroll_generator/templates/designs/configs/template_sample2_mapping.json
```

#### 0.3 템플릿 파일 프로젝트에 복사
- [ ] `sample/급여명세서_template.xlsx` → `payroll_generator/templates/designs/template_sample1.xlsx`
- [ ] `sample/임금명세서양식_template3.xlsx` → `payroll_generator/templates/designs/template_sample2.xlsx`
- [ ] 셀 매핑 JSON 파일 생성 및 검증

**예상 소요 시간**: 1-2시간

**Git 커밋**:
```bash
git add scripts/analyze_template_cells.py
git add payroll_generator/templates/designs/template_sample*.xlsx
git add payroll_generator/templates/designs/configs/template_sample*_mapping.json
git commit -m "feat(template): Phase 0 - 템플릿 파일 분석 및 추가

- 템플릿 분석 스크립트 생성 (자동 셀 매핑 추출)
- template_sample1.xlsx, template_sample2.xlsx 복사
- 셀 매핑 JSON 파일 생성"
```

**머지**:
```bash
git checkout feature/template-designs
git merge --no-ff feature/template-designs-phase-0 -m "merge: Phase 0 완료"
```

---

### Phase 1: 템플릿 기반 디자인 클래스 구현

**브랜치**: `feature/template-designs-phase-1`

#### Git 명령어
```bash
git checkout feature/template-designs
git checkout -b feature/template-designs-phase-1
```

#### 1.1 TemplateDesign 기본 클래스 생성
**파일**: `payroll_generator/templates/designs/template_design.py`

**핵심 기능**:
- `BaseDesign` 상속
- 템플릿 파일 경로 관리 (PyInstaller 환경 대응)
- 셀 매핑 JSON 파일 로드
- 템플릿 파일 로드 및 데이터 채우기
- 에러 처리 및 폴백 전략
- 병합된 셀 처리
- 수식 보존

**구현 상세**:
```python
# template_design.py
import openpyxl
import json
import os
import logging
from pathlib import Path
from .base_design import BaseDesign

logger = logging.getLogger(__name__)

class TemplateDesign(BaseDesign):
    """템플릿 기반 디자인 기본 클래스"""
    
    def __init__(self, template_filename, mapping_filename=None):
        """
        Args:
            template_filename: 템플릿 파일명 (예: 'template_sample1.xlsx')
            mapping_filename: 셀 매핑 JSON 파일명 (선택사항)
        """
        self.template_filename = template_filename
        self.mapping_filename = mapping_filename or template_filename.replace('.xlsx', '_mapping.json')
        self.cell_mapping = self._load_cell_mapping()
        super().__init__(config_path=None)  # YAML 설정 불필요
    
    def _load_cell_mapping(self):
        """셀 매핑 JSON 파일 로드"""
        paths_to_try = []
        
        # PyInstaller 환경
        try:
            from ..utils import resource_path
            paths_to_try.append(resource_path(
                f'templates/designs/configs/{self.mapping_filename}'
            ))
        except ImportError:
            try:
                from payroll_generator.utils import resource_path
                paths_to_try.append(resource_path(
                    f'templates/designs/configs/{self.mapping_filename}'
                ))
            except ImportError:
                pass
        
        # 개발 환경
        paths_to_try.append(os.path.join(
            os.path.dirname(__file__), 'configs', self.mapping_filename
        ))
        
        for path in paths_to_try:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        mapping_data = json.load(f)
                        return mapping_data.get('cell_mapping', {})
                except Exception as e:
                    logger.warning(f"셀 매핑 파일 로드 실패 ({path}): {e}")
                    continue
        
        logger.warning(f"셀 매핑 파일을 찾을 수 없습니다: {self.mapping_filename}")
        return {}
    
    def _get_template_path(self):
        """템플릿 파일 경로 찾기"""
        paths_to_try = []
        
        # PyInstaller 환경
        try:
            from ..utils import resource_path
            paths_to_try.append(resource_path(
                f'templates/designs/{self.template_filename}'
            ))
        except ImportError:
            try:
                from payroll_generator.utils import resource_path
                paths_to_try.append(resource_path(
                    f'templates/designs/{self.template_filename}'
                ))
            except ImportError:
                pass
        
        # 개발 환경
        paths_to_try.append(os.path.join(
            os.path.dirname(__file__), self.template_filename
        ))
        
        for path in paths_to_try:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError(
            f"템플릿 파일을 찾을 수 없습니다: {self.template_filename}. "
            f"다음 경로를 시도했습니다: {paths_to_try}"
        )
    
    def generate_excel(self, payroll_data, employee_data, output_path, period):
        """템플릿 파일을 사용하여 엑셀 생성"""
        try:
            template_path = self._get_template_path()
            wb = openpyxl.load_workbook(template_path)
            ws = wb.active
            
            # 셀 매핑에 따라 데이터 채우기
            self._fill_template_data(ws, payroll_data, employee_data, period)
            
            # 파일 저장
            from ..utils import normalize_path
            normalized_path = normalize_path(output_path)
            wb.save(normalized_path)
            wb.close()
            
            logger.info(f"템플릿 기반 엑셀 생성 완료: {normalized_path}")
        except FileNotFoundError as e:
            logger.error(f"템플릿 파일 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"엑셀 생성 실패: {e}")
            raise
    
    def _fill_template_data(self, ws, payroll_data, employee_data, period):
        """템플릿에 데이터 채우기"""
        # 기간
        if 'period' in self.cell_mapping and period:
            cell_addr = self.cell_mapping['period']
            ws[cell_addr] = f"지급기간: {period}"
        
        # 직원 정보
        if 'employee_name' in self.cell_mapping:
            ws[self.cell_mapping['employee_name']] = employee_data.get('이름', '')
        
        if 'resident_number' in self.cell_mapping:
            ws[self.cell_mapping['resident_number']] = self.mask_resident_number(
                employee_data.get('주민번호', '')
            )
        
        if 'join_date' in self.cell_mapping:
            join_date = employee_data.get('입사일', '')
            if join_date:
                if hasattr(join_date, 'strftime'):
                    ws[self.cell_mapping['join_date']] = join_date.strftime('%Y-%m-%d')
                else:
                    ws[self.cell_mapping['join_date']] = str(join_date)
        
        # 지급 항목 매핑
        payment_mapping = {
            'basic_salary': '기본급',
            'overtime': '연장근무수당',
            'bonus': '상여금',
            'total_payment': '총지급액',
        }
        for cell_key, data_key in payment_mapping.items():
            if cell_key in self.cell_mapping:
                value = payroll_data.get(data_key, 0)
                ws[self.cell_mapping[cell_key]] = value
        
        # 공제 항목 매핑
        deduction_mapping = {
            'national_pension': '국민연금',
            'health_insurance': '건강보험',
            'long_term_care': '장기요양',
            'employment_insurance': '고용보험',
            'income_tax': '소득세',
            'local_income_tax': '지방소득세',
            'total_deduction': '총공제액',
        }
        for cell_key, data_key in deduction_mapping.items():
            if cell_key in self.cell_mapping:
                value = payroll_data.get(data_key, 0)
                ws[self.cell_mapping[cell_key]] = value
        
        # 실수령액
        if 'net_pay' in self.cell_mapping:
            net_pay = payroll_data.get('실수령액', 0)
            ws[self.cell_mapping['net_pay']] = net_pay
    
    def generate_pdf(self, payroll_data, employee_data, output_path, period):
        """PDF 생성 (기본 디자인 사용 또는 엑셀 변환)"""
        # 초기 버전: 기본 PDF 생성 방식 사용
        # 향후: 템플릿 스타일을 반영한 PDF 생성 구현 가능
        from ...pdf_generator import PDFGenerator
        pdf_gen = PDFGenerator()
        return pdf_gen.generate_payslip(
            payroll_data, employee_data, output_path, period,
            use_template=False, design_name=None
        )
```

#### 1.2 TemplateSample1 클래스 생성
**파일**: `payroll_generator/templates/designs/template_sample1.py`

```python
# template_sample1.py
from .template_design import TemplateDesign
import logging

logger = logging.getLogger(__name__)

class TemplateSample1(TemplateDesign):
    """템플릿 샘플 1: 급여명세서_template.xlsx"""
    
    def __init__(self):
        super().__init__(
            template_filename='template_sample1.xlsx',
            mapping_filename='template_sample1_mapping.json'
        )
        logger.info("TemplateSample1 인스턴스 생성 완료")
```

#### 1.3 TemplateSample2 클래스 생성
**파일**: `payroll_generator/templates/designs/template_sample2.py`

```python
# template_sample2.py
from .template_design import TemplateDesign
import logging

logger = logging.getLogger(__name__)

class TemplateSample2(TemplateDesign):
    """템플릿 샘플 2: 임금명세서양식_template3.xlsx"""
    
    def __init__(self):
        super().__init__(
            template_filename='template_sample2.xlsx',
            mapping_filename='template_sample2_mapping.json'
        )
        logger.info("TemplateSample2 인스턴스 생성 완료")
```

**예상 소요 시간**: 3-4시간

**Git 커밋**:
```bash
git add payroll_generator/templates/designs/template_design.py
git add payroll_generator/templates/designs/template_sample1.py
git add payroll_generator/templates/designs/template_sample2.py
git commit -m "feat(template): Phase 1 - 템플릿 기반 디자인 클래스 구현

- TemplateDesign 기본 클래스 생성 (에러 처리, 폴백 전략 포함)
- TemplateSample1 클래스 생성
- TemplateSample2 클래스 생성
- 셀 매핑 JSON 파일 기반 데이터 채우기 로직 구현"
```

**머지**:
```bash
git checkout feature/template-designs
git merge --no-ff feature/template-designs-phase-1 -m "merge: Phase 1 완료"
```

---

### Phase 2: DesignFactory에 템플릿 디자인 등록

**브랜치**: `feature/template-designs-phase-2`

#### Git 명령어
```bash
git checkout feature/template-designs
git checkout -b feature/template-designs-phase-2
```

#### 2.1 DesignFactory 수정
**파일**: `payroll_generator/templates/designs/design_factory.py`

**변경 사항**:
```python
# design_factory.py에 추가
try:
    from .template_sample1 import TemplateSample1
except ImportError:
    try:
        from payroll_generator.templates.designs.template_sample1 import TemplateSample1
    except ImportError:
        TemplateSample1 = None

try:
    from .template_sample2 import TemplateSample2
except ImportError:
    try:
        from payroll_generator.templates.designs.template_sample2 import TemplateSample2
    except ImportError:
        TemplateSample2 = None

class DesignFactory:
    _designs = {
        'default': None,
        'design_1': Design1,
        'design_2': Design2,
        'template_sample1': TemplateSample1,  # 새로 추가
        'template_sample2': TemplateSample2,  # 새로 추가
    }
    # ... 나머지 코드 유지
```

**예상 소요 시간**: 30분

**Git 커밋**:
```bash
git add payroll_generator/templates/designs/design_factory.py
git commit -m "feat(template): Phase 2 - DesignFactory에 템플릿 디자인 등록

- TemplateSample1, TemplateSample2를 DesignFactory에 등록
- template_sample1, template_sample2 디자인 옵션 추가
- Import 에러 처리 추가"
```

**머지**:
```bash
git checkout feature/template-designs
git merge --no-ff feature/template-designs-phase-2 -m "merge: Phase 2 완료"
```

---

### Phase 3: UI 업데이트

**브랜치**: `feature/template-designs-phase-3`

#### Git 명령어
```bash
git checkout feature/template-designs
git checkout -b feature/template-designs-phase-3
```

#### 3.1 웹 인터페이스 업데이트
**파일**: 
- `app/forms/payroll_forms.py`
- `web/templates/payroll/input_form.html`
- `web/templates/payroll/multiple_input.html`

**변경 사항**:
```python
# app/forms/payroll_forms.py
design_name = StringField('디자인 선택', validators=[
    Optional()
], choices=[
    ('default', '기본 디자인'),
    ('design_1', '디자인 1'),
    ('design_2', '디자인 2'),
    ('template_sample1', '템플릿 1: 급여명세서'),  # 새로 추가
    ('template_sample2', '템플릿 2: 임금명세서'),  # 새로 추가
], default='default')
```

```html
<!-- web/templates/payroll/input_form.html -->
<select name="design_name" id="design_name" class="form-select">
    <option value="default">기본 디자인</option>
    <option value="design_1">디자인 1</option>
    <option value="design_2">디자인 2</option>
    <option value="template_sample1">템플릿 1: 급여명세서</option>
    <option value="template_sample2">템플릿 2: 임금명세서</option>
</select>
```

#### 3.2 데스크톱 인터페이스 업데이트
**파일**: `main.py`

**변경 사항**:
```python
# main.py의 디자인 선택 Combobox에 추가
design_options = [
    '기본 디자인',
    '디자인 1',
    '디자인 2',
    '템플릿 1: 급여명세서',  # 새로 추가
    '템플릿 2: 임금명세서',  # 새로 추가
]
```

**예상 소요 시간**: 1시간

**Git 커밋**:
```bash
git add app/forms/payroll_forms.py
git add web/templates/payroll/input_form.html
git add web/templates/payroll/multiple_input.html
git add main.py
git commit -m "feat(template): Phase 3 - UI 업데이트

- 웹 인터페이스 디자인 선택 옵션 추가 (template_sample1, template_sample2)
- 데스크톱 인터페이스 디자인 선택 옵션 추가
- 기존 디자인 옵션 유지"
```

**머지**:
```bash
git checkout feature/template-designs
git merge --no-ff feature/template-designs-phase-3 -m "merge: Phase 3 완료"
```

---

### Phase 4: 테스트 및 검증

**브랜치**: `feature/template-designs-phase-4`

#### Git 명령어
```bash
git checkout feature/template-designs
git checkout -b feature/template-designs-phase-4
```

#### 4.1 단위 테스트 작성
**파일**: `tests/test_template_design.py` (새로 생성)

**테스트 케이스**:
```python
# tests/test_template_design.py
import unittest
import os
import tempfile
from payroll_generator.templates.designs.template_design import TemplateDesign
from payroll_generator.templates.designs.template_sample1 import TemplateSample1
from payroll_generator.templates.designs.template_sample2 import TemplateSample2

class TestTemplateDesign(unittest.TestCase):
    def setUp(self):
        self.sample_payroll_data = {
            '기본급': 3000000,
            '연장근무수당': 500000,
            '상여금': 0,
            '총지급액': 3500000,
            '국민연금': 157500,
            '건강보험': 105000,
            '장기요양': 15750,
            '고용보험': 10500,
            '소득세': 50000,
            '지방소득세': 5000,
            '총공제액': 343750,
            '실수령액': 3156250,
        }
        self.sample_employee_data = {
            '이름': '홍길동',
            '주민번호': '123456-1234567',
            '입사일': '2020-01-01',
        }
    
    def test_template_sample1_init(self):
        """TemplateSample1 초기화 테스트"""
        design = TemplateSample1()
        self.assertIsNotNone(design.cell_mapping)
        self.assertEqual(design.template_filename, 'template_sample1.xlsx')
    
    def test_template_sample1_excel_generation(self):
        """TemplateSample1 엑셀 생성 테스트"""
        design = TemplateSample1()
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            output_path = tmp.name
        
        try:
            design.generate_excel(
                self.sample_payroll_data,
                self.sample_employee_data,
                output_path,
                '2025-01'
            )
            self.assertTrue(os.path.exists(output_path))
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_template_sample2_init(self):
        """TemplateSample2 초기화 테스트"""
        design = TemplateSample2()
        self.assertIsNotNone(design.cell_mapping)
        self.assertEqual(design.template_filename, 'template_sample2.xlsx')
    
    def test_cell_mapping_validation(self):
        """셀 매핑 검증 테스트"""
        design = TemplateSample1()
        required_keys = ['employee_name', 'basic_salary', 'net_pay']
        for key in required_keys:
            self.assertIn(key, design.cell_mapping, f"필수 셀 매핑 누락: {key}")

if __name__ == '__main__':
    unittest.main()
```

#### 4.2 통합 테스트
**파일**: `tests/test_template_integration.py` (새로 생성)

**테스트 케이스**:
- 웹 인터페이스에서 각 디자인 선택 테스트
- 데스크톱 인터페이스에서 각 디자인 선택 테스트
- 생성된 엑셀 파일 검증
- 기존 기능(기본 디자인, design_1, design_2) 정상 동작 확인

#### 4.3 회귀 테스트
- 기존 테스트 스위트 실행
- 모든 기존 기능 정상 동작 확인

**예상 소요 시간**: 2-3시간

**Git 커밋**:
```bash
git add tests/test_template_design.py
git add tests/test_template_integration.py
git commit -m "test(template): Phase 4 - 테스트 및 검증

- 템플릿 디자인 단위 테스트 추가
- 통합 테스트 추가
- 회귀 테스트 실행 및 확인"
```

**머지**:
```bash
git checkout feature/template-designs
git merge --no-ff feature/template-designs-phase-4 -m "merge: Phase 4 완료"
```

**최종 머지**:
```bash
git checkout develop
git merge --no-ff feature/template-designs -m "merge: 템플릿 디자인 기능 통합 완료"
```

---

## 🔧 구현 상세 및 베스트 프랙티스

### 1. 에러 처리 전략

#### 템플릿 파일 누락 시
```python
def _get_template_path(self):
    """템플릿 파일 경로 찾기"""
    # ... 경로 찾기 로직 ...
    
    # 모든 경로 실패 시
    raise FileNotFoundError(
        f"템플릿 파일을 찾을 수 없습니다: {self.template_filename}. "
        f"다음 경로를 시도했습니다: {paths_to_try}"
    )
```

#### 셀 매핑 누락 시
```python
def _fill_template_data(self, ws, payroll_data, employee_data, period):
    """템플릿에 데이터 채우기"""
    # 셀 매핑이 없으면 경고만 출력하고 계속 진행
    if not self.cell_mapping:
        logger.warning("셀 매핑이 비어있습니다. 기본 매핑을 사용합니다.")
        # 기본 매핑 사용 또는 예외 발생
```

### 2. 로깅 전략

```python
import logging

logger = logging.getLogger(__name__)

# 정보성 로그
logger.info(f"템플릿 기반 엑셀 생성 완료: {output_path}")

# 경고 로그
logger.warning(f"셀 매핑 파일을 찾을 수 없습니다: {mapping_filename}")

# 에러 로그
logger.error(f"엑셀 생성 실패: {e}", exc_info=True)
```

### 3. 셀 매핑 검증

```python
def validate_cell_mapping(self):
    """셀 매핑 유효성 검증"""
    required_keys = [
        'employee_name',
        'basic_salary',
        'net_pay'
    ]
    
    missing_keys = [key for key in required_keys if key not in self.cell_mapping]
    if missing_keys:
        raise ValueError(f"필수 셀 매핑 누락: {missing_keys}")
    
    return True
```

### 4. 병합된 셀 처리

템플릿에 병합된 셀이 있는 경우, 데이터를 채울 때 주의:
- 병합된 셀의 첫 번째 셀에만 데이터 쓰기
- 병합 범위는 유지

```python
# openpyxl은 병합된 셀의 첫 번째 셀에만 값을 쓸 수 있음
# 병합 범위는 자동으로 유지됨
ws[merged_cell_range.start_cell] = value
```

### 5. 수식 보존

템플릿에 수식이 있는 경우:
- 수식이 있는 셀은 건드리지 않음
- 수식이 참조하는 셀만 업데이트

```python
def _fill_template_data(self, ws, payroll_data, employee_data, period):
    """템플릿에 데이터 채우기"""
    # 수식이 있는 셀은 건드리지 않음
    # (분석 단계에서 formula_cells 리스트에 저장됨)
    # 수식이 참조하는 셀만 업데이트
```

---

## 📊 셀 매핑 분석 자동화

### 분석 스크립트 사용법

```bash
# 기본 사용법
python scripts/analyze_template_cells.py <템플릿_파일> [출력_JSON_파일]

# 예시
python scripts/analyze_template_cells.py \
    sample/급여명세서_template.xlsx \
    payroll_generator/templates/designs/configs/template_sample1_mapping.json
```

### 출력 JSON 형식

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
  },
  "merged_cells": [
    "A1:B1",
    "A2:B2"
  ],
  "formula_cells": [
    "B12",
    "B21",
    "A23"
  ],
  "sheet_name": "Sheet1"
}
```

### 수동 검증 필요 사항

자동 분석 후 다음 항목은 수동으로 확인 필요:
- [ ] 셀 위치 정확성 (실제 템플릿 파일과 비교)
- [ ] 데이터 타입 (숫자, 날짜, 텍스트)
- [ ] 포맷팅 요구사항 (천 단위 구분, 날짜 형식 등)

---

## 🔄 기존 기능 유지

### 현재 동작 유지
- `design_name=None` 또는 `'default'`: 기존 기본 디자인 사용
- `design_name='design_1'`: YAML 기반 디자인 1 사용
- `design_name='design_2'`: YAML 기반 디자인 2 사용

### 새로 추가되는 동작
- `design_name='template_sample1'`: 템플릿 샘플 1 사용
- `design_name='template_sample2'`: 템플릿 샘플 2 사용

---

## 📋 작업 체크리스트

### Phase 0: 준비 작업
- [ ] 템플릿 분석 스크립트 생성
- [ ] 템플릿 파일 분석 실행 (자동)
- [ ] 템플릿 파일 프로젝트에 복사
- [ ] 셀 매핑 JSON 파일 생성 및 검증

### Phase 1: 템플릿 기반 디자인 클래스 구현
- [ ] `TemplateDesign` 기본 클래스 생성
- [ ] `TemplateSample1` 클래스 생성
- [ ] `TemplateSample2` 클래스 생성
- [ ] 에러 처리 및 로깅 구현
- [ ] 셀 매핑 검증 로직 구현

### Phase 2: DesignFactory에 등록
- [ ] `DesignFactory`에 템플릿 디자인 등록
- [ ] Import 경로 수정
- [ ] 에러 처리 추가

### Phase 3: UI 업데이트
- [ ] 웹 인터페이스 디자인 선택 옵션 추가
- [ ] 데스크톱 인터페이스 디자인 선택 옵션 추가

### Phase 4: 테스트 및 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성
- [ ] 회귀 테스트 실행
- [ ] 기존 기능 정상 동작 확인

---

## ⚠️ 주의사항 및 리스크 관리

### 1. 셀 매핑 정확성
- **리스크**: 잘못된 셀 매핑으로 데이터가 잘못된 위치에 들어감
- **완화 방안**: 
  - 자동 분석 스크립트 사용
  - 수동 검증 필수
  - 단위 테스트로 검증
  - 샘플 데이터로 실제 생성 테스트

### 2. 템플릿 파일 호환성
- **리스크**: 템플릿 파일이 손상되거나 형식이 다를 수 있음
- **완화 방안**:
  - 파일 검증 로직 추가
  - 파일이 없을 경우 명확한 에러 메시지
  - 폴백 로직 구현 (기본 디자인 사용)

### 3. 기존 기능 유지
- **리스크**: 새 기능 추가 시 기존 기능이 깨질 수 있음
- **완화 방안**:
  - 기존 테스트 유지 및 실행
  - 각 Phase마다 회귀 테스트
  - 코드 리뷰 시 기존 기능 확인

### 4. PyInstaller 빌드
- **리스크**: 템플릿 파일이 실행 파일에 포함되지 않을 수 있음
- **완화 방안**:
  - `resource_path` 함수 사용
  - 빌드 후 테스트
  - 템플릿 파일 경로 검증

### 5. 수식 처리
- **리스크**: 템플릿의 수식이 깨질 수 있음
- **완화 방안**:
  - 수식이 있는 셀은 건드리지 않음
  - 수식이 참조하는 셀만 업데이트
  - 생성 후 수식 재계산 확인

---

## 📈 예상 소요 시간

| Phase | 작업 | 예상 시간 |
|-------|------|----------|
| Phase 0 | 준비 작업 (자동화 포함) | 1-2시간 |
| Phase 1 | 템플릿 디자인 클래스 구현 | 3-4시간 |
| Phase 2 | DesignFactory 등록 | 30분 |
| Phase 3 | UI 업데이트 | 1시간 |
| Phase 4 | 테스트 및 검증 | 2-3시간 |
| **총계** | | **7-10시간** |

---

## 🎯 다음 단계

### 즉시 시작 가능한 작업

1. **Git 브랜치 설정**
   ```bash
   git checkout develop
   git checkout -b feature/template-designs
   git checkout -b feature/template-designs-phase-0
   ```

2. **템플릿 분석 스크립트 생성**
   - `scripts/analyze_template_cells.py` 생성
   - 자동 셀 매핑 추출 기능 구현

3. **템플릿 파일 분석 실행**
   ```bash
   python scripts/analyze_template_cells.py sample/급여명세서_template.xlsx
   python scripts/analyze_template_cells.py sample/임금명세서양식_template3.xlsx
   ```

4. **템플릿 파일 복사**
   - `sample/급여명세서_template.xlsx` → `payroll_generator/templates/designs/template_sample1.xlsx`
   - `sample/임금명세서양식_template3.xlsx` → `payroll_generator/templates/designs/template_sample2.xlsx`

5. **코드 구현 시작**
   - Phase 1부터 순차적으로 진행

---

## 📊 작업 우선순위

### 필수 작업 (Phase 0-4)
1. ✅ Phase 0: 템플릿 파일 분석 및 복사 (자동화)
2. ✅ Phase 1: 템플릿 디자인 클래스 구현
3. ✅ Phase 2: DesignFactory 등록
4. ✅ Phase 3: UI 업데이트
5. ✅ Phase 4: 테스트 및 검증

---

## 📈 성공 기준

### 기능적 요구사항
- [ ] `template_sample1` 선택 시 `급여명세서_template.xlsx` 기반 엑셀 생성
- [ ] `template_sample2` 선택 시 `임금명세서양식_template3.xlsx` 기반 엑셀 생성
- [ ] 웹 인터페이스에서 두 템플릿 선택 가능
- [ ] 데스크톱 인터페이스에서 두 템플릿 선택 가능
- [ ] 기존 디자인(기본, design_1, design_2) 정상 동작

### 비기능적 요구사항
- [ ] 기존 기능 정상 동작 (회귀 테스트 통과)
- [ ] 코드 품질 유지 (린터 오류 없음)
- [ ] 테스트 커버리지 80% 이상
- [ ] 문서화 완료
- [ ] 에러 처리 및 로깅 완비

---

## 🔍 코드 품질 기준

### 린터
- `pylint` 점수 8.0 이상
- `flake8` 오류 없음
- `mypy` 타입 체크 통과 (선택사항)

### 테스트
- 단위 테스트 커버리지 80% 이상
- 통합 테스트 포함
- 회귀 테스트 통과

### 문서화
- 모든 공개 메서드 docstring 작성
- 타입 힌트 사용
- README 업데이트

---

**작성자**: AI Assistant  
**작성일**: 2025-12-12  
**버전**: 2.0  
**상태**: 📋 실행 계획 작성 완료 (프로 개발자 관점 개선)
