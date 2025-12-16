# 🚀 빠른 시작 가이드

## 📋 프로젝트 개요

이 프로젝트는 **데스크톱 앱**과 **웹 앱** 두 가지 버전을 제공합니다.

---

## ⚡ 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 활성화
source venv/bin/activate  # Windows: venv\Scripts\activate

# 전체 패키지 설치 (데스크톱 + 웹)
pip install -r requirements.txt

# 또는 선택적 설치
pip install -r requirements-desktop.txt  # 데스크톱 앱만
pip install -r requirements-web.txt     # 웹 앱만
```

### 2. 실행

#### 데스크톱 앱 실행
```bash
python main.py
```

#### 웹 앱 실행
```bash
# Linux/Mac
./run_web.sh

# Windows
run_web.bat

# 또는 직접 실행
python app.py
```

웹 브라우저에서 `http://localhost:5000` 접속

---

## 📁 프로젝트 구조 요약

```
salary_cal/
├── main.py              # 데스크톱 앱 (tkinter)
├── app.py               # 웹 앱 (Flask)
├── payroll_generator/    # 공통 모듈
├── web/                 # 웹 앱 파일
└── outputs/             # 웹 앱 출력 파일
```

---

## 📚 상세 문서

- [프로젝트 구조 가이드](PROJECT_STRUCTURE.md) - 전체 구조 설명
- [웹 버전 가이드](README_WEB.md) - 웹 앱 사용법
- [메인 README](README.md) - 프로젝트 전체 설명

---

**작성일**: 2025-01-XX

