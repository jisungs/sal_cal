# Sample 템플릿 기본 디자인 통합 실행 계획

**작성일**: 2025-12-12  
**버전**: 2.0 (프로 개발자 관점 개선)  
**목적**: Sample 폴더의 두 엑셀 템플릿을 기본 디자인 옵션으로 추가  
**원칙**: 기존 기능 유지하면서 확장, Git 브랜치 전략을 통한 안전한 개발, 프로덕션 품질 보장

> **⚠️ 중요**: 이 문서는 v1.0을 프로 개발자 관점에서 실현 가능하도록 업그레이드한 버전입니다. 자동화된 분석 도구, 강화된 에러 처리, 구체적인 테스트 전략, 그리고 실제 구현 가능한 코드 예시를 포함합니다.  
> **📌 참고**: 상세한 기술 사양은 `sample_템플릿_기본_디자인_통합_실행계획_v2.md`를 참조하세요.

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

### 옵션 1: 템플릿 기반 디자인 클래스 생성 (권장)

새로운 템플릿 기반 디자인 클래스를 만들어 `DesignFactory`에 등록:

```
BaseDesign (추상 클래스)
├── Design1 (YAML 기반)
├── Design2 (YAML 기반)
├── TemplateDesign (템플릿 기반, 새로 추가)
    ├── TemplateSample1 (급여명세서_template.xlsx)
    └── TemplateSample2 (임금명세서양식_template3.xlsx)
```

**장점**:
- 기존 구조와 일관성 유지
- 확장성 좋음 (새 템플릿 추가 용이)
- `DesignFactory`를 통한 통합 관리

### 옵션 2: ExcelHandler에 템플릿 선택 기능 추가

`ExcelHandler`에 템플릿 파일 선택 기능 추가:

**장점**:
- 구현이 간단함
- 기존 코드 수정 최소화

**단점**:
- 디자인 선택 기능과의 일관성 부족
- PDF 생성과의 통합 복잡

**권장**: 옵션 1 (템플릿 기반 디자인 클래스 생성)

---

## 📝 실행 계획 (Git 브랜치 전략 포함)

### Phase 0: 준비 작업

**브랜치**: `feature/template-designs-phase-0`

#### Git 명령어
```bash
# 기능 브랜치 생성
git checkout develop
git checkout -b feature/template-designs
git checkout -b feature/template-designs-phase-0
```

#### 0.1 템플릿 파일 분석 및 셀 매핑 확인
- [ ] `sample/급여명세서_template.xlsx` 열어서 셀 구조 분석
- [ ] `sample/임금명세서양식_template3.xlsx` 열어서 셀 구조 분석
- [ ] 각 템플릿의 셀 위치 매핑 문서 작성
  - 제목, 기간, 직원 정보, 지급 항목, 공제 항목, 실수령액 셀 위치
- [ ] 스타일 정보 확인 (폰트, 색상, 테두리 등)

#### 0.2 템플릿 파일 프로젝트에 복사
- [ ] `sample/급여명세서_template.xlsx` → `payroll_generator/templates/designs/template_sample1.xlsx`
- [ ] `sample/임금명세서양식_template3.xlsx` → `payroll_generator/templates/designs/template_sample2.xlsx`
- [ ] Git에 추가

**예상 소요 시간**: 1-2시간

**Git 커밋**:
```bash
git add payroll_generator/templates/designs/template_sample*.xlsx
git commit -m "feat(template): Phase 0 - 템플릿 파일 프로젝트에 추가

- sample/급여명세서_template.xlsx → template_sample1.xlsx 복사
- sample/임금명세서양식_template3.xlsx → template_sample2.xlsx 복사
- 셀 매핑 분석 문서 작성"
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

**기능**:
- `BaseDesign` 상속
- 템플릿 파일 경로 관리
- 템플릿 파일 로드 및 데이터 채우기
- 셀 매핑 정보 관리

**구조**:
```python
class TemplateDesign(BaseDesign):
    """템플릿 기반 디자인 기본 클래스"""
    
    def __init__(self, template_filename, cell_mapping):
        self.template_filename = template_filename
        self.cell_mapping = cell_mapping
        super().__init__(config_path=None)  # YAML 설정 불필요
    
    def generate_excel(self, payroll_data, employee_data, output_path, period):
        """템플릿 파일을 사용하여 엑셀 생성"""
        # 템플릿 파일 로드
        # 셀 매핑에 따라 데이터 채우기
        # 파일 저장
    
    def generate_pdf(self, payroll_data, employee_data, output_path, period):
        """PDF 생성 (엑셀 생성 후 변환 또는 코드 기반)"""
        # 옵션 1: 엑셀 생성 후 PDF 변환
        # 옵션 2: 코드 기반 PDF 생성 (현재는 이 방식)
