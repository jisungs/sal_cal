# 🔨 빌드 파일 가이드

**작성일**: 2025-01-XX  
**목적**: 빌드 관련 파일들의 용도 및 필요성 설명

---

## 📋 빌드 파일 목록

### ✅ 필수 파일 (데스크톱 앱 배포용)

#### 플랫폼별 빌드 설정 파일
- **`build_mac.spec`** - macOS용 .app 번들 생성 설정
  - 용도: macOS에서 실행 파일(.app) 생성
  - 사용: `pyinstaller build_mac.spec`
  
- **`build_win.spec`** - Windows용 .exe 생성 설정
  - 용도: Windows에서 실행 파일(.exe) 생성
  - 사용: `pyinstaller build_win.spec`

#### 빌드 스크립트
- **`build.sh`** - macOS 빌드 자동화 스크립트
  - 용도: macOS에서 `.app` 및 `.pkg` 자동 생성
  - 사용: `./build.sh`
  
- **`build.bat`** - Windows 빌드 자동화 스크립트
  - 용도: Windows에서 `.exe` 자동 생성
  - 사용: `build.bat`

### ⚠️ 선택적 파일

- **`build.spec`** - 일반 빌드 설정 (디버깅용)
  - 용도: 콘솔 모드로 디버깅 시 사용
  - 상태: `build_mac.spec`과 `build_win.spec`이 있어 중복 가능성
  - 권장: 삭제 또는 `scripts/` 폴더로 이동

---

## 🎯 파일 필요성 판단

### 데스크톱 앱을 배포하는 경우
- ✅ **모두 필요**: `build_mac.spec`, `build_win.spec`, `build.sh`, `build.bat`
- ⚠️ `build.spec`은 선택사항 (디버깅용)

### 웹 앱만 사용하는 경우
- ❌ **모두 불필요**: 웹 앱은 실행 파일 빌드가 필요 없음
- 단, 나중을 위해 보관할 수도 있음

### 하이브리드 프로젝트 (현재 상태)
- ✅ **플랫폼별 파일 필요**: 데스크톱 앱 배포 시 필요
- ⚠️ `build.spec`은 중복이므로 정리 권장

---

## 📂 정리 방안

### 옵션 1: 중복 파일만 정리 (권장) ✅

```bash
# build.spec을 scripts/ 폴더로 이동 (디버깅용으로 보관)
mv build.spec scripts/build_debug.spec
```

**장점**:
- 필수 빌드 파일은 루트에 유지 (빌드 스크립트 경로 수정 불필요)
- 중복 파일만 정리
- 디버깅용 파일은 보관

### 옵션 2: 빌드 파일을 build/ 폴더로 정리

```bash
mkdir build_configs
mv build*.spec build_configs/
mv build.sh build_configs/
mv build.bat build_configs/
```

**단점**:
- 빌드 스크립트 경로 수정 필요
- 빌드 스크립트가 루트에서 실행되어야 함

### 옵션 3: build.spec 삭제

```bash
# 중복 파일 삭제
rm build.spec
```

**장점**:
- 가장 간단한 정리
- 디버깅이 필요하면 `build_mac.spec`을 수정하여 사용

---

## 🚀 사용 방법

### macOS에서 빌드
```bash
./build.sh
# 또는
pyinstaller build_mac.spec --clean
```

### Windows에서 빌드
```cmd
build.bat
# 또는
pyinstaller build_win.spec --clean
```

---

## 💡 권장 사항

**현재 프로젝트는 데스크톱 앱과 웹 앱을 모두 지원하므로:**

1. ✅ **플랫폼별 빌드 파일 유지** (`build_mac.spec`, `build_win.spec`)
2. ✅ **빌드 스크립트 유지** (`build.sh`, `build.bat`)
3. ⚠️ **`build.spec` 정리** (중복 파일이므로)

**정리 방법**: `build.spec`을 `scripts/build_debug.spec`으로 이동하거나 삭제

---

**마지막 업데이트**: 2025-01-XX

