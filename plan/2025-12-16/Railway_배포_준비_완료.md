# Railway 배포 준비 완료 보고서

**작성일**: 2025-12-16  
**상태**: ✅ 배포 준비 완료

---

## ✅ 완료된 작업

### 1. 배포 파일 생성

- [x] **Procfile** 생성 ✅
  - Gunicorn을 사용한 프로덕션 서버 설정
  - Railway의 PORT 환경 변수 사용

- [x] **railway.json** 생성 ✅
  - Railway 빌드 및 배포 설정
  - NIXPACKS 빌더 사용
  - 재시작 정책 설정

- [x] **requirements.txt** 업데이트 ✅
  - `gunicorn==21.2.0` 추가

- [x] **app.py** 수정 ✅
  - Railway의 PORT 환경 변수 지원 추가

- [x] **RAILWAY_DEPLOYMENT.md** 작성 ✅
  - 상세한 배포 가이드 문서

---

## 📋 생성된 파일 목록

### 배포 파일

1. **Procfile**
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

2. **railway.json**
   - 빌드 설정: NIXPACKS 사용
   - 시작 명령어: Gunicorn
   - 재시작 정책: 실패 시 재시작

3. **requirements.txt**
   - `gunicorn==21.2.0` 추가됨

### 문서 파일

1. **RAILWAY_DEPLOYMENT.md**
   - Railway 배포 단계별 가이드
   - 환경 변수 설정 방법
   - 데이터베이스 마이그레이션 가이드
   - 문제 해결 가이드

---

## 🚀 다음 단계: Railway 배포

### 1단계: Railway 계정 생성

1. [Railway.app](https://railway.app) 접속
2. GitHub 계정으로 로그인
3. "New Project" 클릭

### 2단계: GitHub 저장소 연결

1. "Deploy from GitHub repo" 선택
2. `jisungs/sal_cal` 저장소 선택
3. Railway가 자동으로 빌드 시작

### 3단계: PostgreSQL 데이터베이스 추가

1. 프로젝트 대시보드에서 "New" 클릭
2. "Database" → "Add PostgreSQL" 선택
3. `DATABASE_URL` 환경 변수가 자동 설정됨

### 4단계: 환경 변수 설정

**필수 변수**:
```bash
FLASK_ENV=production
SECRET_KEY=<랜덤 문자열>
```

**SECRET_KEY 생성**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**선택적 변수** (이메일 기능 사용 시):
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 5단계: 데이터베이스 마이그레이션

Railway CLI 사용:
```bash
npm i -g @railway/cli
railway login
railway link
railway run flask db upgrade
```

또는 Railway 대시보드 터미널에서:
```bash
flask db upgrade
```

### 6단계: 도메인 설정 (선택사항)

1. 프로젝트 → Settings → "Generate Domain"
2. 무료 도메인 생성 또는 커스텀 도메인 연결

---

## ⚠️ 주의사항

### 파일 저장소

Railway는 **임시 파일 시스템**을 사용하므로:

1. **업로드 파일**: Railway Volume 사용 또는 클라우드 스토리지(S3) 사용 권장
2. **생성된 파일**: 동일하게 Volume 또는 클라우드 스토리지 사용
3. **임시 파일**: 세션 기반으로 처리 (현재 구현됨)

### 환경 변수 보안

- `SECRET_KEY`: 반드시 강력한 랜덤 문자열 사용
- `DATABASE_URL`: Railway가 자동 설정 (노출되지 않음)
- `MAIL_PASSWORD`: Gmail 앱 비밀번호 사용

### 무료 플랜 제한

- 월간 크레딧: $5 (약 500시간)
- 디스크 공간: 1GB
- 네트워크: 100GB/월
- 데이터베이스: PostgreSQL 256MB

---

## 📊 배포 체크리스트

### 배포 전 확인

- [x] Procfile 생성 ✅
- [x] railway.json 생성 ✅
- [x] requirements.txt에 gunicorn 추가 ✅
- [x] app.py PORT 환경 변수 지원 ✅
- [x] 배포 가이드 문서 작성 ✅

### 배포 중 작업

- [ ] Railway 프로젝트 생성
- [ ] GitHub 저장소 연결
- [ ] PostgreSQL 데이터베이스 추가
- [ ] 환경 변수 설정
- [ ] 배포 시작

### 배포 후 작업

- [ ] 데이터베이스 마이그레이션 실행
- [ ] 기본 기능 테스트
- [ ] 도메인 설정
- [ ] 모니터링 설정

---

## 📚 참고 문서

- **RAILWAY_DEPLOYMENT.md**: 상세한 배포 가이드
- [Railway 공식 문서](https://docs.railway.app/)
- [Gunicorn 문서](https://gunicorn.org/)

---

**다음 단계**: Railway 대시보드에서 프로젝트를 생성하고 배포를 시작하세요!

