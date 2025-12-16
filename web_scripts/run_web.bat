@echo off
REM 웹 서버 실행 스크립트 (Windows)

REM 프로젝트 루트로 이동
cd /d "%~dp0\.."

REM 가상환경 활성화
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Flask 앱 실행
set FLASK_APP=app.py
set FLASK_DEBUG=True
REM FLASK_ENV는 Flask 3.x에서 deprecated되었으므로 제거
REM 포트 설정: 기본값 5001 (macOS AirPlay와 충돌 방지)
REM 다른 포트를 사용하려면: set FLASK_RUN_PORT=5002
if not defined FLASK_RUN_PORT set FLASK_RUN_PORT=5001

echo 웹 서버 시작 중...
echo 접속 주소: http://localhost:%FLASK_RUN_PORT%
echo.

python app.py

pause