```

#### 1.2 TemplateSample1 클래스 생성
**파일**: `payroll_generator/templates/designs/template_sample1.py`

**기능**:
- `TemplateDesign` 상속
- `급여명세서_template.xlsx` 사용
- 셀 매핑 정보 정의

**셀 매핑 예시** (실제 분석 후 수정 필요):
```python
CELL_MAPPING = {
    'period': 'A2',
    'employee_name': 'B4',
    'resident_number': 'B5',
    'join_date': 'B6',
    'basic_salary': 'B9',
    'overtime': 'B10',
    'bonus': 'B11',
    'total_payment': 'B12',
    'national_pension': 'B15',
    'health_insurance': 'B16',
    # ... 나머지 셀 매핑
}
```

#### 1.3 TemplateSample2 클래스 생성
**파일**: `payroll_generator/templates/designs/template_sample2.py`

**기능**:
- `TemplateDesign` 상속
- `임금명세서양식_template3.xlsx` 사용
- 셀 매핑 정보 정의 (법적 요구사항 반영)

**예상 소요 시간**: 3-4시간

**Git 커밋**:
```bash
git add payroll_generator/templates/designs/template_design.py
git add payroll_generator/templates/designs/template_sample1.py
git add payroll_generator/templates/designs/template_sample2.py
git commit -m "feat(template): Phase 1 - 템플릿 기반 디자인 클래스 구현

- TemplateDesign 기본 클래스 생성
- TemplateSample1 클래스 생성 (급여명세서_template.xlsx)
- TemplateSample2 클래스 생성 (임금명세서양식_template3.xlsx)
- 셀 매핑 기반 데이터 채우기 로직 구현"
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
- `TemplateSample1`, `TemplateSample2` import 추가
- `_designs` 딕셔너리에 등록:
  ```python
  _designs = {
      'default': None,
      'design_1': Design1,
      'design_2': Design2,
      'template_sample1': TemplateSample1,  # 새로 추가
      'template_sample2': TemplateSample2,  # 새로 추가
  }
  ```

**예상 소요 시간**: 30분

**Git 커밋**:
```bash
git add payroll_generator/templates/designs/design_factory.py
git commit -m "feat(template): Phase 2 - DesignFactory에 템플릿 디자인 등록

- TemplateSample1, TemplateSample2를 DesignFactory에 등록
- template_sample1, template_sample2 디자인 옵션 추가"
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
- 디자인 선택 드롭다운에 옵션 추가:
  - 기본 디자인 (기존)
  - 디자인 1 (기존)
  - 디자인 2 (기존)
  - 템플릿 1: 급여명세서 (새로 추가)
  - 템플릿 2: 임금명세서 (새로 추가)

#### 3.2 데스크톱 인터페이스 업데이트
**파일**: `main.py`

**변경 사항**:
- 디자인 선택 Combobox에 옵션 추가

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

### Phase 4: PDF 생성 지원 (선택사항)

**브랜치**: `feature/template-designs-phase-4` (선택사항)

#### Git 명령어
```bash
git checkout feature/template-designs
git checkout -b feature/template-designs-phase-4
```

#### 4.1 템플릿 기반 PDF 생성
**옵션 A**: 엑셀 생성 후 PDF 변환
- 엑셀→PDF 변환 라이브러리 필요 (예: xlsx2pdf, win32com)
- 플랫폼 의존성 문제 가능

**옵션 B**: 코드 기반 PDF 생성 (권장)
- 템플릿의 스타일을 YAML로 추출
- `design_1.py`, `design_2.py`와 유사한 방식으로 PDF 생성
- 플랫폼 독립적

**권장**: 옵션 B (코드 기반 PDF 생성)

**예상 소요 시간**: 2-3시간 (선택사항)

**Git 커밋**:
```bash
git add payroll_generator/templates/designs/template_sample*.py
git commit -m "feat(template): Phase 4 - PDF 생성 지원 추가

