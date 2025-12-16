# 🔨 빌드 설정 폴더

이 폴더에는 데스크톱 앱을 실행 파일로 빌드하기 위한 설정 파일과 스크립트가 포함되어 있습니다.

## 📋 포함된 파일

### 빌드 설정 파일 (.spec)
- **`build_mac.spec`** - macOS용 PyInstaller 빌드 설정
  - `.app` 번들 생성 설정
  - 번들 식별자: `com.salarycal.payrollgenerator`
  - Info.plist 설정 포함

- **`build_win.spec`** - Windows용 PyInstaller 빌드 설정
  - `.exe` 파일 생성 설정
  - GUI 모드 설정
  - 아이콘 파일 지원

### 빌드 스크립트
- **`build.sh`** - macOS 빌드 자동화 스크립트
  - `.app` 번들 및 `.pkg` 인스톨러 자동 생성
  - 가상환경 활성화 및 PyInstaller 확인
  - 빌드 결과 검증

- **`build.bat`** - Windows 빌드 자동화 스크립트
  - `.exe` 파일 자동 생성
  - 가상환경 활성화 및 PyInstaller 확인
  - 빌드 결과 검증

## 🚀 사용 방법

### macOS에서 빌드
```bash
# 프로젝트 루트에서 실행
./build_configs/build.sh

# 또는 직접 실행
cd build_configs
./build.sh
```

**생성되는 파일**:
- `dist/급여명세서생성기.app` - 실행 가능한 앱 번들
- `dist/급여명세서생성기.pkg` - 인스톨러 패키지 (선택사항)

### Windows에서 빌드
```cmd
REM 프로젝트 루트에서 실행
build_configs\build.bat

REM 또는 직접 실행
cd build_configs
build.bat
```

**생성되는 파일**:
- `dist\급여명세서생성기.exe` - 실행 가능한 실행 파일

## 📝 참고 사항

- 빌드 스크립트는 프로젝트 루트에서 실행되어야 합니다.
- 빌드 전에 가상환경이 활성화되어 있어야 합니다.
- PyInstaller가 설치되어 있어야 합니다: `pip install pyinstaller`
- 빌드 결과물은 프로젝트 루트의 `dist/` 폴더에 생성됩니다.

## 🔗 관련 문서

- [빌드 파일 가이드](../docs/BUILD_FILES_GUIDE.md)
- [실행 파일 생성 가이드](../plan/이전파일/실행파일_생성_가이드.md)

