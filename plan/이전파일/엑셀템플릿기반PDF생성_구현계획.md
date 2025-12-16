# 📋 엑셀 템플릿 기반 PDF 생성 기능 구현 계획

**작성일**: 2025-11-11  
**목표**: 엑셀 템플릿을 활용하여 PDF 파일을 생성

---

## 📊 현재 상태 분석

### ✅ 현재 구현된 기능

1. **PDF 생성**
   - `pdf_generator.py`에서 reportlab으로 코드 기반 PDF 생성
   - 레이아웃과 스타일이 코드에 하드코딩됨

2. **엑셀 템플릿**
   - `payroll_generator/templates/employee_template.xlsx`: 직원 정보 입력 템플릿
   - `payroll_generator/templates/company_template.xlsx`: 회사 정보 템플릿
   - `excel_handler.py`의 `write_payroll()` 메서드로 엑셀 급여명세서 생성

3. **엑셀 급여명세서 생성**
   - `write_payroll()` 메서드로 엑셀 파일 생성
   - 스타일링 및 레이아웃 적용

### ❌ 현재 미구현 기능

1. **엑셀 템플릿 기반 PDF 생성**
   - 엑셀 템플릿 파일을 사용한 PDF 생성 없음
   - 엑셀 파일을 PDF로 변환하는 기능 없음

---

## 🎯 구현 목표

### 주요 목표

1. **엑셀 템플릿 기반 PDF 생성**
   - 엑셀 템플릿 파일을 읽어서 데이터 채우기
   - 엑셀 파일을 PDF로 변환
   - 템플릿의 레이아웃과 스타일 유지

2. **템플릿 관리**
   - PDF용 엑셀 템플릿 파일 생성
   - 템플릿 파일 관리 및 버전 관리

3. **기존 기능과의 통합**
   - 기존 PDF 생성 방식과 병행 사용 가능
   - 사용자가 선택할 수 있도록 옵션 제공

---

## 📋 구현 방법 비교

### 방법 1: openpyxl + reportlab (권장)

**장점**:
- 엑셀 템플릿의 레이아웃을 읽어서 reportlab으로 재현
- 템플릿의 스타일(색상, 폰트, 테두리 등)을 PDF에 반영 가능
- 세밀한 제어 가능

**단점**:
- 구현 복잡도 높음
- 엑셀의 모든 스타일을 PDF로 변환하기 어려움

### 방법 2: openpyxl + xlsxwriter + 엑셀→PDF 변환 라이브러리

**장점**:
- 엑셀 파일을 직접 PDF로 변환
- 템플릿의 모든 스타일 유지
- 구현이 상대적으로 간단

**단점**:
- 추가 라이브러리 필요 (예: `xlsx2pdf`, `win32com` 등)
- 플랫폼 의존성 가능성 (Windows의 경우 win32com 사용)

### 방법 3: openpyxl로 엑셀 생성 → LibreOffice/Excel로 PDF 변환

**장점**:
- 엑셀 파일을 그대로 PDF로 변환
- 스타일 완벽 유지

**단점**:
- 외부 프로그램 필요
- 자동화 어려움

### 방법 4: 엑셀 템플릿 읽기 → reportlab으로 동일 레이아웃 PDF 생성 (선택)

**장점**:
- 순수 Python 라이브러리만 사용
- 플랫폼 독립적
- 세밀한 제어 가능

**단점**:
- 구현 복잡도 높음
- 템플릿 변경 시 코드 수정 필요

---

## 🎯 권장 구현 방법

### 방법 2: openpyxl + xlsx2pdf (또는 유사 라이브러리)

**이유**:
- 엑셀 파일을 직접 PDF로 변환하여 스타일 유지
- 구현이 상대적으로 간단
- 템플릿 변경 시 코드 수정 최소화

**대안 라이브러리**:
1. `xlsx2pdf` (openpyxl 기반)
2. `win32com` (Windows 전용, Excel 설치 필요)
3. `comtypes` (Windows 전용)
4. `LibreOffice` 명령줄 도구 (크로스 플랫폼, LibreOffice 설치 필요)

---

## 📋 구현 계획