- 템플릿 기반 PDF 생성 구현 (코드 기반 또는 엑셀 변환)"
```

**머지**:
```bash
git checkout feature/template-designs
git merge --no-ff feature/template-designs-phase-4 -m "merge: Phase 4 완료"
```

---

### Phase 5: 테스트 및 검증

**브랜치**: `feature/template-designs-phase-5`

#### Git 명령어
```bash
git checkout feature/template-designs
git checkout -b feature/template-designs-phase-5
```

#### 5.1 단위 테스트
- [ ] `TemplateDesign` 클래스 테스트
- [ ] `TemplateSample1` 클래스 테스트
- [ ] `TemplateSample2` 클래스 테스트
- [ ] 셀 매핑 정확성 확인

#### 5.2 통합 테스트
- [ ] 웹 인터페이스에서 각 디자인 선택 테스트
- [ ] 데스크톱 인터페이스에서 각 디자인 선택 테스트
- [ ] 생성된 엑셀 파일 검증
- [ ] 기존 기능(기본 디자인, design_1, design_2) 정상 동작 확인

**예상 소요 시간**: 2-3시간

**Git 커밋**:
```bash
git add tests/
git commit -m "test(template): Phase 5 - 테스트 및 검증

- 템플릿 디자인 단위 테스트 추가
- 통합 테스트 추가
- 기존 기능 정상 동작 확인"
```

**머지**:
```bash
git checkout feature/template-designs
git merge --no-ff feature/template-designs-phase-5 -m "merge: Phase 5 완료"
```

**최종 머지**:
```bash
git checkout develop
git merge --no-ff feature/template-designs -m "merge: 템플릿 디자인 기능 통합 완료"
```

---

## 🔧 구현 상세

### 1. TemplateDesign 기본 클래스

```python
# template_design.py
import openpyxl
from .base_design import BaseDesign
from pathlib import Path
import os

class TemplateDesign(BaseDesign):
    """템플릿 기반 디자인 기본 클래스"""
    
    def __init__(self, template_filename, cell_mapping):
        """
        Args:
            template_filename: 템플릿 파일명 (예: 'template_sample1.xlsx')
            cell_mapping: 셀 위치 매핑 딕셔너리
        """
        self.template_filename = template_filename
        self.cell_mapping = cell_mapping
        super().__init__(config_path=None)  # YAML 설정 불필요
    
    def _get_template_path(self):
        """템플릿 파일 경로 찾기"""
        # 여러 경로 시도 (PyInstaller 환경, 개발 환경)
        paths_to_try = [
            # PyInstaller 환경
            resource_path(f'templates/designs/{self.template_filename}'),
            # 개발 환경
            os.path.join(os.path.dirname(__file__), self.template_filename),
        ]
        
        for path in paths_to_try:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError(f"템플릿 파일을 찾을 수 없습니다: {self.template_filename}")
    
    def generate_excel(self, payroll_data, employee_data, output_path, period):
        """템플릿 파일을 사용하여 엑셀 생성"""
        template_path = self._get_template_path()
        wb = openpyxl.load_workbook(template_path)
        ws = wb.active
        
        # 셀 매핑에 따라 데이터 채우기
        self._fill_template_data(ws, payroll_data, employee_data, period)
        
        # 파일 저장
        wb.save(output_path)
        wb.close()
    
    def _fill_template_data(self, ws, payroll_data, employee_data, period):
        """템플릿에 데이터 채우기"""
        # 기간
        if 'period' in self.cell_mapping and period:
            ws[self.cell_mapping['period']] = f"지급기간: {period}"
        
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
        
        # 지급 항목
        payment_mapping = {
            'basic_salary': '기본급',
            'overtime': '연장근무수당',
            'bonus': '상여금',
            'total_payment': '총지급액',
        }
        for cell_key, data_key in payment_mapping.items():
            if cell_key in self.cell_mapping:
                ws[self.cell_mapping[cell_key]] = payroll_data.get(data_key, 0)
        
        # 공제 항목
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
                ws[self.cell_mapping[cell_key]] = payroll_data.get(data_key, 0)
        
        # 실수령액
        if 'net_pay' in self.cell_mapping:
            net_pay = payroll_data.get('실수령액', 0)
            ws[self.cell_mapping['net_pay']] = net_pay
    
    def generate_pdf(self, payroll_data, employee_data, output_path, period):
        """PDF 생성 (코드 기반 또는 엑셀 변환)"""
        # 현재는 코드 기반 PDF 생성으로 구현
        # 향후 엑셀→PDF 변환 지원 가능
        # 임시로 design_1 스타일 사용 또는 기본 PDF 생성
        from ..pdf_generator import PDFGenerator
        pdf_gen = PDFGenerator()
        return pdf_gen.generate_payslip(
            payroll_data, employee_data, output_path, period, 
            use_template=False, design_name=None
        )
