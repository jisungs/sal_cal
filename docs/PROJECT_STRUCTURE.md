# 📁 프로젝트 구조 가이드

## 🎯 프로젝트 개요

이 프로젝트는 **단일 저장소(Monorepo)** 구조로, 데스크톱 앱과 웹 앱을 모두 지원합니다.

---

## 📂 현재 프로젝트 구조

```
salary_cal/
├── 📱 데스크톱 앱
│   ├── main.py                 # GUI 메인 진입점 (tkinter)
│   ├── view_dashboard.py       # 대시보드 뷰어
│   ├── demo.py                 # 데모 스크립트
│   ├── build.spec              # PyInstaller 빌드 설정
│   ├── build.sh                # 빌드 스크립트 (Linux/Mac)
│   └── build.bat               # 빌드 스크립트 (Windows)
│
├── 🌐 웹 앱
│   ├── app.py                  # Flask 웹 애플리케이션
│   ├── run_web.sh              # 웹 실행 스크립트 (Linux/Mac)
│   ├── run_web.bat             # 웹 실행 스크립트 (Windows)
│   ├── web/
│   │   ├── templates/          # HTML 템플릿
│   │   ├── static/             # CSS, JS
│   │   └── uploads/            # 업로드 파일 임시 저장
│   └── outputs/                # 생성된 파일
│
├── 📦 공통 모듈 (두 앱 모두 사용)
│   └── payroll_generator/
│       ├── calculator.py       # 급여 계산 로직
│       ├── excel_handler.py    # 엑셀 처리 (템플릿 기반)
│       ├── pdf_generator.py     # PDF 생성 (템플릿 기반)
│       ├── dashboard.py         # 대시보드 분석 (데스크톱 전용)
│       ├── config.py            # 설정값
│       ├── utils.py             # 유틸리티
│       ├── templates/           # 엑셀 템플릿 파일
│       │   ├── payroll_template.xlsx
│       │   ├── employee_template.xlsx
│       │   └── company_template.xlsx
│       └── assets/              # 리소스 (폰트 등)
│
└── 📚 문서 및 설정
    ├── README.md               # 프로젝트 메인 문서
    ├── README_WEB.md           # 웹 버전 가이드
    ├── requirements.txt         # 의존성 (데스크톱 + 웹)
    └── plan/                   # 프로젝트 계획 문서
```

---

## 🚀 실행 방법

### 데스크톱 앱 실행
```bash
python main.py
```

### 웹 앱 실행
```bash
# Linux/Mac
./run_web.sh

# Windows
run_web.bat

# 또는 직접 실행
python app.py
```

---

## 🔄 모듈 공유 전략

### 공통 모듈 (`payroll_generator/`)
- ✅ 두 앱 모두 동일한 모듈 사용
- ✅ 코드 중복 없음
- ✅ 버그 수정 시 한 곳만 수정하면 됨

### 앱별 전용 파일
- **데스크톱 앱**: `main.py`, `view_dashboard.py`, `build.*`
- **웹 앱**: `app.py`, `web/`, `run_web.*`

---

## 📋 의존성 관리

### 공통 의존성
- `openpyxl`, `pandas`, `reportlab` (두 앱 모두 사용)

### 데스크톱 앱 전용
- `tkinter` (Python 기본 포함)
- `matplotlib` (대시보드용)
- `pyinstaller` (빌드용)

### 웹 앱 전용
- `flask`, `flask-cors`, `werkzeug`

---

## ✅ 현재 구조의 장점

1. **코드 재사용**: 공통 모듈을 두 앱이 공유
2. **유지보수 용이**: 한 곳에서 수정하면 두 앱 모두 반영
3. **템플릿 공유**: 엑셀 템플릿 파일 공유
4. **단일 저장소**: Git 관리가 간단
5. **빠른 개발**: 기존 모듈 재사용으로 개발 시간 단축

---

## 🎯 권장 사항

**현재 구조 유지 권장** ✅

이유:
- 이미 웹 구조가 잘 추가되어 있음
- 공통 모듈 재사용이 효율적
- 모노레포 패턴으로 관리 용이
- 코드 중복 없음

---

## 📝 향후 개선 사항

### v2.0에서 고려할 사항
- [ ] 웹 앱 전용 `requirements-web.txt` 분리
- [ ] 데스크톱 앱 전용 `requirements-desktop.txt` 분리
- [ ] 배포 스크립트 분리 (웹/데스크톱)
- [ ] CI/CD 파이프라인 분리 (선택사항)

---

**작성일**: 2025-01-XX  
**버전**: 1.0