### 1. PDF용 엑셀 템플릿 생성

#### 1.1 템플릿 파일 구조

**파일명**: `payroll_template_pdf.xlsx`  
**저장 위치**: `payroll_generator/templates/payroll_template_pdf.xlsx`

**시트 구조**:
- 시트 1: 급여명세서 (PDF 출력용)

**레이아웃**:
```
┌─────────────────────────────────────────┐
│           급여명세서 (제목)              │
│         지급기간: YYYY-MM                │
├─────────────────────────────────────────┤
│ 직원 정보                                │
│ - 성명: [이름]                          │
│ - 주민번호: [주민번호]                   │
│ - 입사일: [입사일]                       │
├─────────────────────────────────────────┤
│ 지급 항목                                │
│ ┌──────────────┬──────────────┐        │
│ │ 항목명       │ 금액         │        │
│ ├──────────────┼──────────────┤        │
│ │ 기본급       │ [금액]       │        │
│ │ 연장근무수당 │ [금액]       │        │
│ │ 상여금       │ [금액]       │        │
│ │ 총 지급액    │ [금액]       │        │
│ └──────────────┴──────────────┘        │
├─────────────────────────────────────────┤
│ 공제 항목                                │
│ ┌──────────────┬──────────────┐        │
│ │ 항목명       │ 금액         │        │
│ ├──────────────┼──────────────┤        │
│ │ 국민연금     │ [금액]       │        │
│ │ 건강보험     │ [금액]       │        │
│ │ ...          │ ...          │        │
│ │ 총 공제액    │ [금액]       │        │
│ └──────────────┴──────────────┘        │
├─────────────────────────────────────────┤
│ 실수령액: [금액] (강조)                  │
└─────────────────────────────────────────┘
```

#### 1.2 템플릿 파일 생성

- 기존 `write_payroll()` 메서드로 생성되는 엑셀 파일을 참고
- PDF 출력에 최적화된 레이아웃으로 템플릿 작성
- 스타일링 (색상, 폰트, 테두리 등) 적용

---

### 2. 엑셀→PDF 변환 라이브러리 선택 및 설치

#### 2.1 라이브러리 옵션

**옵션 1: xlsx2pdf (권장)**
```bash
pip install xlsx2pdf
```
- openpyxl 기반
- 크로스 플랫폼
- 엑셀 파일을 PDF로 직접 변환

**옵션 2: win32com (Windows 전용)**
```bash
pip install pywin32
```
- Windows Excel 사용
- 완벽한 스타일 유지
- Windows 전용

**옵션 3: LibreOffice 명령줄 (크로스 플랫폼)**
- LibreOffice 설치 필요
- `libreoffice --headless --convert-to pdf` 명령 사용

#### 2.2 라이브러리 선택 기준

1. **크로스 플랫폼 지원**: macOS, Windows, Linux 모두 지원
2. **의존성 최소화**: 추가 프로그램 설치 불필요
3. **스타일 유지**: 엑셀의 스타일이 PDF에 반영

**권장**: `xlsx2pdf` 또는 LibreOffice 명령줄

---

### 3. PDFGenerator 클래스 수정

#### 3.1 템플릿 기반 PDF 생성 메서드 추가

**파일**: `payroll_generator/pdf_generator.py`  
**메서드**: `generate_payslip_from_template()`

```python
def generate_payslip_from_template(self, payroll_data, employee_data, output_path, period):
    """엑셀 템플릿을 사용하여 PDF 생성
    
    Args:
        payroll_data (dict): calculator.calculate_deductions()의 반환값
        employee_data (dict): 직원 정보
        output_path (str): 출력 PDF 파일 경로
        period (str): 급여 기간
    """
    # 1. 템플릿 파일 경로 확인
    # 2. 템플릿 파일 복사 (임시 파일)
    # 3. openpyxl로 템플릿 읽기
    # 4. 데이터 채우기
    # 5. 엑셀 파일 저장
    # 6. 엑셀 파일을 PDF로 변환
    # 7. 임시 파일 삭제
```

#### 3.2 기존 메서드와의 통합

