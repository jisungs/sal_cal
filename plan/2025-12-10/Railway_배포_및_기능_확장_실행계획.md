# 🚀 Railway 배포 및 기능 확장 실행 계획

**목표**: 프로덕션 환경에서 사용 가능한 웹 서비스 구축  
**배포 플랫폼**: Railway  
**기간**: 4-6주 (단계별 배포 가능)  
**작성일**: 2025-01-XX

---

## 📋 프로젝트 개요

### 현재 상태
- ✅ 기본 웹 애플리케이션 완성 (Flask)
- ✅ 로컬 실행 가능
- ✅ 급여 계산 및 파일 생성 기능 완료

### 목표 상태
- ✅ Railway 프로덕션 배포
- ✅ 사용자 인증 시스템 (로그인/로그아웃)
- ✅ 사용자 피드백 게시판
- ✅ 사용자 데이터 수집 및 분석
- ✅ 사용자 행동 추적 (Analytics)

---

## 🎯 요구사항 분석

### 1. 로그인/로그아웃 기능
**목적**: 사용자 식별 및 개인화된 서비스 제공

**필수 기능**:
- 회원가입 (이메일/소셜 로그인)
- 로그인/로그아웃
- 비밀번호 재설정
- 세션 관리
- 사용자 프로필 관리

**기술 선택**:
- Flask-Login: 세션 관리
- Flask-Bcrypt: 비밀번호 암호화
- Flask-Mail: 이메일 인증
- OAuth2 (선택): 소셜 로그인 (Google, Kakao)

### 2. 사용자 의견 수렴 게시판
**목적**: 사용자 피드백 수집 및 커뮤니티 형성

**필수 기능**:
- 게시글 작성/수정/삭제
- 댓글 기능
- 좋아요/추천 기능
- 카테고리 분류
- 검색 기능
- 관리자 답변 기능

**기술 선택**:
- Flask-WTF: 폼 처리 및 CSRF 보호
- Flask-Migrate: 데이터베이스 마이그레이션
- Rich Text Editor (TinyMCE 또는 CKEditor)

### 3. 사용자 데이터 수집
**목적**: 서비스 개선 및 통계 분석

**수집 데이터**:
- 급여 계산 결과 (금액, 직원 수 등)
- 사용 빈도 (일/주/월별)
- 생성된 파일 수 (PDF/엑셀)
- 사용자별 통계

**기술 선택**:
- 데이터베이스: PostgreSQL (Railway 기본 제공)
- 백그라운드 작업: Celery + Redis (선택)
- 데이터 분석: Pandas (이미 사용 중)

### 4. 사용자 행동 추적 (Analytics)
**목적**: UX 개선 및 기능 최적화

**추적 데이터**:
- 페이지뷰 (어떤 페이지를 얼마나 방문)
- 버튼 클릭 이벤트
- 파일 업로드/다운로드 이벤트
- 에러 발생 이벤트
- 사용자 플로우 (사용자 여정)

**기술 선택**:
- 클라이언트: JavaScript 이벤트 추적
- 서버: Flask 로깅 + 데이터베이스 저장
- 분석 도구: 자체 대시보드 또는 Google Analytics 연동

---

## 🏗️ 아키텍처 설계

### 데이터베이스 스키마 설계

