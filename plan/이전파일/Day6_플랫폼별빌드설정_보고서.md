# 📄 Day 6 플랫폼별 빌드 설정 보고서

**작성일**: 2025-11-12  
**작업 내용**: macOS용 .app/.pkg 및 Windows용 .exe 빌드 설정  
**상태**: ✅ 완료

---

## 📋 작업 개요

플랫폼별로 적절한 형식의 실행 파일을 생성하도록 빌드 설정을 분리했습니다.

### 생성되는 파일 형식
- **macOS**: `.app` 번들 + `.pkg` 인스톨러
- **Windows**: `.exe` 실행 파일

---

## ✅ 완료된 작업

### 1. 플랫폼별 build.spec 파일 생성

#### macOS용: `build_mac.spec`
- `.app` 번들 생성 (BUNDLE 설정)
- 번들 식별자: `com.salarycal.payrollgenerator`
- Info.plist 설정 포함

#### Windows용: `build_win.spec`
- `.exe` 파일 생성
- GUI 모드 설정
- 아이콘 파일 지원

### 2. 빌드 스크립트 수정

#### `build.sh` (macOS)
- `.app` 번들 빌드
- `.pkg` 인스톨러 자동 생성
- `pkgbuild` 명령어 사용

#### `build.bat` (Windows)
- `.exe` 파일 빌드
- 파일 크기 확인

---

## 📊 빌드 결과

### macOS
- **.app 번들**: `dist/급여명세서생성기.app`
- **.pkg 인스톨러**: `dist/급여명세서생성기.pkg`

### Windows
- **.exe 파일**: `dist/급여명세서생성기.exe`

---

## 🚀 사용 방법

### macOS에서 빌드
```bash
./build.sh
```

**생성되는 파일**:
- `dist/급여명세서생성기.app` - 실행 가능한 앱 번들
- `dist/급여명세서생성기.pkg` - 인스톨러 패키지

**실행 방법**:
```bash
# .app 번들 직접 실행
open dist/급여명세서생성기.app

# .pkg 인스톨러 실행 (설치)
open dist/급여명세서생성기.pkg
```

### Windows에서 빌드
```cmd
build.bat
```

**생성되는 파일**:
- `dist\급여명세서생성기.exe` - 실행 가능한 실행 파일

**실행 방법**:
```cmd
dist\급여명세서생성기.exe
```

---

## 📝 빌드 설정 상세

### macOS .app 번들 설정
```python
app = BUNDLE(
    exe,
    name='급여명세서생성기.app',
    bundle_identifier='com.salarycal.payrollgenerator',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
    },
)
```

### .pkg 인스톨러 생성
```bash
pkgbuild --root "$PKG_DIR" \
         --identifier "com.salarycal.payrollgenerator" \
         --version "1.0.0" \
         --install-location "/" \
         "dist/급여명세서생성기.pkg"
```

---

## ⚠️ 주의사항

### macOS
1. **코드 서명**: 배포 시 코드 서명이 필요할 수 있음
2. **Gatekeeper**: .pkg 파일 실행 시 보안 경고가 표시될 수 있음
3. **pkgbuild**: macOS 기본 제공 도구 (추가 설치 불필요)

### Windows
1. **바이러스 검사**: .exe 파일은 바이러스 검사 필요
2. **Windows Defender**: 첫 실행 시 경고가 표시될 수 있음

---

## 🔗 관련 파일

- `build_mac.spec`: macOS용 빌드 설정
- `build_win.spec`: Windows용 빌드 설정
- `build.sh`: macOS 빌드 스크립트
- `build.bat`: Windows 빌드 스크립트

---

**작성자**: AI Assistant  
**상태**: ✅ 완료  
**다음 작업**: 빌드 테스트 및 검증