**옵션 1**: 기존 `generate_payslip()` 메서드에 템플릿 사용 옵션 추가
```python
def generate_payslip(self, payroll_data, employee_data, output_path, period, use_template=False):
    """급여명세서 PDF 생성
    
    Args:
        use_template (bool): True면 엑셀 템플릿 사용, False면 코드 기반 생성
    """
    if use_template:
        return self.generate_payslip_from_template(...)
    else:
        # 기존 코드 기반 생성
        ...
```

**옵션 2**: 별도 메서드로 분리하고 호출부에서 선택
```python
# main.py에서
if use_excel_template:
    pdf_generator.generate_payslip_from_template(...)
else:
    pdf_generator.generate_payslip(...)
```

---

### 4. 엑셀 템플릿 데이터 채우기

#### 4.1 템플릿 셀 위치 정의

**방법 1: 고정 셀 위치 사용**
```python
TEMPLATE_CELLS = {
    'title': 'A1',
    'period': 'A2',
    'employee_name': 'B5',
    'resident_number': 'B6',
    'join_date': 'B7',
    'basic_salary': 'C10',
    'overtime': 'C11',
    # ...
}
```

**방법 2: 셀 이름(Named Range) 사용**
```python
# 엑셀에서 셀 이름 정의
# - 이름: "EmployeeName" → 셀: B5
# - 이름: "BasicSalary" → 셀: C10
```

**방법 3: 키워드 검색**
```python
# 템플릿에서 "[이름]", "[기본급]" 같은 플레이스홀더 검색하여 교체
```

#### 4.2 데이터 채우기 로직

```python
def fill_template_data(self, template_path, payroll_data, employee_data, period):
    """템플릿에 데이터 채우기"""
    from openpyxl import load_workbook
    
    wb = load_workbook(template_path)
    ws = wb.active
    
    # 데이터 채우기
    ws['A1'] = '급여명세서'  # 제목
    ws['A2'] = f'지급기간: {period}'  # 기간
    ws['B5'] = employee_data.get('이름', '')  # 이름
    ws['B6'] = mask_resident_number(employee_data.get('주민번호', ''))  # 주민번호
    ws['C10'] = payroll_data.get('기본급', 0)  # 기본급
    # ... 나머지 데이터
    
    return wb
```

---

### 5. 엑셀→PDF 변환 구현

#### 5.1 xlsx2pdf 사용 (권장)

```python
from xlsx2pdf import xlsx2pdf

def convert_excel_to_pdf(self, excel_path, pdf_path):
    """엑셀 파일을 PDF로 변환"""
    try:
        xlsx2pdf(excel_path, pdf_path)
        logger.info(f"엑셀→PDF 변환 완료: {pdf_path}")
    except Exception as e:
        logger.error(f"엑셀→PDF 변환 실패: {e}")
        raise
```

#### 5.2 LibreOffice 명령줄 사용

```python
import subprocess
import os

def convert_excel_to_pdf_libreoffice(self, excel_path, pdf_path):
    """LibreOffice를 사용하여 엑셀을 PDF로 변환"""
    try:
        output_dir = os.path.dirname(pdf_path)
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            excel_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        
        # LibreOffice는 원본 파일명을 기반으로 PDF 생성
        base_name = os.path.splitext(os.path.basename(excel_path))[0]
        generated_pdf = os.path.join(output_dir, f"{base_name}.pdf")
        
        # 원하는 경로로 이동
        if generated_pdf != pdf_path:
            os.rename(generated_pdf, pdf_path)
        
        logger.info(f"엑셀→PDF 변환 완료: {pdf_path}")
    except FileNotFoundError:
        raise ValueError("LibreOffice가 설치되어 있지 않습니다.")
    except Exception as e:
        logger.error(f"엑셀→PDF 변환 실패: {e}")
        raise
```

#### 5.3 win32com 사용 (Windows 전용)

