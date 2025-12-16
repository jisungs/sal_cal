# 💼 급여명세서 자동생성기

> 10인 이하 소상공인을 위한 간편한 급여명세서 자동 생성 프로그램

## 📋 프로젝트 개요

**목표**: 일주일 안에 판매 가능한 MVP(Minimum Viable Product) 개발 및 출시  
**타겟 고객**: 10인 이하 소상공인, 프리랜서 고용주, 소규모 학원/과외 운영자  
**가격 전략**: 오픈 기념 29,900원 → 정가 39,000원

---

## ✨ 주요 기능

### ✅ 현재 구현 완료된 기능 (v1.0)

- ✅ **4대보험 자동 계산**
  - 국민연금 (4.5%, 상한액 5,530,000원)
  - 건강보험 (3.545%, 상한액 5,530,000원)
  - 장기요양 (건강보험의 12.95%)
  - 고용보험 (0.9%, 상한액 5,530,000원)

- ✅ **소득세/지방소득세 자동 계산**
  - 간이세액표 기반 5단계 누진세율 적용
  - 부양가족수별 공제 반영 (0~4명 이상)

- ✅ **엑셀 파일 읽기**
  - 직원 정보 엑셀 파일 읽기
  - 필수 컬럼 검증
  - 파일 미리보기 기능

- ✅ **급여 계산 엔진**
  - 기본급 계산
  - 연장근무수당 계산
  - 상여금 계산
  - 총 지급액/공제액/실수령액 계산

- ✅ **보안 기능**
  - 주민번호 마스킹 처리
  - 파일 경로 정규화 및 검증
  - 로깅 시스템

- ✅ **엑셀 템플릿 제공**
  - 직원 정보 템플릿 (`templates/employee_template.xlsx`)
  - 회사 정보 템플릿 (`templates/company_template.xlsx`)
  - 샘플 데이터 포함

- ✅ **대시보드 데이터 분석**
  - 직원 데이터 분석
  - 근무현황 분석
  - 특이사항 분석
  - 급여 그래프 생성
  - 근무자구성 그래프 생성

- ✅ **엑셀 출력 (급여명세서 생성)**
  - 직원별 개별 급여명세서 생성
  - 전문적인 스타일링 적용
  - 자동 계산 결과 반영

- ✅ **PDF 출력**
  - A4 크기 PDF 생성
  - 한글 폰트 지원 (나눔고딕)
  - 주민번호 자동 마스킹 처리
  - 전문적인 레이아웃

- ✅ **템플릿 디자인 선택 기능** (v1.2 신규)
  - 기본 디자인, 템플릿 1, 템플릿 2 중 선택 가능
  - 엑셀 템플릿 기반 디자인 시스템 (`sample/` 폴더의 템플릿 사용)
  - 웹 및 데스크톱 인터페이스 모두 지원
  - 템플릿 디자인 PDF 생성 지원 (LibreOffice 필요)

- ✅ **GUI 인터페이스 (tkinter) - 데스크톱 앱**
  - 대시보드 탭 (통계 및 그래프)
  - 급여명세서 생성 탭
  - 파일 미리보기 기능
  - 진행 상태 표시
  - 오류 처리 및 사용자 친화적 메시지

- ✅ **웹 인터페이스 (Flask) - 웹 앱**
  - 브라우저 기반 사용자 인터페이스
  - 파일 업로드 및 처리
  - 결과 확인 및 다운로드
  - 개별/일괄 다운로드 지원
  - 엑셀 템플릿 기반 급여명세서 생성

### 📅 향후 계획 (v2.0)

- 연말정산 기능
- 이메일 자동 발송
- 급여 이력 관리
- 다국어 지원
- 웹 버전 대시보드 추가

---

## 🏗️ 프로젝트 구조

