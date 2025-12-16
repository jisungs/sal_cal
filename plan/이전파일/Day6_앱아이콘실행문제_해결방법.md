# 📄 Day 6 앱 아이콘 실행 문제 해결 방법

**작성일**: 2025-11-12  
**문제**: .app 번들이 Finder에서 폴더처럼 보이고 더블클릭으로 실행되지 않음  
**상태**: ✅ 해결 방법 제공

---

## 🔍 문제 분석

### 현상
- `.app` 번들이 Finder에서 폴더처럼 보임
- 더블클릭해도 실행되지 않음

### 원인
1. **Finder 설정**: "패키지 내용 보기" 옵션이 활성화되어 있을 수 있음
2. **권한 문제**: 실행 권한이 없을 수 있음
3. **확장 속성**: macOS의 확장 속성(quarantine) 문제
4. **코드 서명**: 코드 서명이 없어 실행이 차단될 수 있음

---

## ✅ 해결 방법

### 방법 1: Finder에서 직접 실행

1. **Finder에서 `급여명세서생성기.app` 찾기**
2. **더블클릭** (폴더처럼 보여도 더블클릭하면 실행됨)
3. **보안 경고가 나타나면**:
   - 우클릭 > "열기" 선택
   - 또는 시스템 환경설정 > 보안 및 개인 정보 보호 > "확인" 클릭

### 방법 2: 터미널에서 실행

```bash
# 방법 1: open 명령어 사용
open dist/급여명세서생성기.app

# 방법 2: 직접 실행 파일 실행
./dist/급여명세서생성기.app/Contents/MacOS/급여명세서생성기
```

### 방법 3: Applications 폴더로 복사

```bash
# Applications 폴더로 복사
cp -R dist/급여명세서생성기.app /Applications/

# Applications 폴더에서 실행
open /Applications/급여명세서생성기.app
```

### 방법 4: Finder 설정 확인

1. **Finder > 환경설정** (또는 `Cmd + ,`)
2. **고급** 탭 선택
3. **"모든 파일 확장자 보기"** 체크 해제 (선택사항)
4. **"패키지 내용 보기"** 체크 해제 (중요!)

---

## 🔧 권한 및 속성 수정

### 실행 권한 부여

```bash
# .app 번들 전체에 실행 권한 부여
chmod -R 755 dist/급여명세서생성기.app

# 실행 파일에 실행 권한 부여
chmod +x dist/급여명세서생성기.app/Contents/MacOS/급여명세서생성기
```

### 확장 속성 제거

```bash
# quarantine 속성 제거 (보안 경고 해결)
xattr -cr dist/급여명세서생성기.app
```

### 코드 서명 (선택사항)

```bash
# 개발자 ID로 서명 (Apple Developer 계정 필요)
codesign --force --deep --sign "Developer ID Application: Your Name" dist/급여명세서생성기.app

# 또는 임시 서명 (테스트용)
codesign --force --deep --sign - dist/급여명세서생성기.app
```

---

## 📝 .app 번들 구조 확인

정상적인 .app 번들 구조:

```
급여명세서생성기.app/
├── Contents/
│   ├── Info.plist          # 앱 정보
│   ├── MacOS/
│   │   └── 급여명세서생성기  # 실행 파일
│   ├── Resources/          # 리소스 파일
│   └── Frameworks/         # 프레임워크
```

---

## 🧪 실행 테스트

### 테스트 1: Finder에서 더블클릭
1. Finder에서 `급여명세서생성기.app` 더블클릭
2. GUI 창이 열리는지 확인

### 테스트 2: 터미널에서 실행
```bash
open dist/급여명세서생성기.app
```

### 테스트 3: 직접 실행 파일 실행
```bash
./dist/급여명세서생성기.app/Contents/MacOS/급여명세서생성기
```

---

## ⚠️ 주의사항

1. **Finder에서 폴더처럼 보여도 정상**: .app 번들은 실제로는 폴더 구조이지만, Finder에서는 앱으로 인식되어야 함
2. **더블클릭으로 실행 가능**: 폴더처럼 보여도 더블클릭하면 실행됨
3. **보안 경고**: 첫 실행 시 보안 경고가 나타날 수 있음 (정상)

---

## 🔗 관련 파일

- `build_mac.spec`: macOS 빌드 설정
- `build.sh`: 빌드 스크립트
- `실행방법.md`: 실행 방법 가이드

---

**작성자**: AI Assistant  
**상태**: ✅ 해결 방법 제공  
**다음 작업**: 실행 테스트

