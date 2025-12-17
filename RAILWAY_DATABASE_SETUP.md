# 🗄️ Railway 데이터베이스 설정 가이드

**작성일**: 2025-12-17  
**목적**: Railway 배포 후 PostgreSQL 데이터베이스 연결 및 마이그레이션 설정

---

## ⚠️ 중요: 회원가입 오류 해결

회원가입 시 **Internal Server Error**가 발생하는 경우, 대부분 **데이터베이스 마이그레이션이 실행되지 않아서** 발생합니다.

---

## 📋 단계별 설정 가이드

### 1단계: PostgreSQL 데이터베이스 추가

1. Railway 대시보드 → 프로젝트 선택
2. **"New"** 버튼 클릭
3. **"Database"** → **"Add PostgreSQL"** 선택
4. PostgreSQL이 자동으로 생성되고 `DATABASE_URL` 환경 변수가 자동 설정됨

### 2단계: 환경 변수 확인

Railway 대시보드 → 프로젝트 → **Variables** 탭에서 확인:

- ✅ `DATABASE_URL` - PostgreSQL 추가 시 자동 설정됨
- ✅ `FLASK_ENV=production` - 수동 설정 필요
- ✅ `SECRET_KEY` - 수동 설정 필요

### 3단계: 데이터베이스 마이그레이션 실행 ⭐ **필수**

데이터베이스 테이블을 생성하기 위해 마이그레이션을 실행해야 합니다.

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

#### 방법 2: Railway 대시보드 터미널 사용

1. Railway 대시보드 → 프로젝트 선택
2. **"Deployments"** 탭 → 최신 배포 선택
3. **"View Logs"** 또는 **"Shell"** 클릭
4. 터미널에서 다음 명령어 실행:

```bash
flask db upgrade
```

#### 방법 3: Railway 대시보드에서 직접 실행

1. Railway 대시보드 → 프로젝트 선택
2. **"Deployments"** 탭
3. 최신 배포의 **"..."** 메뉴 → **"Run Command"**
4. 명령어 입력: `flask db upgrade`
5. 실행

---

## ✅ 마이그레이션 확인

마이그레이션이 성공적으로 실행되면 다음 메시지가 표시됩니다:

```
INFO  [alembic.runtime.migration] Running upgrade  -> 34cb4514bf11, Initial migration: User model
INFO  [alembic.runtime.migration] Running upgrade 34cb4514bf11 -> 8ea715dfd8b4, Add phase 4 models
```

### 데이터베이스 연결 확인

앱 로그에서 다음 메시지를 확인하세요:

```
✅ 데이터베이스 연결 성공
✅ 데이터베이스 테이블 확인 완료
```

만약 다음 메시지가 보이면 마이그레이션을 실행하세요:

```
⚠️ 'users' 테이블이 존재하지 않습니다. 마이그레이션을 실행하세요: flask db upgrade
```

---

## 🐛 문제 해결

### 문제 1: "relation 'users' does not exist" 오류

**원인**: 데이터베이스 마이그레이션이 실행되지 않음

**해결 방법**:
```bash
railway run flask db upgrade
```

### 문제 2: "DATABASE_URL" 환경 변수 없음

**원인**: PostgreSQL 데이터베이스가 추가되지 않음

**해결 방법**:
1. Railway 대시보드 → 프로젝트 → **"New"** → **"Database"** → **"Add PostgreSQL"**
2. `DATABASE_URL` 환경 변수가 자동으로 설정되는지 확인

### 문제 3: "could not connect to server" 오류

**원인**: 데이터베이스 연결 정보가 잘못됨

**해결 방법**:
1. Railway 대시보드 → 프로젝트 → **Variables** 탭
2. `DATABASE_URL` 값 확인
3. PostgreSQL 서비스가 실행 중인지 확인

### 문제 4: 마이그레이션 실행 후에도 오류 발생

**해결 방법**:
1. Railway 대시보드 → 프로젝트 → **"Deployments"** 탭
2. 최신 배포 **"Redeploy"** 클릭
3. 앱이 재시작되면 다시 시도

---

## 📊 마이그레이션 파일 확인

현재 프로젝트의 마이그레이션 파일:

- `migrations/versions/34cb4514bf11_initial_migration_user_model.py` - User 모델 생성
- `migrations/versions/8ea715dfd8b4_add_phase_4_models_payrollcalculation_.py` - Phase 4 모델 추가

---

## 🔍 데이터베이스 상태 확인

### Railway CLI로 확인

```bash
# 데이터베이스 연결 테스트
railway run python -c "from app import create_app; app = create_app('production'); app.app_context().push(); from app import db; print('Tables:', db.engine.table_names())"
```

### 앱 로그 확인

Railway 대시보드 → 프로젝트 → **"Deployments"** → **"View Logs"**에서 확인:

- ✅ 정상: `데이터베이스 연결 성공`, `데이터베이스 테이블 확인 완료`
- ❌ 오류: `데이터베이스 연결 실패`, `'users' 테이블이 존재하지 않습니다`

---

## 📝 체크리스트

배포 후 확인사항:

- [ ] PostgreSQL 데이터베이스 추가됨
- [ ] `DATABASE_URL` 환경 변수 자동 설정됨
- [ ] `FLASK_ENV=production` 설정됨
- [ ] `SECRET_KEY` 설정됨
- [ ] `flask db upgrade` 실행 완료
- [ ] 앱 로그에서 "데이터베이스 연결 성공" 확인
- [ ] 회원가입 기능 정상 작동 확인

---

## 🚀 빠른 해결 방법

회원가입 오류가 발생하면:

1. **Railway CLI 설치 및 로그인**
   ```bash
   npm i -g @railway/cli
   railway login
   railway link
   ```

2. **마이그레이션 실행**
   ```bash
   railway run flask db upgrade
   ```

3. **앱 재배포** (선택사항)
   - Railway 대시보드 → **"Redeploy"** 클릭

4. **테스트**
   - 웹사이트에서 회원가입 시도

---

**참고**: 이 가이드는 Railway 배포 후 데이터베이스 설정을 위한 것입니다. 로컬 개발 환경에서는 `python app.py` 실행 시 자동으로 SQLite 데이터베이스가 생성됩니다.