```
salary_cal/
├── README.md                          # 프로젝트 설명서
├── main.py                            # 데스크톱 앱 메인 진입점 ✅
├── app.py                             # 웹 앱 메인 진입점 ✅
│
├── build_configs/                     # 🔨 빌드 설정 및 스크립트
│   ├── build_mac.spec                 # macOS용 PyInstaller 빌드 설정 (.app 번들 생성)
│   ├── build_win.spec                 # Windows용 PyInstaller 빌드 설정 (.exe 생성)
│   ├── build.sh                       # macOS 빌드 자동화 스크립트
│   ├── build.bat                      # Windows 빌드 자동화 스크립트
│   └── README.md                      # 빌드 설정 상세 가이드
│
├── web_scripts/                        # 🌐 웹 실행 스크립트
│   ├── run_web.sh                     # 웹 서버 실행 스크립트 (Linux/Mac)
│   ├── run_web.bat                    # 웹 서버 실행 스크립트 (Windows)
│   └── README.md                      # 웹 실행 스크립트 가이드
│
├── scripts/                           # 📜 유틸리티 스크립트
│   ├── demo.py                        # 데모 실행 스크립트 (기능 테스트용)
│   ├── view_dashboard.py              # 대시보드 뷰어 (독립 실행)
│   ├── run_dashboard.sh              # 대시보드 실행 스크립트
│   ├── build_debug.spec              # 디버깅용 빌드 설정 (콘솔 모드)
│   └── README.md                      # 스크립트 사용 가이드
│
├── docs/                              # 📚 문서 파일
│   ├── PROJECT_STRUCTURE.md           # 프로젝트 구조 상세 가이드
│   ├── README_WEB.md                  # 웹 버전 사용 가이드
│   ├── BUILD_FILES_GUIDE.md           # 빌드 파일 설명서
│   ├── CLEANUP_REPORT.md              # 프로젝트 정리 보고서
│   └── ...
│   # 기능: 프로젝트 관련 모든 문서 및 가이드
│
├── misc/                              # 📦 기타 파일
│   ├── sample/                        # 샘플 파일 (대시보드 스크린샷, 샘플 엑셀 등)
│   └── README.md                      # 기타 파일 설명
│   # 기능: 프로젝트 실행에 필수적이지 않은 참고용 파일
│
├── web/                               # 🌐 웹 앱 리소스
│   ├── templates/                     # HTML 템플릿
│   │   ├── base.html                  # 기본 레이아웃
│   │   ├── index.html                 # 메인 페이지 (파일 업로드)
│   │   ├── result.html                # 결과 페이지
│   │   └── error.html                 # 에러 페이지
│   ├── static/                        # 정적 파일
│   │   ├── css/
│   │   │   └── style.css             # 스타일시트
│   │   └── js/
│   │       └── main.js                # 클라이언트 스크립트
│   └── uploads/                       # 업로드된 파일 임시 저장
│
├── outputs/                           # 생성된 파일 저장
│   ├── pdf/                           # PDF 파일
│   └── excel/                         # 엑셀 파일
│
├── payroll_generator/                 # 💼 메인 패키지 (공통 모듈)
│   ├── __init__.py
│   ├── config.py                      # 설정값 (세율, 상한액 등)
│   ├── calculator.py                  # 급여 계산 로직
│   ├── excel_handler.py               # 엑셀 입출력 처리 ✅
│   ├── pdf_generator.py               # PDF 생성 ✅
│   ├── dashboard.py                   # 대시보드 데이터 수집 ✅
│   ├── utils.py                       # 유틸리티 함수 (보안, 파일 경로)
│   ├── logger.py                      # 로깅 시스템 설정
│   │
│   ├── templates/                     # 엑셀 템플릿
│   │   ├── employee_template.xlsx     # 직원 정보 템플릿
│   │   ├── company_template.xlsx      # 회사 정보 템플릿
│   │   └── payroll_template.xlsx     # 급여명세서 템플릿 ✅
│   │
│   ├── data/                          # 샘플 데이터
│   ├── docs/                          # 문서
│   │   ├── 사용자_매뉴얼.md          # 사용자 매뉴얼 ✅
│   │   └── 샘플_파일_가이드.md       # 샘플 파일 가이드 ✅
│   ├── output/                        # 생성된 파일 저장 (데스크톱 앱용)
│   ├── assets/                        # 리소스 파일
│   │   └── NanumGothic.ttf           # 한글 폰트 ✅
│   └── logs/                          # 로그 파일 저장
│       └── app.log
│
├── plan/                              # 프로젝트 계획 문서
│   ├── master_plan/
│   │   └── 급여자동계산기_실행계획_최종.md
│   ├── Day1/                          # Day 1 문서
│   ├── Day2.md                        # Day 2 작업 계획 및 보고서 ✅
│   ├── Day3.md                        # Day 3 작업 계획 및 보고서 ✅
│   ├── Day4.md                        # Day 4 작업 계획 및 보고서 ✅
│   ├── Day5.md                        # Day 5 작업 계획 및 보고서 ✅
│   ├── Day6.md                        # Day 6 작업 계획 및 보고서 ✅
│   └── GUI_실행_가이드.md            # GUI 실행 가이드 ✅
│
└── venv/                              # 가상환경
```

---

## 📂 폴더별 상세 설명

### 🔨 `build_configs/` - 빌드 설정 및 스크립트

**기능**: 데스크톱 앱을 실행 파일(.app/.exe)로 빌드하기 위한 설정 및 스크립트

