# GitHub Push 오류 분석 및 해결 보고서

**작성일**: 2025-12-16  
**에러**: `RPC failed; HTTP 400`  
**상태**: 🔍 원인 분석 완료

---

## 🔍 에러 분석

### 에러 메시지
```
error: RPC failed; HTTP 400 curl 22 The requested URL returned error: 400
send-pack: unexpected disconnect while reading sideband packet
fatal: the remote end hung up unexpectedly
```

### 원인 분석

**핵심 문제**: **큰 파일이 Git 저장소에 포함되어 있음**

1. **125MB 파일 발견**: `payroll_generator/assets/nanum-all_new.zip`
   - GitHub는 **100MB 이상의 파일을 거부**합니다
   - 이 파일이 push 실패의 주요 원인입니다

2. **전체 저장소 크기**: 274.35 MiB
   - 매우 큰 저장소 크기로 인해 push가 느리고 실패할 수 있음

3. **불필요한 파일 포함**:
   - `app.db` (228KB) - 데이터베이스 파일 (이미 커밋됨)
   - `dist/`, `build/` 폴더의 빌드 파일들
   - 큰 폰트 파일들

---

## 📊 문제 파일 목록

### 큰 파일 (10MB 이상)

| 파일 경로 | 크기 | 상태 | 문제 |
|----------|------|------|------|
| `payroll_generator/assets/nanum-all_new.zip` | **125MB** | ❌ 커밋됨 | **GitHub 100MB 제한 초과** |
| `payroll_generator/assets/NanumGothic.ttf` | 4.5MB | ⚠️ 커밋됨 | 큰 파일 (허용되지만 불필요) |

### 불필요한 파일

| 파일 경로 | 크기 | 상태 | 문제 |
|----------|------|------|------|
| `app.db` | 228KB | ❌ 커밋됨 | 데이터베이스 파일 (제외해야 함) |
| `dist/` 폴더 | - | ❌ 커밋됨 | 빌드 결과물 (제외해야 함) |
| `build/` 폴더 | - | ❌ 커밋됨 | 빌드 임시 파일 (제외해야 함) |

---

## ✅ 해결 방법

### 방법 1: 큰 파일 제거 및 .gitignore 업데이트 (권장)

#### 1단계: .gitignore 업데이트

큰 파일과 불필요한 파일을 `.gitignore`에 추가:

```bash
# 큰 폰트 파일
payroll_generator/assets/nanum-all_new.zip
payroll_generator/assets/나눔\ 글꼴/

# 빌드 파일
dist/
build/

# 데이터베이스 (이미 있지만 확인)
app.db
*.db
```

#### 2단계: 이미 커밋된 파일 제거

```bash
# Git 캐시에서 제거 (파일은 유지)
git rm --cached payroll_generator/assets/nanum-all_new.zip
git rm --cached app.db
git rm -r --cached dist/
git rm -r --cached build/

# 커밋
git commit -m "chore: 큰 파일 및 불필요한 파일 제거 (GitHub 배포용)"
```

#### 3단계: 다시 push 시도

```bash
git push -u origin main
```

### 방법 2: Git LFS 사용 (대안)

큰 파일을 유지해야 하는 경우 Git LFS 사용:

```bash
# Git LFS 설치 (macOS)
brew install git-lfs

# Git LFS 초기화
git lfs install

# 큰 파일을 LFS로 추적
git lfs track "*.zip"
git lfs track "*.ttf"

# .gitattributes 파일 커밋
git add .gitattributes
git commit -m "chore: Git LFS 설정"
```

**주의**: Git LFS는 GitHub에서 무료로 제공하지만 용량 제한이 있습니다.

### 방법 3: HTTP 버퍼 크기 증가 (임시 해결책)

큰 파일 문제를 해결한 후에도 문제가 발생하면:

```bash
# HTTP 버퍼 크기 증가
git config http.postBuffer 524288000  # 500MB

# 다시 push 시도
git push -u origin main
```

---

## 🎯 권장 해결 순서

### 1단계: .gitignore 업데이트

```bash
# .gitignore에 추가할 내용
cat >> .gitignore << 'EOF'

# 큰 폰트 파일 (웹 프로젝트에는 불필요)
payroll_generator/assets/nanum-all_new.zip
payroll_generator/assets/나눔\ 글꼴/

# 빌드 파일
dist/
build/
EOF
```