```sql
-- 사용자 테이블
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE
);

-- 세션 테이블 (Flask-Session)
CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    data BYTEA,
    expiry TIMESTAMP
);

-- 게시판 테이블
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    category VARCHAR(50),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 댓글 테이블
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 사용자 활동 로그 테이블
CREATE TABLE user_activities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    activity_type VARCHAR(50) NOT NULL, -- 'page_view', 'button_click', 'file_upload', etc.
    activity_data JSONB, -- 상세 정보 (JSON 형식)
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 급여 계산 결과 테이블
CREATE TABLE payroll_calculations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    employee_count INTEGER,
    total_payroll DECIMAL(15, 2),
    total_deductions DECIMAL(15, 2),
    total_net_pay DECIMAL(15, 2),
    period VARCHAR(7), -- 'YYYY-MM'
    calculation_data JSONB, -- 상세 계산 결과
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 파일 생성 로그 테이블
CREATE TABLE file_generations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    file_type VARCHAR(10), -- 'excel', 'pdf', 'both'
    file_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 프로젝트 구조 개선

```
salary_cal/
├── app.py                          # Flask 메인 애플리케이션
├── config.py                       # 설정 파일 (개발/프로덕션 분리)
├── requirements.txt                 # 의존성 목록
│
├── app/                            # 애플리케이션 패키지
│   ├── __init__.py                 # Flask 앱 팩토리
│   ├── models/                     # 데이터베이스 모델
│   │   ├── __init__.py
│   │   ├── user.py                # User 모델
│   │   ├── post.py                 # Post 모델
│   │   ├── activity.py             # Activity 모델
│   │   └── payroll.py             # PayrollCalculation 모델
│   │
│   ├── routes/                     # 라우트 블루프린트
│   │   ├── __init__.py
│   │   ├── auth.py                 # 인증 라우트
│   │   ├── main.py                 # 메인 라우트
│   │   ├── board.py                # 게시판 라우트
│   │   └── api.py                 # API 라우트 (Analytics)
│   │
│   ├── forms/                      # 폼 클래스
│   │   ├── __init__.py
│   │   ├── auth_forms.py          # 로그인/회원가입 폼
│   │   └── board_forms.py         # 게시판 폼
│   │
│   ├── utils/                      # 유틸리티
│   │   ├── __init__.py
│   │   ├── analytics.py            # 분석 유틸리티
│   │   └── decorators.py          # 데코레이터 (로그인 필요 등)
│   │
│   └── templates/                  # HTML 템플릿
│       ├── base.html
│       ├── auth/
│       │   ├── login.html
│       │   ├── register.html
│       │   └── reset_password.html
│       ├── board/
│       │   ├── list.html
│       │   ├── detail.html
│       │   └── write.html
│       └── admin/
│           └── analytics.html
│
├── migrations/                     # 데이터베이스 마이그레이션
│
├── payroll_generator/              # 기존 모듈 (유지)
│
└── web/                            # 정적 파일
    ├── static/
    │   ├── css/
    │   ├── js/
    │   │   └── analytics.js        # 클라이언트 분석 스크립트
    │   └── img/
```

---

## 📅 단계별 실행 계획

### Phase 1: 인프라 및 기본 설정 (1주)

#### Day 1-2: 프로젝트 구조 개선
- [x] Flask 애플리케이션 팩토리 패턴으로 리팩토링 ✅
- [x] Blueprint 구조로 라우트 분리 ✅
- [x] 설정 파일 분리 (개발/프로덕션) ✅
- [x] 환경 변수 관리 (.env 파일) ✅

#### Day 1-2 추가 작업: 네비게이션 메뉴바 구현 ✅
- [x] 상단 고정 네비게이션 메뉴바 구현 ✅
- [x] 메뉴 항목: Home, About, Design, Contact, Login/Sign in ✅
- [x] 반응형 디자인 (모바일 햄버거 메뉴) ✅
- [x] 각 페이지 라우트 생성 및 연결 ✅
- [x] pages Blueprint 생성 (About, Design, Contact) ✅
- [x] 네비게이션 스타일링 및 활성 상태 표시 ✅
- [ ] 로그인 상태에 따른 메뉴 동적 변경 (Phase 2에서 완성)

**작업 내용**:
```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name.capitalize()}Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Blueprint 등록
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    return app
```

#### Day 3-4: 데이터베이스 설정
- [ ] PostgreSQL 설정 (로컬 개발용)
- [ ] SQLAlchemy 모델 정의
- [ ] Flask-Migrate 초기화
- [ ] 기본 마이그레이션 생성

**필수 패키지 추가**:
```txt
flask-sqlalchemy>=3.0.0
flask-migrate>=4.0.0
psycopg2-binary>=2.9.0  # PostgreSQL 드라이버
flask-login>=0.6.0
flask-bcrypt>=1.0.0
flask-wtf>=1.1.0
flask-mail>=0.9.1
python-dotenv>=1.0.0
```

#### Day 5: Railway 계정 및 프로젝트 설정
- [ ] Railway 계정 생성
- [ ] 프로젝트 생성
- [ ] PostgreSQL 서비스 추가
- [ ] 환경 변수 설정
- [ ] 배포 테스트 (기본 앱)

**Railway 설정 파일**:
```json
// railway.json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

### Phase 2: 사용자 인증 시스템 (1주)

#### Day 1-2: 사용자 모델 및 기본 인증
- [ ] User 모델 생성
- [ ] 회원가입 기능 구현
- [ ] 로그인/로그아웃 기능 구현
- [ ] 비밀번호 해싱 (Flask-Bcrypt)