```python
import win32com.client

def convert_excel_to_pdf_win32com(self, excel_path, pdf_path):
    """Windows Excel을 사용하여 엑셀을 PDF로 변환"""
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        
        wb = excel.Workbooks.Open(os.path.abspath(excel_path))
        wb.ExportAsFixedFormat(0, os.path.abspath(pdf_path))  # 0 = PDF
        wb.Close(False)
        excel.Quit()
        
        logger.info(f"엑셀→PDF 변환 완료: {pdf_path}")
    except Exception as e:
        logger.error(f"엑셀→PDF 변환 실패: {e}")
        raise
```

---

### 6. 플랫폼별 변환 방법 선택

#### 6.1 자동 감지 및 선택

```python
import platform

def get_converter(self):
    """플랫폼에 맞는 변환기 반환"""
    system = platform.system()
    
    if system == 'Windows':
        # win32com 시도, 실패하면 xlsx2pdf
        try:
            import win32com.client
            return 'win32com'
        except ImportError:
            return 'xlsx2pdf'
    else:
        # macOS/Linux: LibreOffice 시도, 실패하면 xlsx2pdf
        try:
            subprocess.run(['libreoffice', '--version'], 
                         capture_output=True, check=True)
            return 'libreoffice'
        except (FileNotFoundError, subprocess.CalledProcessError):
            return 'xlsx2pdf'
```

---

## 🔄 구현 단계

### 단계 1: PDF용 엑셀 템플릿 생성
**예상 시간**: 1시간

**작업 내용**:
- [ ] `payroll_template_pdf.xlsx` 템플릿 파일 생성
- [ ] 레이아웃 설계 (제목, 직원 정보, 지급/공제 항목, 실수령액)
- [ ] 스타일링 적용 (색상, 폰트, 테두리)
- [ ] 셀 위치 또는 셀 이름 정의

### 단계 2: 엑셀→PDF 변환 라이브러리 선택 및 설치
**예상 시간**: 30분

**작업 내용**:
- [ ] 라이브러리 비교 및 선택
- [ ] `requirements.txt`에 추가
- [ ] 설치 및 테스트

### 단계 3: 템플릿 데이터 채우기 기능 구현
**예상 시간**: 2시간

**작업 내용**:
- [ ] 템플릿 파일 읽기 메서드
- [ ] 데이터 채우기 메서드 구현
- [ ] 셀 위치 매핑 정의
- [ ] 데이터 형식 변환 (숫자, 날짜 등)

### 단계 4: 엑셀→PDF 변환 기능 구현
**예상 시간**: 1시간 30분

**작업 내용**:
- [ ] 플랫폼 감지 로직
- [ ] 변환기 선택 로직
- [ ] xlsx2pdf 변환 구현
- [ ] LibreOffice 변환 구현 (선택)
- [ ] win32com 변환 구현 (Windows, 선택)

### 단계 5: PDFGenerator 클래스 통합
**예상 시간**: 1시간

**작업 내용**:
- [ ] `generate_payslip_from_template()` 메서드 구현
- [ ] 기존 `generate_payslip()` 메서드와 통합
- [ ] 에러 처리 및 로깅

### 단계 6: main.py 통합
**예상 시간**: 30분

**작업 내용**:
- [ ] PDF 생성 방식 선택 옵션 추가 (선택 사항)
- [ ] 기본값 설정 (템플릿 사용 또는 코드 기반)
- [ ] UI 옵션 추가 (선택 사항)

### 단계 7: 테스트
**예상 시간**: 1시간

**테스트 항목**:
- [ ] 템플릿 파일 읽기 테스트
- [ ] 데이터 채우기 테스트
- [ ] 엑셀→PDF 변환 테스트
- [ ] 생성된 PDF 파일 확인
- [ ] 스타일 유지 확인
- [ ] 플랫폼별 동작 확인

### 단계 8: 에러 처리 및 예외 상황
**예상 시간**: 30분

**작업 내용**:
- [ ] 템플릿 파일 없을 때 처리
- [ ] 변환 실패 시 폴백 (기존 방식 사용)
- [ ] 플랫폼별 에러 처리

---

## 📝 구현 상세

### 1. PDF용 엑셀 템플릿 구조

**파일**: `payroll_generator/templates/payroll_template_pdf.xlsx`

**시트 레이아웃 예시**:

| 셀 | 내용 | 데이터 소스 |
|----|------|------------|
| A1 | 급여명세서 | 고정 |
| A2 | 지급기간: {period} | period 파라미터 |
| A4 | 성명: | 고정 |
| B4 | {이름} | employee_data['이름'] |
| A5 | 주민번호: | 고정 |
| B5 | {주민번호} | employee_data['주민번호'] (마스킹) |
| A7 | 지급 항목 | 고정 |
| B8 | 기본급 | 고정 |
| C8 | {기본급} | payroll_data['기본급'] |
| B9 | 연장근무수당 | 고정 |
| C9 | {연장근무수당} | payroll_data['연장근무수당'] |
| ... | ... | ... |

### 2. 템플릿 데이터 채우기 구현

```python
# payroll_generator/pdf_generator.py

TEMPLATE_CELL_MAPPING = {
    # 제목 및 기간
    'title': ('A1', '급여명세서'),
    'period': ('A2', None),  # 동적 값
    
    # 직원 정보
    'employee_name_label': ('A4', '성명:'),
    'employee_name': ('B4', None),
    'resident_number_label': ('A5', '주민번호:'),
    'resident_number': ('B5', None),
    'join_date_label': ('A6', '입사일:'),
    'join_date': ('B6', None),
    
    # 지급 항목
    'payment_header': ('A7', '지급 항목'),
    'basic_salary_label': ('B8', '기본급'),
    'basic_salary': ('C8', None),
    'overtime_label': ('B9', '연장근무수당'),
    'overtime': ('C9', None),
    'bonus_label': ('B10', '상여금'),
    'bonus': ('C10', None),
    'total_payment_label': ('B11', '총 지급액'),
    'total_payment': ('C11', None),
    
    # 공제 항목
    'deduction_header': ('A13', '공제 항목'),
    'national_pension_label': ('B14', '국민연금'),
    'national_pension': ('C14', None),
    # ... 나머지 공제 항목
    
    # 실수령액
    'net_pay_label': ('A20', '실수령액:'),
    'net_pay': ('B20', None),
}

def fill_template_data(self, template_path, payroll_data, employee_data, period):
    """템플릿에 데이터 채우기"""
    from openpyxl import load_workbook
    from .utils import mask_resident_number
    
    wb = load_workbook(template_path)
    ws = wb.active
    
    # 데이터 매핑
    data_map = {
        'period': f'지급기간: {period}',
        'employee_name': employee_data.get('이름', ''),
        'resident_number': mask_resident_number(employee_data.get('주민번호', '')),
        'join_date': employee_data.get('입사일', ''),
        'basic_salary': payroll_data.get('기본급', 0),
        'overtime': payroll_data.get('연장근무수당', 0),
        'bonus': payroll_data.get('상여금', 0),
        'total_payment': payroll_data.get('총지급액', 0),
        'national_pension': payroll_data.get('국민연금', 0),
        # ... 나머지 데이터
        'net_pay': payroll_data.get('실수령액', 0),
    }
    
    # 템플릿 채우기
    for key, (cell, default_value) in TEMPLATE_CELL_MAPPING.items():
        if default_value is not None:
            # 고정 값
            ws[cell] = default_value
        elif key in data_map:
            # 동적 값
            value = data_map[key]
            if isinstance(value, (int, float)) and key.endswith('_label') == False:
                ws[cell] = value
                # 숫자 형식 적용
                ws[cell].number_format = '#,##0'
            else:
                ws[cell] = value
    
    return wb
```

### 3. 엑셀→PDF 변환 통합