```

### 2. TemplateSample1 클래스

```python
# template_sample1.py
from .template_design import TemplateDesign

class TemplateSample1(TemplateDesign):
    """템플릿 샘플 1: 급여명세서_template.xlsx"""
    
    # 셀 매핑 (실제 분석 후 수정 필요)
    CELL_MAPPING = {
        'period': 'A2',
        'employee_name': 'B4',
        'resident_number': 'B5',
        'join_date': 'B6',
        'basic_salary': 'B9',
        'overtime': 'B10',
        'bonus': 'B11',
        'total_payment': 'B12',
        'national_pension': 'B15',
        'health_insurance': 'B16',
        'long_term_care': 'B17',
        'employment_insurance': 'B18',
        'income_tax': 'B19',
        'local_income_tax': 'B20',
        'total_deduction': 'B21',
        'net_pay': 'A23',
    }
    
    def __init__(self):
        super().__init__(
            template_filename='template_sample1.xlsx',
            cell_mapping=self.CELL_MAPPING
        )
```

### 3. TemplateSample2 클래스

```python
# template_sample2.py
from .template_design import TemplateDesign

class TemplateSample2(TemplateDesign):
    """템플릿 샘플 2: 임금명세서양식_template3.xlsx"""
    
    # 셀 매핑 (실제 분석 후 수정 필요)
    CELL_MAPPING = {
        # 실제 분석 후 셀 위치 확인 필요
        'period': 'A2',
        'employee_name': 'B4',
        # ... 나머지 셀 매핑
    }
    
    def __init__(self):
        super().__init__(
            template_filename='template_sample2.xlsx',
            cell_mapping=self.CELL_MAPPING
        )