**User 모델 예시**:
```python
# app/models/user.py
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # 관계
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    activities = db.relationship('UserActivity', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

#### Day 3: 세션 관리 및 보안
- [ ] Flask-Login 설정
- [ ] 세션 타임아웃 설정
- [ ] CSRF 보호 (Flask-WTF)
- [ ] 로그인 필요 데코레이터 구현

#### Day 4: 비밀번호 재설정 기능
- [ ] 이메일 발송 기능 (Flask-Mail)
- [ ] 토큰 기반 비밀번호 재설정
- [ ] 이메일 템플릿 작성

#### Day 5: 소셜 로그인 (선택사항)
- [ ] Google OAuth2 연동
- [ ] Kakao OAuth2 연동 (한국 사용자용)

---

### Phase 3: 게시판 기능 (1주)

#### Day 1-2: 게시판 모델 및 기본 CRUD
- [ ] Post 모델 생성
- [ ] Comment 모델 생성
- [ ] 게시글 작성/수정/삭제 기능
- [ ] 게시글 목록 및 상세보기

**Post 모델 예시**:
```python
# app/models/post.py
from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), default='general')
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
```

#### Day 3: 댓글 기능
- [ ] 댓글 작성/수정/삭제
- [ ] 댓글 목록 표시
- [ ] 댓글 권한 관리

#### Day 4: 고급 기능
- [ ] 검색 기능 (제목/내용)
- [ ] 카테고리 필터링
- [ ] 좋아요 기능
- [ ] 페이지네이션

#### Day 5: 관리자 기능
- [ ] 관리자 대시보드
- [ ] 게시글 관리 (삭제/고정)
- [ ] 댓글 관리

---

### Phase 4: 데이터 수집 시스템 (1주)

#### Day 1-2: 데이터 모델 설계 및 구현
- [ ] PayrollCalculation 모델 생성
- [ ] FileGeneration 모델 생성
- [ ] 사용자 활동 로그 모델 생성
- [ ] 데이터베이스 마이그레이션

**활동 로그 모델**:
```python
# app/models/activity.py
from app import db
from datetime import datetime
import json

class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    activity_type = db.Column(db.String(50), nullable=False, index=True)
    activity_data = db.Column(db.JSON)  # 상세 정보 (JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    @property
    def data_dict(self):
        return json.loads(self.activity_data) if isinstance(self.activity_data, str) else self.activity_data
```

#### Day 3: 급여 계산 데이터 수집
- [ ] 계산 결과 저장 로직 추가
- [ ] 파일 생성 로그 저장
- [ ] 사용자별 통계 집계

**수집 예시**:
```python
# app/utils/analytics.py
from app import db
from app.models.activity import UserActivity
from app.models.payroll import PayrollCalculation
from flask import request

def log_payroll_calculation(user_id, calculation_data):
    """급여 계산 결과 저장"""
    calculation = PayrollCalculation(
        user_id=user_id,
        employee_count=calculation_data.get('employee_count'),
        total_payroll=calculation_data.get('total_payroll'),
        total_deductions=calculation_data.get('total_deductions'),
        total_net_pay=calculation_data.get('total_net_pay'),
        period=calculation_data.get('period'),
        calculation_data=calculation_data
    )
    db.session.add(calculation)
    db.session.commit()

def log_activity(user_id, activity_type, activity_data=None):
    """사용자 활동 로그 저장"""
    activity = UserActivity(
        user_id=user_id,
        activity_type=activity_type,
        activity_data=activity_data or {},
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(activity)
    db.session.commit()
```

#### Day 4: 통계 API 구현
- [ ] 사용자별 통계 조회 API
- [ ] 전체 통계 조회 API (관리자)
- [ ] 시간대별 통계 조회

#### Day 5: 데이터 시각화 (선택사항)
- [ ] Chart.js를 사용한 통계 그래프
- [ ] 관리자 대시보드에 통계 표시

---

### Phase 5: 사용자 행동 추적 (1주)

#### Day 1-2: 클라이언트 사이드 추적 구현
- [ ] JavaScript 이벤트 추적 스크립트 작성
- [ ] 페이지뷰 추적
- [ ] 버튼 클릭 이벤트 추적
- [ ] 폼 제출 이벤트 추적

**클라이언트 스크립트 예시**:
```javascript
// web/static/js/analytics.js
(function() {
    'use strict';
    
    // 페이지뷰 추적
    function trackPageView() {
        fetch('/api/analytics/track', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: 'page_view',
                page: window.location.pathname,
                timestamp: new Date().toISOString()
            })
        });
    }
    
    // 버튼 클릭 추적
    function trackButtonClick(buttonId, buttonText) {
        fetch('/api/analytics/track', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: 'button_click',
                element_id: buttonId,
                element_text: buttonText,
                page: window.location.pathname,
                timestamp: new Date().toISOString()
            })
        });
    }
    
    // 파일 업로드 추적
    function trackFileUpload(fileName, fileSize) {
        fetch('/api/analytics/track', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: 'file_upload',
                file_name: fileName,
                file_size: fileSize,
                timestamp: new Date().toISOString()
            })
        });
    }
    
    // 이벤트 리스너 등록
    document.addEventListener('DOMContentLoaded', function() {
        trackPageView();
        
        // 모든 버튼에 클릭 추적 추가
        document.querySelectorAll('button, .btn, a.btn').forEach(function(btn) {
            btn.addEventListener('click', function() {
                trackButtonClick(btn.id || btn.className, btn.textContent.trim());
            });
        });
        
        // 파일 업로드 추적
        document.querySelectorAll('input[type="file"]').forEach(function(input) {
            input.addEventListener('change', function(e) {
                if (e.target.files.length > 0) {
                    const file = e.target.files[0];
                    trackFileUpload(file.name, file.size);
                }
            });
        });
    });
})();
```

#### Day 3: 서버 사이드 추적 API
- [ ] Analytics API 엔드포인트 구현
- [ ] 이벤트 데이터 저장
- [ ] 요청 정보 수집 (IP, User-Agent 등)

**API 엔드포인트**:
```python
# app/routes/api.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.utils.analytics import log_activity
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/analytics/track', methods=['POST'])
@login_required
def track_analytics():
    """사용자 행동 추적 API"""
    data = request.get_json()
    
    log_activity(
        user_id=current_user.id,
        activity_type=data.get('type'),
        activity_data=data
    )
    
    return jsonify({'status': 'success'}), 200
