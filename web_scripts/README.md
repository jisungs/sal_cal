# 🌐 웹 실행 스크립트 폴더

이 폴더에는 웹 애플리케이션을 실행하기 위한 스크립트가 포함되어 있습니다.

## 📋 포함된 파일

- **`run_web.sh`** - 웹 서버 실행 스크립트 (Linux/Mac)
  - 가상환경 자동 활성화
  - Flask 개발 모드 설정
  - 웹 서버 시작

- **`run_web.bat`** - 웹 서버 실행 스크립트 (Windows)
  - 가상환경 자동 활성화
  - Flask 개발 모드 설정
  - 웹 서버 시작

## 🚀 사용 방법

### Linux/Mac에서 실행
```bash
# 프로젝트 루트에서 실행
./web_scripts/run_web.sh

# 또는 직접 실행
cd web_scripts
./run_web.sh
```

### Windows에서 실행
```cmd
REM 프로젝트 루트에서 실행
web_scripts\run_web.bat

REM 또는 직접 실행
cd web_scripts
run_web.bat
```

## 📝 실행 후

웹 서버가 시작되면 브라우저에서 다음 주소로 접속하세요:
- **로컬**: http://127.0.0.1:5000
- **네트워크**: http://localhost:5000

## ⚙️ 환경 변수

스크립트에서 자동으로 설정되는 환경 변수:
- `FLASK_APP=app.py` - Flask 앱 파일 지정
- `FLASK_DEBUG=True` - 디버그 모드 활성화
- `FLASK_ENV=development` - 개발 환경 설정

## 📝 참고 사항

- 스크립트는 프로젝트 루트에서 실행되어야 합니다.
- 가상환경이 활성화되어 있어야 합니다.
- Flask가 설치되어 있어야 합니다: `pip install flask`
- 웹 앱 파일(`app.py`)이 프로젝트 루트에 있어야 합니다.

## 🔗 관련 문서

- [웹 버전 가이드](../docs/README_WEB.md)
- [프로젝트 구조 가이드](../docs/PROJECT_STRUCTURE.md)