**포함 파일**:
- `build_mac.spec` - macOS용 PyInstaller 빌드 설정 (.app 번들 생성)
- `build_win.spec` - Windows용 PyInstaller 빌드 설정 (.exe 생성)
- `build.sh` - macOS 빌드 자동화 스크립트
- `build.bat` - Windows 빌드 자동화 스크립트
- `README.md` - 빌드 설정 상세 가이드

**사용 방법**:
```bash
# macOS
./build_configs/build.sh

# Windows
build_configs\build.bat
```

---

### 🌐 `web/` - 웹 앱 리소스

**기능**: 웹 애플리케이션의 프론트엔드 리소스 (HTML, CSS, JavaScript)

**포함 파일**:
- `templates/` - HTML 템플릿 파일 (Jinja2)
  - `base.html` - 기본 레이아웃
  - `index.html` - 메인 페이지 (파일 업로드 폼)
  - `result.html` - 결과 표시 페이지
  - `error.html` - 에러 페이지
- `static/` - 정적 파일
  - `css/style.css` - 스타일시트
  - `js/main.js` - 클라이언트 JavaScript
- `uploads/` - 업로드된 파일 임시 저장 폴더

### 🌐 `web_scripts/` - 웹 실행 스크립트

**기능**: Flask 웹 애플리케이션을 실행하기 위한 스크립트 (가상환경 자동 활성화)

**포함 파일**:
- `run_web.sh` - 웹 서버 실행 스크립트 (Linux/Mac)
- `run_web.bat` - 웹 서버 실행 스크립트 (Windows)
- `README.md` - 웹 실행 스크립트 가이드

**사용 방법**:
```bash
# Linux/Mac
./web_scripts/run_web.sh

# Windows
web_scripts\run_web.bat
```

**기능**:
- 가상환경 자동 활성화
- Flask 의존성 자동 설치 확인
- 포트 설정 (기본값: 5001)
- 접속 주소 안내 메시지 표시

---

### 📜 `scripts/` - 유틸리티 스크립트

**기능**: 개발 및 테스트용 유틸리티 스크립트 모음

**포함 파일**:
- `demo.py` - 데모 실행 스크립트 (기능 테스트용)
- `view_dashboard.py` - 대시보드 뷰어 (독립 실행)
- `run_dashboard.sh` - 대시보드 실행 스크립트
- `build_debug.spec` - 디버깅용 빌드 설정 (콘솔 모드)
- `README.md` - 스크립트 사용 가이드

**사용 방법**:
```bash
# 데모 실행
python scripts/demo.py

# 대시보드 뷰어
python scripts/view_dashboard.py
```

---

### 📚 `docs/` - 문서 파일

**기능**: 프로젝트 관련 모든 문서 및 가이드

**포함 파일**:
- `PROJECT_STRUCTURE.md` - 프로젝트 구조 상세 가이드
- `README_WEB.md` - 웹 버전 사용 가이드
- `BUILD_FILES_GUIDE.md` - 빌드 파일 설명서
- `CLEANUP_REPORT.md` - 프로젝트 정리 보고서
- 기타 프로젝트 문서

---

### 📦 `misc/` - 기타 파일

**기능**: 프로젝트 실행에 필수적이지 않은 참고용 파일

**포함 파일**:
- `sample/` - 샘플 파일 (대시보드 스크린샷, 샘플 엑셀 등)
- `README.md` - 기타 파일 설명

---

### 💼 `payroll_generator/` - 메인 패키지 (공통 모듈)

**기능**: 데스크톱 앱과 웹 앱이 공유하는 핵심 비즈니스 로직

**주요 모듈**:
- `calculator.py` - 급여 계산 로직
- `excel_handler.py` - 엑셀 입출력 처리
- `pdf_generator.py` - PDF 생성
- `dashboard.py` - 대시보드 데이터 수집
- `config.py` - 설정값 (세율, 상한액 등)
- `utils.py` - 유틸리티 함수
- `logger.py` - 로깅 시스템

**리소스**:
- `templates/` - 엑셀 템플릿 파일
- `assets/` - 폰트 등 리소스 파일
- `data/` - 샘플 데이터
- `docs/` - 사용자 매뉴얼 등 문서

---

## 🚀 시작하기

### 필수 요구사항

- Python 3.8 이상
- macOS, Windows, Linux

### 선택 요구사항 (템플릿 디자인 PDF 생성용)

