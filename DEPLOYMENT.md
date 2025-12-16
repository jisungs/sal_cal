# 🚀 GitHub 배포 가이드 (웹 프로젝트 전용)

**작성일**: 2025-12-16  
**목표**: 웹 프로젝트만 GitHub에 배포

---

## 📋 배포 전 체크리스트

### 1. 민감 정보 제거 확인

- [x] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인 ✅
- [x] `app.db` 파일이 `.gitignore`에 포함되어 있는지 확인 ✅
- [x] 로그 파일이 `.gitignore`에 포함되어 있는지 확인 ✅
- [x] 업로드된 파일이 `.gitignore`에 포함되어 있는지 확인 ✅

### 2. requirements.txt 확인

- [x] 웹 프로젝트에 필요한 패키지만 포함 ✅
- [x] 버전 고정 (==) 또는 최소 버전 (>=) 명시 ✅
- [x] 데스크톱 전용 패키지 제외 (matplotlib, pyinstaller 등) ✅

### 3. README.md 업데이트

- [x] 웹 프로젝트 중심으로 설명 ✅
- [x] 설치 및 실행 방법 명시 ✅
- [x] 환경 변수 설정 가이드 포함 ✅

---

## 🔧 GitHub 배포 단계

### 1단계: 현재 상태 커밋

```bash
# 변경사항 확인
git status

# 변경사항 추가
git add .

# 커밋
git commit -m "feat: 웹 프로젝트 배포 준비 - requirements.txt 업데이트 및 메뉴바 개선"
```

### 2단계: GitHub 저장소 생성

1. GitHub에 로그인
2. 새 저장소 생성 (New Repository)
   - Repository name: `salary-cal-web` (또는 원하는 이름)
   - Description: "급여명세서 자동생성기 - 웹 버전"
   - Public 또는 Private 선택
   - **README, .gitignore, license 추가하지 않음** (이미 있으므로)

### 3단계: 원격 저장소 연결 및 푸시

```bash
# 원격 저장소 추가 (GitHub에서 제공하는 URL 사용)
git remote add origin https://github.com/YOUR_USERNAME/salary-cal-web.git

# 또는 SSH 사용
git remote add origin git@github.com:YOUR_USERNAME/salary-cal-web.git

# 브랜치 이름 확인 (보통 master 또는 main)
git branch

# 원격 저장소에 푸시
git push -u origin master
# 또는
git push -u origin main
```

### 4단계: 배포 확인

1. GitHub 저장소 페이지에서 파일 확인
2. README.md가 올바르게 표시되는지 확인
3. requirements.txt가 포함되어 있는지 확인

---

## 📦 배포에 포함할 파일

### ✅ 포함할 파일/폴더

- `app/` - Flask 애플리케이션 코드
- `web/` - 웹 템플릿 및 정적 파일
- `payroll_generator/` - 공통 모듈
- `sample/` - 샘플 템플릿 파일 (템플릿 디자인용)
- `config.py` - 설정 파일
- `app.py` - 웹 앱 진입점
- `requirements.txt` - 패키지 의존성
- `requirements-web.txt` - 웹 앱 전용 패키지 (참고용)
- `README.md` - 프로젝트 설명서
- `.gitignore` - Git 제외 파일 목록
- `plan/` - 프로젝트 계획 문서 (선택사항)

### ❌ 제외할 파일/폴더

- `venv/` - 가상환경 (이미 .gitignore에 포함)
- `app.db` - 데이터베이스 파일 (이미 .gitignore에 포함)
- `*.log` - 로그 파일 (이미 .gitignore에 포함)
- `web/uploads/*` - 업로드된 파일 (이미 .gitignore에 포함)
- `outputs/*` - 생성된 파일 (이미 .gitignore에 포함)
- `main.py` - 데스크톱 앱 진입점 (웹 프로젝트에는 불필요)
- `build_configs/` - 빌드 설정 (데스크톱 앱용)
- `sample/*.pdf` - 생성된 PDF 파일 (샘플 파일 제외)

---

## 🔐 환경 변수 설정 가이드

### .env.example 파일 생성 (선택사항)

GitHub에 올리기 전에 `.env.example` 파일을 생성하여 필요한 환경 변수를 문서화할 수 있습니다:

```bash
# .env.example
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

사용자는 이 파일을 복사하여 `.env` 파일을 만들고 실제 값을 입력합니다.

---

## 🌐 배포 플랫폼 추천

### Railway (권장)

1. GitHub 저장소 연결
2. 자동 배포 설정
3. 환경 변수 설정
4. 무료 플랜 제공

### Heroku

1. GitHub 저장소 연결
2. Procfile 생성 필요
3. 환경 변수 설정
4. 유료 플랜 (무료 플랜 종료됨)

### Render

1. GitHub 저장소 연결
2. 자동 배포 설정
3. 환경 변수 설정
4. 무료 플랜 제공

---

## 📝 배포 후 확인 사항

- [ ] README.md가 올바르게 표시되는지 확인
- [ ] requirements.txt가 포함되어 있는지 확인
- [ ] .gitignore가 올바르게 작동하는지 확인
- [ ] 민감한 정보가 포함되지 않았는지 확인
- [ ] 샘플 파일이 포함되어 있는지 확인

---

## 🚨 주의사항

1. **민감한 정보 확인**
   - `.env` 파일이 커밋되지 않았는지 확인
   - 데이터베이스 파일이 커밋되지 않았는지 확인
   - API 키나 비밀번호가 코드에 하드코딩되지 않았는지 확인

2. **파일 크기**
   - 큰 파일은 Git LFS 사용 고려
   - 불필요한 파일은 제외

3. **라이선스**
   - LICENSE 파일 추가 고려
   - README.md에 라이선스 정보 명시

---

**작성자**: AI Assistant  
**작성일**: 2025-12-16