```

#### Day 4: 사용자 플로우 분석
- [ ] 사용자 여정 추적
- [ ] 페이지 간 이동 추적
- [ ] 이탈 지점 분석

#### Day 5: 분석 대시보드 구현
- [ ] 관리자용 분석 대시보드
- [ ] 실시간 통계 표시
- [ ] 사용자 행동 히트맵 (선택사항)

---

### Phase 6: Railway 배포 및 최적화 (1주)

#### Day 1-2: Railway 배포 설정
- [ ] Railway 프로젝트 설정
- [ ] PostgreSQL 데이터베이스 연결
- [ ] 환경 변수 설정
- [ ] 빌드 설정 (requirements.txt, Procfile)

**Procfile**:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

**requirements.txt 업데이트**:
```txt
# 기존 패키지
flask>=3.0.0
flask-cors>=4.0.0
werkzeug>=3.0.0
openpyxl>=3.1.0
pandas>=2.0.0
reportlab>=4.0.0
pillow>=10.0.0

# 새로운 패키지
flask-sqlalchemy>=3.0.0
flask-migrate>=4.0.0
psycopg2-binary>=2.9.0
flask-login>=0.6.0
flask-bcrypt>=1.0.0
flask-wtf>=1.1.0
flask-mail>=0.9.1
python-dotenv>=1.0.0
gunicorn>=21.2.0
```

#### Day 3: 보안 강화
- [ ] HTTPS 설정 (Railway 자동)
- [ ] 세션 보안 설정
- [ ] CSRF 토큰 검증
- [ ] SQL Injection 방지 (SQLAlchemy ORM 사용)
- [ ] XSS 방지 (템플릿 이스케이핑)

#### Day 4: 성능 최적화
- [ ] 데이터베이스 인덱스 최적화
- [ ] 쿼리 최적화 (N+1 문제 해결)
- [ ] 캐싱 전략 (Redis 선택사항)
- [ ] 정적 파일 CDN (선택사항)

#### Day 5: 모니터링 및 로깅
- [ ] 에러 로깅 설정
- [ ] 성능 모니터링
- [ ] 사용자 활동 로그 모니터링
- [ ] 알림 설정 (에러 발생 시)

---

## 🔒 보안 고려사항

### 1. 인증 및 권한
- ✅ 비밀번호 해싱 (bcrypt)
- ✅ 세션 타임아웃 설정
- ✅ CSRF 보호
- ✅ SQL Injection 방지 (ORM 사용)
- ✅ XSS 방지 (템플릿 이스케이핑)

### 2. 데이터 보호
- ✅ 개인정보 암호화 (필요시)
- ✅ 로그 데이터 익명화 옵션
- ✅ GDPR 준수 (개인정보 처리 방침)

### 3. API 보안
- ✅ Rate Limiting (요청 제한)
- ✅ API 키 인증 (필요시)
- ✅ 입력 검증 및 Sanitization

---

## 📊 데이터 수집 전략

### 수집할 데이터

#### 1. 사용자 기본 정보
- 이메일 (암호화 저장)
- 가입일
- 마지막 로그인 시간
- 사용 빈도

#### 2. 급여 계산 데이터
- 계산 횟수
- 직원 수
- 총 급여액
- 총 공제액
- 실수령액
- 계산 기간

#### 3. 파일 생성 데이터
- 생성된 파일 수 (PDF/엑셀)
- 파일 생성 빈도
- 파일 다운로드 횟수

#### 4. 사용자 행동 데이터
- 페이지뷰
- 버튼 클릭
- 폼 제출
- 에러 발생
- 사용자 플로우

### 데이터 분석 목표
- 사용자 행동 패턴 분석
- 기능 사용률 분석
- 에러 발생 패턴 분석
- 사용자 만족도 측정

---

## 🛠️ 기술 스택 최종 정리

### 백엔드
- **웹 프레임워크**: Flask 3.0+
- **데이터베이스**: PostgreSQL (Railway)
- **ORM**: SQLAlchemy
- **인증**: Flask-Login, Flask-Bcrypt
- **폼 처리**: Flask-WTF
- **마이그레이션**: Flask-Migrate
- **이메일**: Flask-Mail
- **배포**: Railway
- **WSGI 서버**: Gunicorn

### 프론트엔드
- **템플릿 엔진**: Jinja2
- **CSS 프레임워크**: Bootstrap 5 (선택)
- **JavaScript**: Vanilla JS + Analytics 스크립트
- **차트 라이브러리**: Chart.js (통계 시각화)

### 개발 도구
- **버전 관리**: Git
- **환경 변수**: python-dotenv
- **로깅**: Python logging
- **테스트**: pytest (선택)

---

## 📝 체크리스트

### Phase 1: 인프라 (1주)
- [ ] 프로젝트 구조 리팩토링
- [ ] 데이터베이스 설정
- [ ] Railway 계정 및 프로젝트 생성
- [ ] 기본 배포 테스트

### Phase 2: 인증 (1주)
- [ ] 사용자 모델 생성
- [ ] 회원가입/로그인 구현
- [ ] 세션 관리
- [ ] 비밀번호 재설정

### Phase 3: 게시판 (1주)
- [ ] 게시판 모델 생성
- [ ] CRUD 기능 구현
- [ ] 댓글 기능
- [ ] 검색 및 필터링

### Phase 4: 데이터 수집 (1주)
- [ ] 데이터 모델 생성
- [ ] 수집 로직 구현
- [ ] 통계 API 구현
- [ ] 데이터 시각화

### Phase 5: 행동 추적 (1주)
- [ ] 클라이언트 추적 스크립트
- [ ] 서버 API 구현
- [ ] 분석 대시보드

### Phase 6: 배포 (1주)
- [ ] Railway 배포 설정
- [ ] 보안 강화
- [ ] 성능 최적화
- [ ] 모니터링 설정

---

## 🎯 우선순위

### Must Have (필수)
1. ✅ 사용자 인증 시스템
2. ✅ 데이터베이스 설정
3. ✅ 기본 데이터 수집
4. ✅ Railway 배포

### Should Have (권장)
1. ✅ 게시판 기능
2. ✅ 사용자 행동 추적
3. ✅ 관리자 대시보드

### Nice to Have (선택)
1. 소셜 로그인
2. 실시간 통계
3. 이메일 알림
4. 고급 분석 기능

---

## 📈 예상 일정

| Phase | 기간 | 주요 작업 |
|-------|------|----------|
| Phase 1 | 1주 | 인프라 및 기본 설정 |
| Phase 2 | 1주 | 사용자 인증 시스템 |
| Phase 3 | 1주 | 게시판 기능 |
| Phase 4 | 1주 | 데이터 수집 시스템 |
| Phase 5 | 1주 | 사용자 행동 추적 |
| Phase 6 | 1주 | Railway 배포 및 최적화 |
| **총계** | **6주** | **전체 기능 완성** |

**빠른 배포 전략** (MVP):
- Phase 1 + Phase 2 + Phase 4 + Phase 6 = 4주
- 기본 기능만 구현하여 빠르게 배포
- 나머지 기능은 점진적으로 추가

---

## 🚀 다음 단계

1. **즉시 시작**: Phase 1부터 순차적으로 진행
2. **코드 리뷰**: 각 Phase 완료 후 코드 리뷰 및 테스트
3. **점진적 배포**: 각 Phase 완료 시 Railway에 배포하여 테스트
4. **사용자 피드백**: 배포 후 사용자 피드백 수집 및 반영

---

**작성자**: AI Assistant (프로 개발자 관점)  
**작성일**: 2025-01-XX  
**버전**: 1.0

