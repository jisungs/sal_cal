@echo off
REM 급여명세서 자동생성기 빌드 스크립트 (Windows)

echo ==========================================
echo 급여명세서 자동생성기 빌드 시작
echo ==========================================

REM 가상환경 활성화 확인
if not exist "venv" (
    echo ❌ 가상환경이 없습니다. 먼저 가상환경을 생성하세요.
    exit /b 1
)

REM 가상환경 활성화
call venv\Scripts\activate.bat

REM PyInstaller 설치 확인
where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ❌ PyInstaller가 설치되어 있지 않습니다.
    echo 다음 명령어로 설치하세요: pip install pyinstaller
    exit /b 1
)

REM 이전 빌드 정리
echo 📦 이전 빌드 정리 중...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM 프로젝트 루트로 이동
cd /d "%~dp0\.."

REM 빌드 실행
echo 🔨 빌드 실행 중...
pyinstaller build_configs\build_win.spec --clean

REM 빌드 결과 확인
if exist "dist\급여명세서생성기.exe" (
    echo.
    echo ✅ 빌드 성공!
    echo 📁 빌드 결과: dist\급여명세서생성기.exe
    echo 📊 파일 크기 확인 중...
    for %%A in ("dist\급여명세서생성기.exe") do echo    크기: %%~zA bytes
    echo.
    echo 실행 방법:
    echo   dist\급여명세서생성기.exe
) else (
    echo.
    echo ❌ 빌드 실패!
    exit /b 1
)

