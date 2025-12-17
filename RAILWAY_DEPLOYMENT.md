# 🚂 Railway 배포 가이드

**작성일**: 2025-12-16  
**플랫폼**: Railway.app  
**상태**: ✅ 배포 준비 완료

---

## 📋 Railway 배포 전 체크리스트

### 필수 파일 확인

- [x] `Procfile` - Railway가 애플리케이션을 시작하는 방법 정의 ✅
- [x] `railway.json` - Railway 빌드 및 배포 설정 ✅
- [x] `requirements.txt` - Python 패키지 의존성 ✅
- [x] `app.py` - Flask 애플리케이션 진입점 ✅
- [x] `.gitignore` - 불필요한 파일 제외 ✅

### 환경 변수 설정

Railway 대시보드에서 다음 환경 변수를 설정해야 합니다:

#### 필수 환경 변수

| 변수명 | 설명 | 예시 값 |
|--------|------|---------|
| `FLASK_ENV` | Flask 환경 | `production` |
| `SECRET_KEY` | Flask 세션 암호화 키 | `your-secret-key-here` (랜덤 문자열) |
| `DATABASE_URL` | PostgreSQL 데이터베이스 URL | Railway가 자동 설정 |
| `PORT` | 서버 포트 | Railway가 자동 설정 |

#### 선택적 환경 변수

| 변수명 | 설명 | 예시 값 |
|--------|------|---------|
| `MAIL_SERVER` | 이메일 서버 | `smtp.gmail.com` |
| `MAIL_PORT` | 이메일 포트 | `587` |
| `MAIL_USE_TLS` | TLS 사용 여부 | `True` |
| `MAIL_USERNAME` | 이메일 계정 | `your-email@gmail.com` |
| `MAIL_PASSWORD` | 이메일 앱 비밀번호 | `your-app-password` |
| `MAIL_DEFAULT_SENDER` | 기본 발신자 | `your-email@gmail.com` |

---

## 🚀 Railway 배포 단계

### 1단계: Railway 계정 생성 및 프로젝트 생성