```python
def generate_payslip_from_template(self, payroll_data, employee_data, output_path, period):
    """엑셀 템플릿을 사용하여 PDF 생성"""
    import tempfile
    import shutil
    
    try:
        # 템플릿 파일 경로
        template_path = os.path.join(
            os.path.dirname(__file__), 
            'templates', 
            'payroll_template_pdf.xlsx'
        )
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"템플릿 파일을 찾을 수 없습니다: {template_path}")
        
        # 임시 엑셀 파일 생성
        temp_excel = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        temp_excel_path = temp_excel.name
        temp_excel.close()
        
        # 템플릿 복사
        shutil.copy2(template_path, temp_excel_path)
        
        # 데이터 채우기
        wb = self.fill_template_data(temp_excel_path, payroll_data, employee_data, period)
        wb.save(temp_excel_path)
        wb.close()
        
        # 엑셀→PDF 변환
        converter = self.get_converter()
        if converter == 'xlsx2pdf':
            self.convert_excel_to_pdf_xlsx2pdf(temp_excel_path, output_path)
        elif converter == 'libreoffice':
            self.convert_excel_to_pdf_libreoffice(temp_excel_path, output_path)
        elif converter == 'win32com':
            self.convert_excel_to_pdf_win32com(temp_excel_path, output_path)
        
        # 임시 파일 삭제
        if os.path.exists(temp_excel_path):
            os.unlink(temp_excel_path)
        
        logger.info(f"템플릿 기반 PDF 생성 완료: {output_path}")
        
    except Exception as e:
        logger.error(f"템플릿 기반 PDF 생성 실패: {e}")
        # 임시 파일 정리
        if 'temp_excel_path' in locals() and os.path.exists(temp_excel_path):
            os.unlink(temp_excel_path)
        raise
```

---

## ⚠️ 주의사항

### 1. 라이브러리 의존성
- `xlsx2pdf`: 추가 라이브러리 필요
- `LibreOffice`: 외부 프로그램 설치 필요
- `win32com`: Windows 전용, Excel 설치 필요

### 2. 플랫폼 호환성
- 크로스 플랫폼 지원을 위해 여러 변환 방법 지원
- 폴백 메커니즘 구현 (변환 실패 시 기존 방식 사용)

### 3. 템플릿 파일 관리
- 템플릿 파일은 버전 관리에 포함
- 템플릿 변경 시 하위 호환성 고려

### 4. 성능
- 엑셀→PDF 변환은 시간이 걸릴 수 있음
- 대량 생성 시 성능 고려

---

## 📊 예상 작업 시간

| 단계 | 작업 내용 | 예상 시간 |
|------|----------|----------|
| 1 | PDF용 엑셀 템플릿 생성 | 1시간 |
| 2 | 엑셀→PDF 변환 라이브러리 선택 및 설치 | 30분 |
| 3 | 템플릿 데이터 채우기 기능 구현 | 2시간 |
| 4 | 엑셀→PDF 변환 기능 구현 | 1시간 30분 |
| 5 | PDFGenerator 클래스 통합 | 1시간 |
| 6 | main.py 통합 | 30분 |
| 7 | 테스트 | 1시간 |
| 8 | 에러 처리 및 예외 상황 | 30분 |
| **총계** | | **8시간** |

---

## ✅ 체크리스트

### 구현 전
- [ ] 현재 상태 분석 완료
- [ ] 구현 방법 선택 완료
- [ ] 구현 계획 작성 완료

### 구현 중
- [ ] PDF용 엑셀 템플릿 생성
- [ ] 엑셀→PDF 변환 라이브러리 설치
- [ ] 템플릿 데이터 채우기 기능
- [ ] 엑셀→PDF 변환 기능
- [ ] PDFGenerator 클래스 통합
- [ ] main.py 통합
- [ ] 테스트
- [ ] 에러 처리

### 구현 후
- [ ] 문서 업데이트
- [ ] 사용자 매뉴얼 업데이트

---

## 🔗 관련 파일

- `payroll_generator/pdf_generator.py` (수정 예정)
- `payroll_generator/templates/payroll_template_pdf.xlsx` (신규)
- `payroll_generator/excel_handler.py` (참고)
- `main.py` (수정 예정, 선택 사항)
- `requirements.txt` (수정 예정)

---

## 🚀 향후 개선 사항

1. **템플릿 편집기**
   - GUI로 템플릿 편집 가능
   - 템플릿 미리보기 기능

2. **다중 템플릿 지원**
   - 회사별, 부서별 다른 템플릿 사용
   - 템플릿 선택 기능

3. **템플릿 버전 관리**
   - 템플릿 버전 관리
   - 템플릿 변경 이력 추적

---

**마지막 업데이트**: 2025-11-11

