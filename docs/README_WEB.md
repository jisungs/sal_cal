# 💼 급여명세서 자동생성기 - 웹 버전

웹 브라우저에서 사용할 수 있는 급여명세서 자동 생성 서비스입니다.

## 🚀 빠른 시작

### 1. 가상환경 활성화 및 패키지 설치

```bash
# 가상환경 활성화
source venv/bin/activate  # Windows: venv\Scripts\activate

# 웹 버전 필수 패키지 설치
pip install flask flask-cors werkzeug
```

### 2. 웹 서버 실행

**Linux/Mac:**
```bash
./run_web.sh
```

**Windows:**
```cmd
run_web.bat
```

**또는 직접 실행:**
```bash
python app.py
```

### 3. 브라우저에서 접속

웹 브라우저에서 `http://localhost:5000` 접속

---

## 📁 프로젝트 구조

```
salary_cal/
├── app.py                      # Flask 메인 애플리케이션
├── requirements.txt            # 의존성 목록
├── run_web.sh                 # 실행 스크립트 (Linux/Mac)
├── run_web.bat                # 실행 스크립트 (Windows)
│
├── payroll_generator/          # 기존 모듈 (재사용)
│   ├── calculator.py          # 급여 계산 로직
│   ├── excel_handler.py       # 엑셀 처리 (템플릿 기반)
│   ├── pdf_generator.py       # PDF 생성 (템플릿 기반)
│   ├── templates/             # 엑셀 템플릿 파일
│   │   └── payroll_template.xlsx
│   └── ...
│
├── web/
│   ├── templates/              # HTML 템플릿
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── result.html
│   │   └── error.html
│   ├── static/                 # 정적 파일
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── uploads/                # 업로드된 파일 (임시)
│
└── outputs/                    # 생성된 파일
    ├── pdf/
    └── excel/
```

---

## 🎯 주요 기능

- ✅ 엑셀 파일 업로드
- ✅ 급여명세서 자동 계산
- ✅ **엑셀 템플릿 기반 급여명세서 생성**
- ✅ PDF/엑셀 다운로드
- ✅ 일괄 처리 (ZIP 파일 다운로드)

---

## 📋 사용 방법

1. **직원 정보 엑셀 파일 준비**
   - 필수 컬럼: 이름, 주민번호, 입사일, 기본급, 부양가족수
   - 샘플 템플릿: `payroll_generator/templates/employee_template.xlsx`

2. **웹 브라우저에서 접속**
   - `http://localhost:5000` 접속

3. **파일 업로드 및 설정**
   - 직원 정보 엑셀 파일 선택
   - 지급 기간 입력 (예: 2025-01)
   - 출력 형식 선택 (엑셀/PDF/둘 다)

4. **결과 확인 및 다운로드**
   - 계산 결과 확인
   - 개별 다운로드 또는 일괄 다운로드

---

## 🔧 환경 설정

### 환경 변수 (선택사항)

`.env` 파일 생성 (선택사항):

```env
FLASK_DEBUG=True
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

---

## 🛠️ 개발 모드

개발 모드로 실행:

```bash
export FLASK_DEBUG=True
export FLASK_ENV=development
python app.py
```

---

## 📝 API 엔드포인트

- `GET /` - 메인 페이지 (파일 업로드 폼)
- `POST /upload` - 파일 업로드 및 처리
- `GET /result/<session_id>` - 결과 페이지
- `GET /download/<format>/<employee_name>` - 개별 파일 다운로드
- `GET /batch_download/<format>` - 일괄 다운로드 (ZIP)

---

## ⚠️ 주의사항

- 업로드 파일 크기 제한: 16MB
- 지원 파일 형식: .xlsx, .xls
- 생성된 파일은 `outputs/` 폴더에 저장됩니다.

---

## 🔄 데스크톱 앱과의 차이점

- 웹 버전은 브라우저에서 실행
- 대시보드 기능 제외 (v2.0에서 추가 예정)
- 사용자 인증 없음 (로컬 실행 전용)
- 템플릿 기반 생성 방식 사용

---

## 📞 문제 해결

### 포트가 이미 사용 중인 경우

```bash
# 다른 포트로 실행
export FLASK_RUN_PORT=5001
python app.py
```

### 모듈 import 오류

```bash
# 현재 디렉토리를 Python 경로에 추가
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python app.py
```

---

**작성일**: 2025-01-XX  
**버전**: 1.0 (웹 버전 MVP)