```

---

## 📊 셀 매핑 분석 필요 사항

각 템플릿 파일을 열어서 다음 정보를 확인해야 합니다:

### 급여명세서_template.xlsx
- [ ] 제목 셀 위치
- [ ] 기간 셀 위치
- [ ] 직원 정보 셀 위치 (이름, 주민번호, 입사일)
- [ ] 지급 항목 셀 위치 (기본급, 연장근무수당, 상여금, 총 지급액)
- [ ] 공제 항목 셀 위치 (국민연금, 건강보험, 장기요양, 고용보험, 소득세, 지방소득세, 총 공제액)
- [ ] 실수령액 셀 위치
- [ ] 병합된 셀 정보
- [ ] 수식이 있는 셀

### 임금명세서양식_template3.xlsx
- [ ] 위와 동일한 항목들
- [ ] 추가로 계산 방법 기재 셀 위치 (법적 요구사항)
- [ ] 연장·야간·휴일근로수당 상세 정보 셀 위치

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
- [ ] 템플릿 파일 분석 (셀 매핑 확인)
- [ ] 템플릿 파일 프로젝트에 복사
- [ ] 셀 매핑 문서 작성

### Phase 1: 템플릿 기반 디자인 클래스 구현
- [ ] `TemplateDesign` 기본 클래스 생성
- [ ] `TemplateSample1` 클래스 생성
- [ ] `TemplateSample2` 클래스 생성
- [ ] 셀 매핑 정보 구현

### Phase 2: DesignFactory에 등록
- [ ] `DesignFactory`에 템플릿 디자인 등록
- [ ] Import 경로 수정

### Phase 3: UI 업데이트
- [ ] 웹 인터페이스 디자인 선택 옵션 추가
- [ ] 데스크톱 인터페이스 디자인 선택 옵션 추가

### Phase 4: PDF 생성 지원 (선택사항)
- [ ] 템플릿 기반 PDF 생성 구현

### Phase 5: 테스트 및 검증
- [ ] 단위 테스트
- [ ] 통합 테스트
- [ ] 기존 기능 정상 동작 확인

---

## ⚠️ 주의사항

### 1. 셀 매핑 정확성
- 각 템플릿의 셀 위치를 정확히 확인해야 함
- 잘못된 셀 매핑은 데이터가 잘못된 위치에 들어갈 수 있음

### 2. 템플릿 파일 호환성
- 템플릿 파일이 손상되지 않았는지 확인
- PyInstaller 빌드 시 템플릿 파일이 포함되는지 확인

### 3. 기존 기능 유지
- 기존 기본 디자인(`payroll_template.xlsx`) 동작 유지
- `design_1`, `design_2` 동작 유지

### 4. PDF 생성
- 템플릿 기반 PDF 생성은 복잡할 수 있음
- 초기에는 엑셀만 지원하고 PDF는 기본 방식 사용 가능

---

## 📈 예상 소요 시간

| Phase | 작업 | 예상 시간 |
|-------|------|----------|
| Phase 0 | 준비 작업 | 1-2시간 |
| Phase 1 | 템플릿 디자인 클래스 구현 | 3-4시간 |
| Phase 2 | DesignFactory 등록 | 30분 |
| Phase 3 | UI 업데이트 | 1시간 |
| Phase 4 | PDF 생성 지원 (선택) | 2-3시간 |
| Phase 5 | 테스트 및 검증 | 2-3시간 |
| **총계** | | **9-13시간** (PDF 제외 시 7-10시간) |

---

## 🎯 다음 단계

### 즉시 시작 가능한 작업

1. **Git 브랜치 설정**
   ```bash
   git checkout develop
   git checkout -b feature/template-designs
   git checkout -b feature/template-designs-phase-0
   ```

2. **템플릿 파일 분석** (가장 중요)
   - 엑셀 파일을 열어 셀 구조 정확히 파악
   - 셀 매핑 문서 작성
   - `scripts/analyze_sample_templates.py` 실행 (openpyxl 설치 필요)

3. **템플릿 파일 복사**
   - `sample/급여명세서_template.xlsx` → `payroll_generator/templates/designs/template_sample1.xlsx`
   - `sample/임금명세서양식_template3.xlsx` → `payroll_generator/templates/designs/template_sample2.xlsx`

4. **코드 구현 시작**
   - Phase 1부터 순차적으로 진행

---

## 📊 작업 우선순위

### 필수 작업 (Phase 0-3)
1. ✅ Phase 0: 템플릿 파일 분석 및 복사
2. ✅ Phase 1: 템플릿 디자인 클래스 구현
3. ✅ Phase 2: DesignFactory 등록
4. ✅ Phase 3: UI 업데이트

### 선택 작업 (Phase 4)
- PDF 생성 지원 (엑셀만 지원해도 초기 버전은 가능)

### 필수 작업 (Phase 5)
- 테스트 및 검증

---

## ⚠️ 주의사항 및 리스크

### 1. 셀 매핑 정확성
- **리스크**: 잘못된 셀 매핑으로 데이터가 잘못된 위치에 들어감
- **완화 방안**: 
  - 템플릿 파일을 직접 열어 정확한 셀 위치 확인
  - 샘플 데이터로 테스트하여 검증

### 2. 템플릿 파일 호환성
- **리스크**: 템플릿 파일이 손상되거나 형식이 다를 수 있음
- **완화 방안**:
  - 파일 검증 로직 추가
  - 파일이 없을 경우 폴백 로직 구현

### 3. 기존 기능 유지
- **리스크**: 새 기능 추가 시 기존 기능이 깨질 수 있음
- **완화 방안**:
  - 기존 테스트 유지
  - 각 Phase마다 기존 기능 테스트

### 4. PDF 생성 복잡성
- **리스크**: 템플릿 기반 PDF 생성이 복잡할 수 있음
- **완화 방안**:
  - 초기에는 엑셀만 지원
  - PDF는 기본 방식 사용 또는 나중에 구현

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
- [ ] 문서화 완료

---

**작성자**: AI Assistant  
**작성일**: 2025-12-12  
**상태**: 📋 실행 계획 작성 완료 (Git 브랜치 전략 포함)