- **LibreOffice** (템플릿 디자인 PDF 생성 시 필요)
  - Mac: `brew install --cask libreoffice`
  - Linux: `sudo apt-get install libreoffice` 또는 `sudo yum install libreoffice`
  - Windows: [LibreOffice 공식 사이트](https://www.libreoffice.org/download/)에서 다운로드

### 설치 방법

1. **저장소 클론**
```bash
git clone <repository-url>
cd salary_cal
```

2. **가상환경 생성 및 활성화**
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **필수 패키지 설치**

**전체 패키지 설치** (데스크톱 + 웹):
```bash
pip install -r requirements.txt
```

**웹 앱만 사용하는 경우**:
```bash
pip install -r requirements-web.txt
```

**데스크톱 앱만 사용하는 경우**:
```bash
pip install -r requirements-desktop.txt
```

---

## 🚀 실행 방법

### 📱 방법 1: 데스크톱 앱 실행 (GUI)

**단계별 가이드**:

1. **가상환경 활성화**
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

2. **앱 실행**
```bash
python main.py
```

3. **사용 방법**
- GUI 창이 열리면 직원 정보 엑셀 파일을 선택합니다
- 대시보드 탭에서 통계 및 그래프를 확인할 수 있습니다
- 급여명세서 생성 탭에서 엑셀/PDF 파일을 생성할 수 있습니다

**주요 기능**:
- ✅ 대시보드: 직원 통계 및 그래프 확인
- ✅ 급여명세서 생성: 엑셀/PDF 자동 생성
- ✅ 파일 미리보기 기능
- ✅ 진행 상태 표시

---

### 🌐 방법 2: 웹 앱 실행 (브라우저)

**초보자를 위한 단계별 가이드**:

#### 1단계: 가상환경 활성화

터미널(또는 명령 프롬프트)을 열고 프로젝트 폴더로 이동합니다.

```bash
# 프로젝트 폴더로 이동
cd salary_cal

# 가상환경 활성화
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

**성공 확인**: 터미널 앞에 `(venv)`가 표시되면 성공입니다.

#### 2단계: 웹 의존성 설치 (처음 한 번만)

```bash
# 웹 앱 필수 패키지 설치
pip install -r requirements-web.txt
```

**설치 확인**:
```bash
pip list | grep flask
# Flask가 표시되면 설치 완료
```

#### 3단계: 웹 서버 실행

**방법 A: 실행 스크립트 사용 (권장)** ⭐

```bash
# macOS/Linux
./web_scripts/run_web.sh

# Windows
web_scripts\run_web.bat
```

**방법 B: 직접 실행**

```bash
python app.py
```

**실행 성공 확인**:
터미널에 다음과 같은 메시지가 표시되면 성공입니다:
```
🌐 웹 서버 시작 중...
📍 접속 주소: http://localhost:5001

 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://0.0.0.0:5001
```

#### 4단계: 브라우저에서 접속

웹 브라우저(Chrome, Safari, Firefox 등)를 열고 다음 주소로 접속합니다:

```
http://localhost:5001
```

또는

```
http://127.0.0.1:5001
```

**접속 확인**: 파일 업로드 폼이 표시되면 성공입니다.

#### 5단계: 사용하기

1. **직원 정보 엑셀 파일 준비**
   - 샘플 템플릿: `payroll_generator/templates/employee_template.xlsx`
   - 필수 컬럼: 이름, 주민번호, 입사일, 기본급, 부양가족수

2. **파일 업로드 및 디자인 선택**
   - "직원 정보 엑셀 파일" 버튼을 클릭하여 파일 선택
   - 지급 기간 입력 (예: 2025-01)
   - 디자인 선택 (기본 디자인, 템플릿 1, 템플릿 2)
   - 출력 형식 선택 (엑셀/PDF/둘 다)

3. **결과 확인 및 다운로드**
   - 계산 결과가 표시됩니다
   - 개별 다운로드: 각 직원별로 엑셀/PDF 다운로드
   - 일괄 다운로드: 모든 직원의 파일을 ZIP으로 다운로드

**주요 기능**:
- ✅ 엑셀 파일 업로드 및 처리
- ✅ 급여명세서 자동 계산
- ✅ 엑셀 템플릿 기반 급여명세서 생성
- ✅ 템플릿 디자인 선택 (기본 디자인, 템플릿 1, 템플릿 2)
- ✅ PDF/엑셀 다운로드
- ✅ 일괄 처리 (ZIP 파일 다운로드)

---

### 🔄 데스크톱 앱 vs 웹 앱 비교

| 기능 | 데스크톱 앱 | 웹 앱 |
|------|------------|-------|
| 실행 환경 | Python 설치 필요 | 브라우저만 있으면 됨 |
| 대시보드 | ✅ 지원 | ❌ v2.0 예정 |
| 파일 업로드 | ✅ GUI 파일 선택 | ✅ 브라우저 파일 선택 |
| 급여 계산 | ✅ 지원 | ✅ 지원 |
| 엑셀 출력 | ✅ 지원 | ✅ 지원 |
| PDF 출력 | ✅ 지원 | ✅ 지원 |
| 템플릿 기반 생성 | ✅ 지원 | ✅ 지원 |
| 사용자 인터페이스 | tkinter GUI | 웹 브라우저 |

**권장 사용 시나리오**:
- **데스크톱 앱**: 대시보드 통계가 필요하거나 오프라인에서 작업할 때
- **웹 앱**: 간단하게 브라우저에서 빠르게 급여명세서만 생성할 때

---

### ⚠️ 문제 해결 (Troubleshooting)

#### 문제 1: 포트가 이미 사용 중입니다

**에러 메시지**:
```
Address already in use
Port 5000 is in use by another program.
```

**해결 방법**:
- 웹 앱은 기본적으로 포트 5001을 사용합니다 (macOS AirPlay 충돌 방지)
- 다른 포트를 사용하려면:
```bash
export FLASK_RUN_PORT=8080  # macOS/Linux
python app.py

# Windows:
set FLASK_RUN_PORT=8080
python app.py
```

#### 문제 2: Flask 모듈을 찾을 수 없습니다

**에러 메시지**:
```
ModuleNotFoundError: No module named 'flask'
```

**해결 방법**:
```bash
# 1. 가상환경이 활성화되어 있는지 확인
# 터미널 앞에 (venv)가 있어야 합니다

# 2. Flask 설치
pip install -r requirements-web.txt

# 3. 설치 확인
pip list | grep flask
```

#### 문제 3: 실행 스크립트가 실행되지 않습니다

**해결 방법**:

**macOS/Linux**:
```bash
# 실행 권한 부여
chmod +x web_scripts/run_web.sh

# 실행
./web_scripts/run_web.sh
```

**Windows**:
```bash
# 직접 실행
web_scripts\run_web.bat
```

#### 문제 4: 브라우저에서 접속이 안 됩니다

**확인 사항**:
1. 웹 서버가 실행 중인지 확인 (터미널에 "Running on..." 메시지 확인)
2. 포트 번호 확인 (기본값: 5001)
3. 방화벽 설정 확인
4. 다른 브라우저로 시도

**해결 방법**:
```bash
# 포트 확인
lsof -i :5001  # macOS/Linux
netstat -an | findstr 5001  # Windows

# 다른 포트로 실행
export FLASK_RUN_PORT=8080
python app.py
```

#### 문제 5: 파일 업로드가 안 됩니다

**확인 사항**:
1. 파일 형식: `.xlsx` 또는 `.xls`만 지원
2. 파일 크기: 최대 16MB
3. 필수 컬럼: 이름, 주민번호, 입사일, 기본급, 부양가족수

**해결 방법**:
- 샘플 템플릿 사용: `payroll_generator/templates/employee_template.xlsx`
- 엑셀 파일 형식 확인
- 필수 컬럼이 모두 있는지 확인

#### 문제 6: 템플릿 디자인 PDF 생성이 안 됩니다

**에러 메시지**:
```
템플릿 디자인 PDF 변환 실패. 엑셀 파일은 생성되었습니다.
PDF 변환 라이브러리를 설치하거나 엑셀 파일을 수동으로 PDF로 변환하세요.
```

**해결 방법**:
1. **LibreOffice 설치** (권장)
   ```bash
   # Mac
   brew install --cask libreoffice
   
   # Linux
   sudo apt-get install libreoffice
   
   # Windows
   # LibreOffice 공식 사이트에서 다운로드: https://www.libreoffice.org/download/
   ```

2. **설치 확인**
   ```bash
   libreoffice --version
   # LibreOffice 버전이 표시되면 설치 완료
   ```

3. **대안**: 엑셀 파일이 생성되므로, 엑셀 파일을 수동으로 PDF로 변환할 수 있습니다.

#### 3. 데모 프로그램 실행
```bash
python scripts/demo.py
```

데모 프로그램은 다음을 보여줍니다:
- 시스템 설정 정보 (4대보험 요율, 세율 등)
- 엑셀 파일 읽기
- 급여 계산 결과
- 전체 급여 현황 요약

#### 4. 데스크톱 앱 빌드 (실행 파일 생성)
```bash
# macOS
./build_configs/build.sh

# Windows
build_configs\build.bat
```

빌드 결과물은 `dist/` 폴더에 생성됩니다.

---

## 📊 데이터 구조

### 입력 엑셀 파일 (직원 정보)

| 컬럼명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| 이름 | string | ✅ | 직원 이름 |
| 주민번호 | string | ✅ | 주민번호 앞자리 (세금계산용) |
| 입사일 | date | ✅ | YYYY-MM-DD 형식 |
| 부양가족수 | integer | ✅ | 부양가족 수 (소득세 계산용) |
| 계좌번호 | string | ❌ | 급여 이체용 |
| 기본급 | integer | ✅ | 월 기본급 |
| 연장근무시간 | integer | ❌ | 시간당 단가 별도 입력 |
| 연장근무단가 | integer | ❌ | 기본급/일근무시간 * 1.5 권장 |
| 상여금 | integer | ❌ | 상여금 금액 |
| 공제사항 | string | ❌ | 기타 공제 메모 |

### 출력 구조 (급여명세서)

**지급 항목**
- 기본급
- 연장근무수당
- 상여금
- 총 지급액

**공제 항목**
- 국민연금
- 건강보험
- 장기요양
- 고용보험
- 소득세 (부양가족수 반영)
- 지방소득세
- 총 공제액

**최종 항목**
- 실수령액 (총 지급액 - 총 공제액)

---

## 💻 사용 예시

### Python 코드로 사용하기

```python
from payroll_generator.calculator import PayrollCalculator
from payroll_generator.excel_handler import ExcelHandler

# 엑셀 파일 읽기
handler = ExcelHandler()
df = handler.read_employee_data('templates/employee_template.xlsx')

# 급여 계산
calculator = PayrollCalculator()
for idx, row in df.iterrows():
    result = calculator.calculate_deductions(row.to_dict())
    print(f"{row['이름']}님의 실수령액: {result['실수령액']:,}원")
```

---

## 📝 개발 진행 상황

### ✅ 완료된 작업

- [x] Day 0: 개발 환경 세팅
  - [x] 프로젝트 구조 생성
  - [x] 가상환경 생성
  - [x] 필수 패키지 설치
  - [x] Git 저장소 초기화

- [x] Day 1: 요구사항 정의 및 설계 ✅
  - [x] 데이터 구조 설계
  - [x] 출력 구조 설계
  - [x] 엑셀 템플릿 생성
  - [x] 기본 모듈 구현 (config, utils, logger, calculator, excel_handler, dashboard)
  - [x] 화면 설계 (와이어프레임)

### ✅ 완료된 작업 (Day 0-6)

- [x] Day 0: 개발 환경 세팅 ✅
- [x] Day 1: 요구사항 정의 및 설계 ✅
- [x] Day 2: 기술 스택 확정 및 프로젝트 초기화 ✅
- [x] Day 3: 급여 계산 로직 완성 및 엑셀 출력 기능 ✅
- [x] Day 4: GUI 개발 및 통합 ✅
- [x] Day 5: PDF 생성 및 테스트 ✅
- [x] Day 6: 패키징 및 문서화 ✅

### 🚧 진행 예정

- [ ] Day 7: 출시 준비 및 마케팅

---

## 🧪 데모 실행

### 데모 프로그램 실행

```bash
python scripts/demo.py
```

데모 프로그램은 다음을 보여줍니다:
- 시스템 설정 정보 (4대보험 요율, 세율 등)
- 엑셀 파일 읽기
- 급여 계산 결과
- 전체 급여 현황 요약

---

## 📚 문서

### 프로젝트 계획 문서
- [실행 계획서](plan/master_plan/급여자동계산기_실행계획_최종.md) - 전체 프로젝트 계획
- [Day 2 작업 계획](plan/Day2.md) - 기술 스택 확정 및 프로젝트 초기화
- [Day 3 작업 계획](plan/Day3.md) - 급여 계산 로직 완성
- [Day 4 작업 계획](plan/Day4.md) - GUI 개발 및 통합
- [Day 5 작업 계획](plan/Day5.md) - PDF 생성 및 테스트
- [Day 6 작업 계획](plan/Day6.md) - 패키징 및 문서화

### 사용자 문서
- [사용자 매뉴얼](payroll_generator/docs/사용자_매뉴얼.md) - 사용자 가이드 (약 15페이지)
- [샘플 파일 가이드](payroll_generator/docs/샘플_파일_가이드.md) - 샘플 파일 사용 가이드
- [GUI 실행 가이드](plan/GUI_실행_가이드.md) - GUI 실행 및 테스트 가이드

### 설계 문서
- [Day 1 요구사항 정의](plan/Day1/Day1_요구사항정의_및_설계.md) - Day 1 작업 내용
- [데이터 구조 설계서](plan/Day1/Day1_데이터구조설계서.md) - 상세 데이터 구조
- [화면 설계서](plan/Day1/Day1_화면설계서.md) - GUI 화면 설계 (와이어프레임)

---

## 🔧 기술 스택

### 공통 기술 스택
- **언어**: Python 3.8+
- **엑셀 처리**: openpyxl, pandas ✅
- **PDF 생성**: reportlab ✅
- **이미지 처리**: Pillow ✅

### 데스크톱 앱 전용
- **GUI**: tkinter ✅
- **그래프**: matplotlib ✅
- **패키징**: PyInstaller ✅

### 웹 앱 전용
- **웹 프레임워크**: Flask 3.0+ ✅
- **템플릿 엔진**: Jinja2 ✅
- **정적 파일**: CSS, JavaScript ✅

---

## 📋 세율 정보 (2025년 기준)

### 4대보험 요율

| 보험 종류 | 요율 | 상한액 |
|----------|------|--------|
| 국민연금 | 4.5% | 5,530,000원 |
| 건강보험 | 3.545% | 5,530,000원 |
| 장기요양 | 0.4591% | - |
| 고용보험 | 0.9% | 5,530,000원 |

### 소득세 간이세액표

| 과세표준 구간 | 세율 | 누진공제 |
|--------------|------|---------|
| 0원 ~ 1,200,000원 | 6% | 0원 |
| 1,200,000원 ~ 4,600,000원 | 15% | 108,000원 |
| 4,600,000원 ~ 8,800,000원 | 24% | 522,000원 |
| 8,800,000원 ~ 15,000,000원 | 35% | 1,490,000원 |
| 15,000,000원 이상 | 38% | 1,940,000원 |

### 부양가족 공제액

| 부양가족수 | 공제액 |
|-----------|--------|
| 0명 | 0원 |
| 1명 | 150,000원 |
| 2명 | 300,000원 |
| 3명 | 450,000원 |
| 4명 이상 | 600,000원 |

---

## 🔒 보안 및 개인정보 보호

- ✅ 주민번호 마스킹 처리 (PDF 출력 시)
- ✅ 파일 경로 정규화 및 검증
- ✅ 로깅 시스템 (모든 작업 기록)
- ✅ 로컬 처리만 (클라우드 업로드 없음)

---

## 📞 지원 및 문의

- **이메일**: support@example.com
- **카카오톡**: @급여자동화
- **응답 시간**: 평일 1주일 이내

---

## 📄 라이선스

상업적 사용 가능

---

## 🗺️ 로드맵

### v1.0 (MVP) - ✅ 완료
- [x] 기본 급여 계산 기능 ✅
- [x] 4대보험 자동 계산 ✅
- [x] 소득세/지방소득세 계산 ✅
- [x] 대시보드 데이터 분석 ✅
- [x] 화면 설계 완료 ✅
- [x] 엑셀 출력 ✅
- [x] PDF 출력 ✅
- [x] GUI 인터페이스 ✅
- [x] 패키징 (PyInstaller) ✅
- [x] 문서화 ✅

### v1.2 (현재) ✅
- ✅ 엑셀 템플릿 기반 디자인 시스템
- ✅ 템플릿 디자인 선택 기능 (템플릿 1, 템플릿 2)
- ✅ LibreOffice를 통한 템플릿 PDF 생성
- ✅ YAML 기반 디자인 제거 및 코드 정리

### v1.3 (예정)
- Service Layer 추가
- 자동 테스트 구축
- 성능 최적화
- 브랜드 디자인 적용

### v2.0 (예정)
- 연말정산 기능
- 이메일 자동 발송
- 급여 이력 관리
- 다국어 지원

---

---

## 📖 웹 프로젝트 구조 상세 설명

### 🌐 웹 앱 아키텍처

```
웹 애플리케이션 구조:

app.py (Flask 메인 애플리케이션)
├── 라우트 정의
│   ├── GET /                    → 메인 페이지 (index.html)
│   ├── POST /upload             → 파일 업로드 및 처리
│   ├── GET /result/<session_id> → 결과 페이지 (result.html)
│   ├── GET /download/<format>/<name> → 개별 파일 다운로드
│   └── GET /batch_download/<format>  → 일괄 다운로드 (ZIP)
│
├── 공통 모듈 사용
│   ├── payroll_generator.calculator    → 급여 계산
│   ├── payroll_generator.excel_handler → 엑셀 처리
│   └── payroll_generator.pdf_generator → PDF 생성
│
└── 파일 저장
    ├── web/uploads/              → 업로드된 파일 (임시)
    └── outputs/                 → 생성된 파일
        ├── pdf/                 → PDF 파일
        └── excel/               → 엑셀 파일
```

### 📁 주요 파일 설명

| 파일/폴더 | 설명 | 용도 |
|----------|------|------|
| `app.py` | Flask 웹 애플리케이션 메인 파일 | 웹 서버 진입점, 라우트 정의 |
| `web/templates/` | HTML 템플릿 파일 | 사용자 인터페이스 |
| `web/static/css/` | 스타일시트 | 웹 페이지 디자인 |
| `web/static/js/` | JavaScript 파일 | 클라이언트 로직 |
| `web/uploads/` | 업로드 파일 임시 저장 | 사용자가 업로드한 엑셀 파일 |
| `outputs/` | 생성된 파일 저장 | 급여명세서 PDF/엑셀 |

### 🔄 웹 앱 동작 흐름

```
1. 사용자가 브라우저에서 접속
   ↓
2. index.html 표시 (파일 업로드 폼)
   ↓
3. 사용자가 엑셀 파일 업로드
   ↓
4. POST /upload 요청
   ↓
5. 서버에서 파일 처리
   - 엑셀 파일 읽기
   - 급여 계산 (calculator.py)
   - 결과를 세션에 저장
   ↓
6. GET /result/<session_id> 리다이렉트
   ↓
7. result.html 표시 (계산 결과)
   ↓
8. 사용자가 다운로드 버튼 클릭
   ↓
9. GET /download/<format>/<name> 요청
   ↓
10. 서버에서 파일 생성 및 다운로드
    - 엑셀: excel_handler.py 사용
    - PDF: pdf_generator.py 사용
```

### 🔐 보안 및 세션 관리

- **세션 기반**: Flask 세션을 사용하여 업로드된 파일과 계산 결과를 임시 저장
- **파일 검증**: 파일 확장자 및 크기 검증
- **보안 파일명**: `secure_filename` 사용으로 파일명 보안 처리
- **로컬 실행 전용**: 현재는 로컬 네트워크에서만 접근 가능

---

---

## 🎨 템플릿 디자인 사용 가이드

### 템플릿 디자인이란?

템플릿 디자인은 `sample/` 폴더에 있는 엑셀 템플릿 파일을 기반으로 급여명세서를 생성하는 기능입니다. 템플릿의 스타일, 레이아웃, 디자인이 그대로 유지됩니다.

### 사용 가능한 템플릿

1. **템플릿 1** (`template_sample1`)
   - 템플릿 파일: `sample/급여명세서_template.xlsx`
   - 특징: 표준 급여명세서 양식

2. **템플릿 2** (`template_sample2`)
   - 템플릿 파일: `sample/임금명세서양식_template3.xlsx`
   - 특징: 임금명세서 양식

### 템플릿 디자인 사용 방법

#### 웹 앱에서 사용하기

1. 파일 업로드 페이지에서 디자인 선택
   - 기본 디자인: 코드 기반 기본 디자인
   - 템플릿 1: `sample/급여명세서_template.xlsx` 사용
   - 템플릿 2: `sample/임금명세서양식_template3.xlsx` 사용

2. 출력 형식 선택
   - 엑셀: 템플릿 디자인이 적용된 엑셀 파일 생성
   - PDF: 템플릿 디자인이 적용된 PDF 파일 생성 (LibreOffice 필요)

#### 데스크톱 앱에서 사용하기

1. 급여명세서 생성 탭에서 디자인 선택
   - 드롭다운 메뉴에서 "템플릿 1" 또는 "템플릿 2" 선택

2. 출력 형식 선택
   - 엑셀/PDF 선택 가능

### PDF 생성 요구사항

템플릿 디자인을 PDF로 생성하려면 **LibreOffice**가 필요합니다.

#### LibreOffice 설치 방법

**Mac**:
```bash
brew install --cask libreoffice
```

**Linux**:
```bash
sudo apt-get install libreoffice
# 또는
sudo yum install libreoffice
```

**Windows**:
- [LibreOffice 공식 사이트](https://www.libreoffice.org/download/)에서 다운로드 및 설치

#### 설치 확인

```bash
libreoffice --version
# LibreOffice 버전이 표시되면 설치 완료
```

### 템플릿 파일 위치

템플릿 파일은 프로젝트 루트의 `sample/` 폴더에 있습니다:
- `sample/급여명세서_template.xlsx` (템플릿 1)
- `sample/임금명세서양식_template3.xlsx` (템플릿 2)

### 주의사항

- 템플릿 디자인 PDF 생성 시 LibreOffice가 없으면 엑셀 파일만 생성됩니다
- 엑셀 파일은 항상 생성되므로, 필요시 수동으로 PDF로 변환할 수 있습니다
- 템플릿 파일이 없으면 기본 디자인으로 폴백됩니다

---

**마지막 업데이트**: 2025-12-15  
**버전**: 1.2 (템플릿 디자인 기능 추가)  
**웹 앱 포트**: 5001 (기본값)