1. [Railway.app](https://railway.app)에 접속하여 계정 생성
2. "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. GitHub 저장소 선택 (`jisungs/sal_cal`)

### 2단계: PostgreSQL 데이터베이스 추가

1. Railway 대시보드에서 프로젝트 선택
2. "New" 버튼 클릭
3. "Database" → "Add PostgreSQL" 선택
4. PostgreSQL이 자동으로 생성되고 `DATABASE_URL` 환경 변수가 자동 설정됨

### 3단계: 환경 변수 설정

Railway 대시보드 → 프로젝트 → Variables 탭에서 다음 변수 설정:

#### 필수 변수

```bash
FLASK_ENV=production
SECRET_KEY=<랜덤 문자열 생성>
```

**SECRET_KEY 생성 방법**:
```python
import secrets
print(secrets.token_hex(32))
```

또는 Python에서:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 선택적 변수 (이메일 기능 사용 시)

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**Gmail 앱 비밀번호 생성 방법**:
1. Google 계정 설정 → 보안
2. 2단계 인증 활성화
3. 앱 비밀번호 생성
4. 생성된 비밀번호를 `MAIL_PASSWORD`에 설정

### 4단계: 데이터베이스 마이그레이션

Railway는 자동으로 빌드 및 배포를 시작하지만, 데이터베이스 마이그레이션은 수동으로 실행해야 합니다.

#### 방법 1: Railway CLI 사용 (권장)

```bash
# Railway CLI 설치
npm i -g @railway/cli

# Railway 로그인
railway login

# 프로젝트 연결
railway link

# 데이터베이스 마이그레이션 실행
railway run flask db upgrade
```

#### 방법 2: Railway 대시보드에서 실행

1. Railway 대시보드 → 프로젝트 → "Deployments" 탭
2. 최신 배포 선택
3. "View Logs" 클릭
4. 터미널에서 다음 명령어 실행:
```bash
flask db upgrade
```

### 5단계: 도메인 설정 (선택사항)

1. Railway 대시보드 → 프로젝트 → "Settings" 탭
2. "Generate Domain" 클릭하여 무료 도메인 생성
3. 또는 커스텀 도메인 연결 가능

---

## 🔧 Railway 배포 설정 파일

### Procfile

```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**설명**:
- `web`: Railway가 웹 서비스를 시작하는 명령어
- `gunicorn`: 프로덕션 WSGI 서버
- `app:app`: `app.py` 파일의 `app` 객체
- `--bind 0.0.0.0:$PORT`: Railway가 제공하는 PORT 환경 변수 사용
- `--workers 2`: 워커 프로세스 수 (동시 요청 처리)
- `--timeout 120`: 요청 타임아웃 (초 단위)

### railway.json

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**설명**:
- `NIXPACKS`: Railway의 자동 빌드 시스템 (Python 자동 감지)
- `buildCommand`: 패키지 설치 명령어
- `startCommand`: 애플리케이션 시작 명령어
- `restartPolicyType`: 재시작 정책 (실패 시 재시작)

---

## 📝 코드 수정 사항

### 1. app.py 포트 설정 수정 (Railway 호환)

Railway는 `PORT` 환경 변수를 제공하므로, `app.py`를 수정할 필요는 없습니다. `Procfile`에서 `gunicorn`이 `$PORT`를 사용합니다.

하지만 개발 환경에서도 Railway와 동일하게 작동하도록 `app.py`를 수정할 수 있습니다:

```python
# app.py
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # Railway는 PORT 환경 변수를 제공, 없으면 기본값 5001 사용
    port = int(os.environ.get('PORT', os.environ.get('FLASK_RUN_PORT', 5001)))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
```

### 2. config.py 프로덕션 설정 확인

`config.py`의 `ProductionConfig`가 이미 Railway 환경에 맞게 설정되어 있습니다:

- ✅ `DATABASE_URL` 환경 변수 사용
- ✅ `SECRET_KEY` 환경 변수 필수 확인
- ✅ HTTPS 설정 (`SESSION_COOKIE_SECURE = True`)

---

## 🗄️ 데이터베이스 마이그레이션

### 초기 마이그레이션 실행

Railway 배포 후 데이터베이스 마이그레이션을 실행해야 합니다:

```bash
# Railway CLI 사용
railway run flask db upgrade

# 또는 Railway 대시보드 터미널에서
flask db upgrade
```

### 마이그레이션 파일 확인

현재 마이그레이션 파일:
- `migrations/versions/` 폴더에 마이그레이션 파일이 있는지 확인
- 없으면 초기 마이그레이션 생성 필요

---

## 📁 파일 시스템 및 저장소

### 업로드 파일 및 출력 파일

Railway는 **임시 파일 시스템**을 사용하므로, 업로드된 파일과 생성된 파일은 **영구 저장소**에 저장해야 합니다.

#### 옵션 1: Railway Volume 사용 (권장)

1. Railway 대시보드 → 프로젝트 → "New" → "Volume" 추가
2. 마운트 경로 설정 (예: `/data`)
3. `config.py`에서 경로 수정:

```python
# config.py
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/data/uploads')
OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', '/data/outputs')
```

#### 옵션 2: 클라우드 스토리지 사용 (S3, Cloudinary 등)

- AWS S3
- Cloudinary
- Railway의 자체 스토리지 서비스

#### 옵션 3: 데이터베이스에 저장 (작은 파일만)

- 파일을 Base64로 인코딩하여 데이터베이스에 저장
- 큰 파일에는 권장하지 않음

---

## 🔐 보안 설정

### 환경 변수 보안

1. **SECRET_KEY**: 반드시 강력한 랜덤 문자열 사용
2. **DATABASE_URL**: Railway가 자동 설정 (노출되지 않음)
3. **MAIL_PASSWORD**: Gmail 앱 비밀번호 사용 (일반 비밀번호 아님)

### HTTPS 설정

Railway는 자동으로 HTTPS를 제공하므로:
- `SESSION_COOKIE_SECURE = True` (이미 설정됨)
- `SESSION_COOKIE_HTTPONLY = True` (이미 설정됨)

---

## 🧪 배포 후 테스트

### 1. 기본 기능 테스트

- [ ] 메인 페이지 접속 확인
- [ ] 회원가입 기능 테스트
- [ ] 로그인 기능 테스트
- [ ] 파일 업로드 기능 테스트
- [ ] 급여명세서 생성 기능 테스트
- [ ] 다운로드 기능 테스트

### 2. 데이터베이스 테스트

- [ ] 사용자 생성 확인
- [ ] 세션 유지 확인
- [ ] 데이터 저장 확인

### 3. 성능 테스트

- [ ] 페이지 로딩 속도 확인
- [ ] 동시 요청 처리 확인
- [ ] 파일 업로드/다운로드 속도 확인

---

## 🐛 문제 해결

### 문제 1: 빌드 실패

**증상**: Railway 빌드가 실패함

**해결 방법**:
1. `requirements.txt` 확인
2. 빌드 로그 확인
3. Python 버전 확인 (Railway는 자동 감지)

### 문제 2: 애플리케이션 시작 실패

**증상**: 배포는 성공했지만 애플리케이션이 시작되지 않음

**해결 방법**:
1. `Procfile` 확인
2. 환경 변수 확인 (`SECRET_KEY`, `DATABASE_URL`)
3. 로그 확인

### 문제 3: 데이터베이스 연결 실패

**증상**: `DATABASE_URL` 오류

**해결 방법**:
1. PostgreSQL 서비스가 추가되었는지 확인
2. `DATABASE_URL` 환경 변수가 자동 설정되었는지 확인
3. 데이터베이스 마이그레이션 실행

### 문제 4: 정적 파일이 로드되지 않음

**증상**: CSS, JavaScript 파일이 로드되지 않음

**해결 방법**:
1. `STATIC_FOLDER` 경로 확인
2. `url_for('static', ...)` 사용 확인
3. 빌드 시 정적 파일이 포함되었는지 확인

---

## 📊 Railway 무료 플랜 제한

### 무료 플랜 제한사항

- **월간 크레딧**: $5 (약 500시간)
- **디스크 공간**: 1GB
- **네트워크**: 100GB/월
- **데이터베이스**: PostgreSQL 256MB

### 권장 사항

- 무료 플랜으로 시작하여 테스트
- 트래픽이 많아지면 유료 플랜 고려
- 디스크 공간 모니터링 (업로드 파일 관리)

---

## 🎯 배포 체크리스트

### 배포 전

- [ ] `Procfile` 생성 및 확인
- [ ] `railway.json` 생성 및 확인
- [ ] `requirements.txt`에 `gunicorn` 추가 확인
- [ ] `.gitignore`에 불필요한 파일 제외 확인
- [ ] 큰 파일 제거 확인 (GitHub 100MB 제한)

### 배포 중

- [ ] Railway 프로젝트 생성
- [ ] GitHub 저장소 연결
- [ ] PostgreSQL 데이터베이스 추가
- [ ] 환경 변수 설정
- [ ] 배포 시작

### 배포 후

- [ ] 데이터베이스 마이그레이션 실행
- [ ] 기본 기능 테스트
- [ ] 도메인 설정 (선택사항)
- [ ] 모니터링 설정

---

## 📚 참고 자료

- [Railway 공식 문서](https://docs.railway.app/)
- [Railway Python 가이드](https://docs.railway.app/guides/python)
- [Gunicorn 문서](https://gunicorn.org/)

---

**다음 단계**: Railway 대시보드에서 프로젝트를 생성하고 GitHub 저장소를 연결하세요!

