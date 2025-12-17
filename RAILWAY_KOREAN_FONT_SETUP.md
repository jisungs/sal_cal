# 🔤 Railway 한글 폰트 설정 가이드

**작성일**: 2025-12-17  
**목적**: Railway 배포 환경에서 LibreOffice PDF 변환 시 한글 깨짐 문제 해결

---

## ⚠️ 문제 상황

Railway에 LibreOffice를 설치한 후 PDF 출력은 성공했지만, 한글이 깨져서 나타나는 문제가 발생했습니다.

**원인**: LibreOffice가 시스템에 한글 폰트가 설치되어 있지 않아 한글을 제대로 렌더링하지 못함

---

## ✅ 해결 방법

### 방법 1: Railway 빌드 시 자동 설치 (권장)

`nixpacks.toml` 파일에 한글 폰트 설치 명령이 이미 추가되어 있습니다:

```toml
[phases.install]
cmds = [
  "apt-get update && apt-get install -y libreoffice libreoffice-writer libreoffice-calc libreoffice-impress fonts-nanum fonts-nanum-coding fontconfig || true",
  "mkdir -p /usr/share/fonts/truetype/nanum ~/.fonts",
  "cp payroll_generator/assets/NanumGothic.ttf /usr/share/fonts/truetype/nanum/ 2>/dev/null || cp 'payroll_generator/assets/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf' /usr/share/fonts/truetype/nanum/ 2>/dev/null || true",
  "cp payroll_generator/assets/NanumGothic.ttf ~/.fonts/ 2>/dev/null || cp 'payroll_generator/assets/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf' ~/.fonts/ 2>/dev/null || true",
  "fc-cache -fv",
  "pip install -r requirements.txt"
]
```

**설명**:
- `fonts-nanum`: Debian/Ubuntu의 나눔 폰트 패키지
- `fonts-nanum-coding`: 나눔 코딩 폰트 패키지
- 프로젝트의 `NanumGothic.ttf` 파일을 시스템 폰트 디렉토리에 복사
- `fc-cache -fv`: 폰트 캐시 업데이트

### 방법 2: Railway 대시보드에서 직접 설치

Railway 대시보드 → 프로젝트 → "Deployments" → "Shell" 또는 "Run Command"에서:

```bash
# 한글 폰트 설치
apt-get update && \
apt-get install -y fonts-nanum fonts-nanum-coding fontconfig && \
mkdir -p /usr/share/fonts/truetype/nanum && \
cp payroll_generator/assets/NanumGothic.ttf /usr/share/fonts/truetype/nanum/ 2>/dev/null || \
cp 'payroll_generator/assets/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf' /usr/share/fonts/truetype/nanum/ 2>/dev/null || true && \
fc-cache -fv
```

---

## 🔍 확인 방법

### 1. 폰트 설치 확인

Railway Shell에서 다음 명령어 실행:

```bash
# 폰트 파일 확인
ls -la /usr/share/fonts/truetype/nanum/

# 폰트 캐시 확인
fc-list | grep -i nanum

# LibreOffice 폰트 확인
libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.xlsx
```

### 2. PDF 생성 테스트

웹사이트에서 템플릿 디자인을 선택하고 PDF를 생성한 후:
- 한글이 정상적으로 표시되는지 확인
- 폰트가 깨지지 않는지 확인

---

## 📋 설치되는 폰트

1. **시스템 패키지**:
   - `fonts-nanum`: 나눔 고딕, 나눔 명조 등
   - `fonts-nanum-coding`: 나눔 코딩 폰트

2. **프로젝트 폰트**:
   - `payroll_generator/assets/NanumGothic.ttf`
   - `payroll_generator/assets/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf`

---

## 🐛 문제 해결

### 문제 1: 폰트 파일을 찾을 수 없음

**증상**: `cp: cannot stat 'payroll_generator/assets/NanumGothic.ttf': No such file or directory`

**해결 방법**:
1. 프로젝트에 `NanumGothic.ttf` 파일이 있는지 확인
2. Git에 폰트 파일이 포함되어 있는지 확인 (`.gitignore` 확인)
3. Railway 빌드 로그에서 파일 경로 확인

### 문제 2: 폰트 캐시 업데이트 실패

**증상**: `fc-cache: command not found`

**해결 방법**:
```bash
apt-get install -y fontconfig
fc-cache -fv
```

### 문제 3: LibreOffice가 여전히 한글을 인식하지 못함

**해결 방법**:
1. LibreOffice 재시작 (Railway 재배포)
2. 폰트 캐시 강제 업데이트: `fc-cache -fv --force`
3. LibreOffice 폰트 설정 확인

---

## 📝 참고사항

### 폰트 파일 크기

- `NanumGothic.ttf`: 약 1-2MB
- Git에 포함되어 있어야 Railway 빌드 시 사용 가능

### 폰트 라이선스

- **NanumGothic**: SIL Open Font License 1.1
- 상업적 사용 가능
- 재배포 가능

---

## 🚀 빠른 해결 방법

Railway 대시보드에서 다음 명령어를 실행하세요:

```bash
apt-get update && \
apt-get install -y fonts-nanum fonts-nanum-coding fontconfig && \
mkdir -p /usr/share/fonts/truetype/nanum && \
cp payroll_generator/assets/NanumGothic.ttf /usr/share/fonts/truetype/nanum/ 2>/dev/null || \
cp 'payroll_generator/assets/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf' /usr/share/fonts/truetype/nanum/ 2>/dev/null || true && \
fc-cache -fv
```

그 다음 Railway를 재배포하면 `nixpacks.toml` 설정이 적용되어 자동으로 한글 폰트가 설치됩니다.

---

**다음 단계**: Railway를 재배포하고 PDF 생성 시 한글이 정상적으로 표시되는지 확인하세요.

