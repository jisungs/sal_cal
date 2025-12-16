# 🪟 Windows용 실행 파일(.exe) 빌드 가이드

**작성일**: 2025-11-12  
**대상**: Windows 10/11

---

## 📋 사전 준비

### 1. Windows PC 준비
- Windows 10 이상 (권장: Windows 11)
- 관리자 권한 (선택사항, 권장)

### 2. Python 설치
- Python 3.8 이상 설치
- 설치 시 "Add Python to PATH" 옵션 체크

### 3. 프로젝트 파일 복사
프로젝트 폴더 전체를 Windows PC로 복사:
```
salary_cal/
├── main.py
├── payroll_generator/
├── build_win.spec
├── build.bat
├── requirements.txt
└── ...
```

---

## 🚀 빌드 방법

### 방법 1: 빌드 스크립트 사용 (권장)

#### 1단계: 명령 프롬프트 열기
1. **시작 메뉴**에서 "cmd" 또는 "명령 프롬프트" 검색
2. **관리자 권한으로 실행** (선택사항, 권장)

#### 2단계: 프로젝트 폴더로 이동
```cmd
cd C:\path\to\salary_cal
```

#### 3단계: 가상환경 생성 및 활성화
```cmd
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate
```

#### 4단계: 필수 패키지 설치
```cmd
pip install -r requirements.txt
pip install pyinstaller
```

#### 5단계: 빌드 실행
```cmd
build.bat
```

또는 직접 실행:
```cmd
pyinstaller build_win.spec --clean
```

#### 6단계: 빌드 결과 확인
빌드가 완료되면 `dist\급여명세서생성기.exe` 파일이 생성됩니다.

---

### 방법 2: 수동 빌드

#### 1단계: 가상환경 설정
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
```

#### 2단계: PyInstaller로 빌드
```cmd
pyinstaller build_win.spec --clean
```

#### 3단계: 결과 확인
```cmd
dir dist\급여명세서생성기.exe
```

---

## 📁 생성되는 파일

빌드가 완료되면 다음 파일이 생성됩니다:

- **실행 파일**: `dist\급여명세서생성기.exe`
- **파일 크기**: 약 40-50MB
- **위치**: `dist\` 폴더

---

## 🧪 실행 방법

### 방법 1: 파일 탐색기에서 실행
1. **파일 탐색기** 열기
2. **`dist` 폴더**로 이동
3. **`급여명세서생성기.exe` 더블클릭**

### 방법 2: 명령 프롬프트에서 실행
```cmd
dist\급여명세서생성기.exe
```

---

## ⚠️ Windows Defender 경고 해결

첫 실행 시 Windows Defender가 경고를 표시할 수 있습니다:

### 해결 방법 1: Windows Defender 예외 추가
1. **Windows 보안** 열기
2. **바이러스 및 위협 방지** 선택
3. **바이러스 및 위협 방지 설정 관리** 클릭
4. **제외 추가 또는 제거** 클릭
5. **제외 추가** > **파일** 선택
6. **`급여명세서생성기.exe` 파일 선택**

### 해결 방법 2: 실행 허용
1. 경고 창에서 **"추가 정보"** 클릭
2. **"실행"** 버튼 클릭

---

## 🔧 빌드 문제 해결

### 문제 1: "pyinstaller를 찾을 수 없습니다"
**해결**:
```cmd
pip install pyinstaller
```

### 문제 2: "모듈을 찾을 수 없습니다"
**해결**:
```cmd
pip install -r requirements.txt
```

### 문제 3: 빌드 실패
**해결**:
1. 가상환경 재생성
2. 모든 패키지 재설치
3. `build\` 및 `dist\` 폴더 삭제 후 재빌드

---

## 📝 빌드 스크립트 내용

`build.bat` 파일 내용:

```batch
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

REM 빌드 실행
echo 🔨 빌드 실행 중...
pyinstaller build_win.spec --clean

REM 빌드 결과 확인
if exist "dist\급여명세서생성기.exe" (
    echo.
    echo ✅ 빌드 성공!
    echo 📁 빌드 결과: dist\급여명세서생성기.exe
    echo.
    echo 실행 방법:
    echo   dist\급여명세서생성기.exe
) else (
    echo.
    echo ❌ 빌드 실패!
    exit /b 1
)
```

---

## 🎯 빌드 체크리스트

빌드 전 확인사항:
- [ ] Python 3.8 이상 설치됨
- [ ] 프로젝트 파일이 Windows PC에 복사됨
- [ ] 가상환경 생성됨
- [ ] 필수 패키지 설치됨
- [ ] PyInstaller 설치됨

빌드 후 확인사항:
- [ ] `dist\급여명세서생성기.exe` 파일 생성됨
- [ ] 파일 크기가 40-50MB 범위
- [ ] 실행 파일이 정상 실행됨
- [ ] GUI 창이 정상 표시됨

---

## 📊 빌드 시간

- **예상 시간**: 2-5분
- **파일 크기**: 약 40-50MB
- **플랫폼**: Windows 10/11 (64-bit)

---

## 🔗 관련 파일

- `build_win.spec`: Windows 빌드 설정 파일
- `build.bat`: Windows 빌드 스크립트
- `requirements.txt`: 필수 패키지 목록

---

## 💡 팁

1. **관리자 권한**: 빌드 시 관리자 권한으로 실행하면 권한 문제를 피할 수 있습니다
2. **바이러스 검사**: 빌드 후 바이러스 검사를 실행하여 오탐지 확인
3. **테스트**: 다른 Windows PC에서도 테스트하여 호환성 확인

---

**마지막 업데이트**: 2025-11-12