### 2단계: 이미 커밋된 파일 제거

```bash
# 큰 파일 제거
git rm --cached payroll_generator/assets/nanum-all_new.zip

# 데이터베이스 파일 제거
git rm --cached app.db

# 빌드 폴더 제거
git rm -r --cached dist/ build/ 2>/dev/null || true

# 변경사항 커밋
git add .gitignore
git commit -m "chore: GitHub 배포를 위한 큰 파일 및 불필요한 파일 제거"
```

### 3단계: 저장소 크기 확인

```bash
# 저장소 크기 확인
git count-objects -vH

# 큰 파일이 제거되었는지 확인
git ls-files | xargs -I {} du -h {} 2>/dev/null | sort -rh | head -10
```

### 4단계: 다시 push 시도

```bash
# HTTP 버퍼 크기 증가 (선택사항)
git config http.postBuffer 524288000

# Push
git push -u origin main
```

---

## 📋 웹 프로젝트 배포에 불필요한 파일

웹 프로젝트만 배포하는 경우 다음 파일들은 제외해야 합니다:

### 제외할 파일/폴더

1. **데스크톱 앱 관련**
   - `main.py` - 데스크톱 앱 진입점
   - `dist/` - 빌드 결과물
   - `build/` - 빌드 임시 파일

2. **큰 리소스 파일**
   - `payroll_generator/assets/nanum-all_new.zip` (125MB)
   - `payroll_generator/assets/나눔 글꼴/` 폴더 전체
   - `payroll_generator/assets/NanumGothic.ttf` (4.5MB) - 웹에서는 CDN 사용 가능

3. **데이터베이스**
   - `app.db` - 로컬 데이터베이스 파일

4. **로그 및 임시 파일**
   - `*.log` - 로그 파일
   - `web/uploads/*` - 업로드된 파일
   - `outputs/*` - 생성된 파일

### 포함할 파일/폴더

1. **웹 앱 코드**
   - `app/` - Flask 애플리케이션
   - `web/` - 웹 템플릿 및 정적 파일
   - `payroll_generator/` - 공통 모듈 (큰 파일 제외)

2. **템플릿 파일**
   - `sample/급여명세서_template.xlsx` - 템플릿 디자인용
   - `sample/임금명세서양식_template3.xlsx` - 템플릿 디자인용

3. **설정 파일**
   - `config.py` - 설정 파일
   - `app.py` - 웹 앱 진입점
   - `requirements.txt` - 패키지 의존성

---

## 🚨 주의사항

1. **파일 삭제 전 백업**
   - 큰 파일을 제거하기 전에 필요하면 백업하세요
   - 웹 프로젝트에는 큰 폰트 파일이 필요하지 않을 수 있습니다

2. **Git 히스토리 정리**
   - 이미 커밋된 큰 파일은 `git rm --cached`로 제거해도 히스토리에 남아있습니다
   - 완전히 제거하려면 `git filter-branch` 또는 `git filter-repo` 사용 필요

3. **팀 협업**
   - 다른 개발자와 협업 중이라면 큰 파일 제거 전에 공지하세요

---

## 🔧 빠른 해결 스크립트

다음 명령어를 순서대로 실행하세요:

```bash
# 1. .gitignore 업데이트
cat >> .gitignore << 'EOF'

# 큰 폰트 파일 (웹 프로젝트에는 불필요)
payroll_generator/assets/nanum-all_new.zip
payroll_generator/assets/나눔\ 글꼴/

# 빌드 파일
dist/
build/
EOF

# 2. 큰 파일 제거
git rm --cached payroll_generator/assets/nanum-all_new.zip
git rm --cached app.db
git rm -r --cached dist/ build/ 2>/dev/null || true

# 3. 커밋
git add .gitignore
git commit -m "chore: GitHub 배포를 위한 큰 파일 제거"

# 4. HTTP 버퍼 크기 증가
git config http.postBuffer 524288000

# 5. Push 시도
git push -u origin main
```

---

## 📊 예상 결과

### 제거 전
- 저장소 크기: **274.35 MiB**
- 큰 파일: 125MB (nanum-all_new.zip)
- Push 실패

### 제거 후
- 저장소 크기: **약 50-100 MB** (예상)
- 큰 파일: 없음
- Push 성공 예상

---

**다음 단계**: 위의 해결 방법을 적용하여 다시 push를 시도하세요.

