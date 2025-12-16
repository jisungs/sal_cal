# 🚀 급여명세서 자동생성기 웹 버전 MVP - 1주일 실행 계획 (실무 개선안)

**목표 일자**: 7일 (1주일)  
**목표**: MVP 완성 + 유튜브 영상 제작  
**핵심 원칙**: 기존 코드 최대한 재사용, 최소 기능만 구현, 영상 제작 통합

> ⚠️ **중요**: 이 계획은 실무 개발자 관점에서 검토 및 개선되었습니다.  
> 현재 `app.py`가 이미 구현되어 있어 개발 시간이 단축됩니다.

---

## 📋 MVP 범위 정의

### ✅ 포함할 기능 (Must Have)
- ✅ 엑셀 파일 업로드
- ✅ 급여명세서 자동 계산 (기존 calculator.py 재사용)
- ✅ **엑셀 템플릿 기반 급여명세서 생성** (템플릿 파일 활용)
- ✅ PDF/엑셀 다운로드 (기존 pdf_generator.py, excel_handler.py 재사용)
- ✅ 간단한 웹 UI (파일 업로드, 결과 다운로드)
- ✅ 로컬 실행 가능 (Flask 개발 서버)

### ❌ 제외할 기능 (v2.0에서)
- ❌ 사용자 인증/회원가입
- ❌ 데이터베이스 저장
- ❌ 대시보드 (웹 버전은 v2.0)
- ❌ 결제 시스템
- ❌ 클라우드 배포 (로컬 실행만)

---

## 📅 일자별 상세 실행 계획

### 🔥 Day 1 (월) - 현재 상태 점검 및 MVP 범위 확정

**목표**: 현재 코드 상태 확인 및 MVP 범위 최종 확정

#### 오전 (2시간)
- [ ] **현재 코드 상태 점검**
  - `app.py` 동작 확인 (이미 구현됨)
  - 기존 모듈 통합 상태 확인
  - 템플릿 파일 경로 확인
  - 버그 및 누락 기능 파악

- [ ] **MVP 범위 최종 확정**
  - Must Have 기능 리스트 작성
  - Should Have 기능 리스트 작성
  - 우선순위 명확화

#### 오후 (2시간)
- [ ] **유튜브 영상 제작 계획 수립**
  - 영상 시나리오 작성
  - 체크포인트 설정 (영상 촬영 시점)
  - 데모 시나리오 작성

- [ ] **개발 환경 최종 확인**
  - 가상환경 설정 확인
  - 의존성 설치 확인
  - Git 저장소 정리

**Day 1 완료 기준:**
- [x] 현재 코드 상태 파악 완료
- [x] MVP 범위 확정 완료
- [x] 유튜브 영상 계획 수립 완료
  ```
  salary_cal_web/
  ├── app.py                 # Flask 메인 애플리케이션
  ├── requirements.txt       # 웹 버전 의존성
  ├── config.py             # 웹 설정
  ├── payroll_generator/     # 기존 모듈 (그대로 사용)
  │   ├── calculator.py
  │   ├── excel_handler.py
  │   ├── pdf_generator.py
  │   └── ...
  ├── web/
  │   ├── templates/         # HTML 템플릿
  │   │   ├── index.html
  │   │   └── result.html
  │   ├── static/            # CSS, JS
  │   │   ├── css/
  │   │   │   └── style.css
  │   │   └── js/
  │   │       └── main.js
  │   └── uploads/           # 업로드된 파일 임시 저장
  └── outputs/               # 생성된 파일 저장
  ```

- [ ] **Flask 프로젝트 초기화**
  ```bash
  # 새 디렉토리 생성 (선택사항: 기존 프로젝트에 추가)
  mkdir salary_cal_web
  cd salary_cal_web
  
  # 가상환경 생성
  python3 -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  
  # Flask 설치
  pip install flask flask-cors werkzeug
  ```

- [ ] **기존 모듈 복사/연결**
  - `payroll_generator/` 폴더를 새 프로젝트로 복사 또는 심볼릭 링크
  - 기존 모듈 import 테스트

- [ ] **엑셀 템플릿 파일 확인**
  - `payroll_generator/templates/payroll_template.xlsx` 템플릿 파일 확인
  - 템플릿 파일이 웹 프로젝트에 포함되는지 확인
  - 템플릿 파일 경로 설정 확인

#### 오후 (2-3시간)
- [ ] **기본 Flask 앱 구조 작성**
  - `app.py` 기본 구조 생성
  - 라우트 정의 (/, /upload, /download)
  - 파일 업로드 핸들러 기본 구조

- [ ] **HTML 템플릿 기본 구조**
  - `templates/index.html` 생성 (파일 업로드 폼)
  - Bootstrap 또는 Tailwind CSS CDN 연결
  - 기본 레이아웃 작성

**Day 1 완료 체크리스트:**
- [ ] Flask 프로젝트 구조 생성 완료
- [ ] 기본 Flask 앱 실행 가능
- [ ] HTML 템플릿 기본 구조 완성
- [ ] 기존 모듈 import 테스트 통과
- [ ] 엑셀 템플릿 파일 확인 완료

---

### 🔥 Day 2 (화) - 핵심 기능 완성 및 버그 수정

**목표**: 핵심 기능 완성 및 작동 확인 (이미 구현된 기능 점검)

#### 오전 (3-4시간)
- [ ] **파일 업로드 기능 점검 및 수정**
  ```python
  # app.py
  @app.route('/upload', methods=['POST'])
  def upload_file():
      # 1. 파일 검증 (엑셀 파일인지 확인)
      # 2. 파일 저장 (web/uploads/)
      # 3. 엑셀 읽기 (기존 excel_handler.py 사용)
      # 4. 급여 계산 (기존 calculator.py 사용)
      # 5. 결과 반환 (JSON 또는 세션 저장)
  ```

- [ ] **기존 모듈 통합**
  - `ExcelHandler.read_employee_data()` 호출
  - `PayrollCalculator.calculate_deductions()` 호출
  - **템플릿 기반 급여명세서 생성**
    - `ExcelHandler.write_payroll(use_template=True)` 사용
    - `PDFGenerator.generate_payslip(use_template=True)` 사용
  - 에러 처리 추가

#### 오후 (3-4시간)
- [ ] **결과 페이지 구현**
  - `templates/result.html` 생성
  - 계산 결과 표시 (직원별 급여 정보)
  - PDF/엑셀 다운로드 버튼 추가

- [ ] **파일 다운로드 API 구현**
  ```python
  @app.route('/download/<format>/<filename>')
  def download_file(format, filename):
      # format: 'pdf' or 'excel'
      # 템플릿 기반 생성 사용
      # excel_handler.write_payroll(use_template=True)
      # pdf_generator.generate_payslip(use_template=True)
      # 생성된 파일 다운로드 제공
  ```

**Day 2 완료 체크리스트:**
- [ ] 파일 업로드 기능 작동 확인
- [ ] 급여 계산 결과 표시 확인
- [ ] **템플릿 기반 엑셀 생성 작동 확인**
- [ ] **템플릿 기반 PDF 생성 작동 확인**
- [ ] PDF 다운로드 기능 작동 확인
- [ ] 엑셀 다운로드 기능 작동 확인

---

### 🔥 Day 3 (수) - 일괄 처리 및 UI 개선

**목표**: 일괄 처리 기능 완성 및 UI 개선 (최소한)

#### 오전 (3시간)
- [ ] **일괄 처리 기능 확인/수정**
  - 여러 직원 일괄 생성 확인 (이미 구현됨)
  - ZIP 파일 다운로드 확인
  - 진행 상태 표시 (간단한 로딩)

#### 오후 (3시간)
- [ ] **UI 개선 (최소한)**
  - Bootstrap 기본 스타일 적용
  - 버튼 스타일링
  - 레이아웃 정리
  - **영상 촬영 준비 완료 상태**

**Day 3 완료 체크리스트:**
- [x] 일괄 처리 기능 작동 확인
- [x] 기본 UI 완성
- [x] 영상 촬영 가능 상태

---

### 🔥 Day 4 (목) - 유튜브 영상 제작 (체크포인트 1)

**목표**: MVP 데모 영상 제작

#### 오전 (2시간)
- [ ] **데모 시나리오 준비**
  - 샘플 엑셀 파일 준비
  - 데모 스크립트 작성
  - 화면 녹화 설정

#### 오후 (3-4시간)
- [ ] **영상 촬영**
  - 기능 데모 영상 (2-3분)
  - 사용법 설명 영상 (5-7분)
  - 타임랩스 개발 영상 (선택사항)

**Day 4 완료 체크리스트:**
- [x] 데모 영상 촬영 완료
- [x] 영상 편집 준비 완료

---

### 🔥 Day 5 (금) - 버그 수정 및 최종 점검

**목표**: 버그 수정 및 최종 점검

#### 오전 (2-3시간)
- [ ] **전체 기능 테스트**
  - 다양한 엑셀 파일 테스트
  - 에러 케이스 테스트
  - 성능 테스트 (10명 이하 직원 기준)

#### 오후 (2-3시간)
- [ ] **버그 수정**
  - 발견된 버그 수정
  - 코드 정리
  - README 작성

**Day 5 완료 체크리스트:**
- [x] 모든 기능 테스트 통과
- [x] 버그 수정 완료
- [x] MVP 완성

---

### 🔥 Day 6 (토) - 유튜브 영상 편집 및 업로드

**목표**: 영상 편집 및 업로드

#### 오전 (2-3시간)
- [ ] **영상 편집**
  - 데모 영상 편집
  - 자막 추가
  - 썸네일 제작

#### 오후 (2-3시간)
- [ ] **영상 업로드 및 홍보**
  - 유튜브 업로드
  - 제목/설명 최적화
  - 소셜미디어 홍보

**Day 6 완료 체크리스트:**
- [x] 영상 업로드 완료
- [x] 홍보 시작

---

### 🔥 Day 7 (일) - 추가 개선 및 다음 단계 준비

**목표**: 추가 개선 및 다음 단계 준비

#### 오전 (2시간)
- [ ] **피드백 수집**
  - 영상 댓글 확인
  - 사용자 피드백 수집
  - 개선 사항 정리

#### 오후 (2시간)
- [ ] **다음 단계 계획**
  - v2.0 기능 계획
  - 마케팅 전략 수립
  - 판매 전략 수립

**Day 7 완료 체크리스트:**
- [x] 피드백 수집 완료
- [x] 다음 단계 계획 수립

---

## 🛠️ 기술 스택

### 백엔드
- **Flask**: 웹 프레임워크 (가볍고 빠른 개발)
- **기존 모듈 재사용**: calculator.py, excel_handler.py, pdf_generator.py
- **엑셀 템플릿 기반 생성**: payroll_template.xlsx 템플릿 파일 활용

### 프론트엔드
- **HTML5/CSS3**: 기본 구조
- **Bootstrap 5** 또는 **Tailwind CSS**: 빠른 스타일링
- **Vanilla JavaScript**: 간단한 인터랙션

### 파일 처리
- **pandas**: 엑셀 읽기/쓰기
- **openpyxl**: 엑셀 생성
- **reportlab**: PDF 생성

---

## 📁 프로젝트 구조 (최종)

```
salary_cal_web/
├── app.py                      # Flask 메인 애플리케이션
├── config.py                   # 설정 파일
├── requirements.txt            # 의존성 목록
├── .env.example                # 환경 변수 예시
├── run.sh                      # 실행 스크립트 (Linux/Mac)
├── run.bat                     # 실행 스크립트 (Windows)
├── README.md                   # 사용 가이드
│
├── payroll_generator/          # 기존 모듈 (재사용)
│   ├── __init__.py
│   ├── calculator.py
│   ├── excel_handler.py       # 템플릿 기반 생성 지원
│   ├── pdf_generator.py        # 템플릿 기반 생성 지원
│   ├── config.py
│   ├── utils.py
│   ├── templates/              # 엑셀 템플릿 파일
│   │   ├── payroll_template.xlsx  # 급여명세서 템플릿
│   │   ├── employee_template.xlsx
│   │   └── company_template.xlsx
│   └── ...
│
├── web/
│   ├── templates/              # HTML 템플릿
│   │   ├── base.html
│   │   ├── index.html
│   │   └── result.html
│   │
│   ├── static/                 # 정적 파일
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   │
│   └── uploads/                # 업로드된 파일 (임시)
│
└── outputs/                    # 생성된 파일
    ├── pdf/
    └── excel/
```

---

## 🎯 핵심 API 엔드포인트

### 1. 메인 페이지
```
GET /
```
- 파일 업로드 폼 표시

### 2. 파일 업로드 및 처리
```
POST /upload
```
- 엑셀 파일 업로드
- 급여 계산 수행
- 결과 페이지로 리다이렉트

### 3. 결과 페이지
```
GET /result/<session_id>
```
- 계산 결과 표시
- 다운로드 버튼 제공

### 4. 파일 다운로드
```
GET /download/<format>/<employee_name>
```
- format: 'pdf' or 'excel'
- **템플릿 기반으로 생성된 파일 다운로드**
- 엑셀: `excel_handler.write_payroll(use_template=True)`
- PDF: `pdf_generator.generate_payslip(use_template=True)`

### 5. 일괄 다운로드
```
GET /batch_download/<format>
```
- 모든 직원의 파일을 **템플릿 기반으로 생성**
- ZIP 파일로 압축하여 다운로드

---

## ✅ 일일 체크리스트 템플릿

각 날짜마다 다음을 확인하세요:

**아침 체크리스트:**
- [ ] 어제 작업 내용 확인
- [ ] 오늘 목표 설정
- [ ] 필요한 리소스 준비

**저녁 체크리스트:**
- [ ] 오늘 완료한 작업 체크
- [ ] 내일 계획 수립
- [ ] 코드 커밋 (Git)

---

## 🚨 리스크 관리 (강화)

### 리스크 1: 개발 시간 부족
**확률**: 높음  
**영향**: 높음  
**대응:**
- MVP 범위 최소화 (Must Have만)
- Should Have는 선택사항으로 처리
- 버그는 치명적인 것만 수정
- **현재 `app.py`가 이미 구현되어 있어 시간 단축 가능**

### 리스크 2: 영상 제작 시간 부족
**확률**: 중간  
**영향**: 중간  
**대응:**
- 영상 촬영은 Day 4에 집중
- 편집은 간단하게 (자막만 추가)
- 고급 편집은 나중에

### 리스크 3: 기존 코드 통합 문제
**확률**: 낮음 (이미 구현됨)  
**영향**: 높음  
**대응:**
- Day 1에 충분한 테스트
- 문제 발견 시 즉시 수정

### 리스크 4: 성능 문제
**확률**: 낮음  
**영향**: 낮음  
**대응:**
- 10명 이하 직원 기준으로 테스트
- 대용량 처리는 v2.0에서

---

## 📊 진행 상황 추적

### Day 1 진행률: [ ] 0%
- [ ] 프로젝트 구조 생성
- [ ] Flask 환경 설정
- [ ] 기본 앱 구조 작성

### Day 2 진행률: [ ] 0%
- [ ] 파일 업로드 구현
- [ ] 급여 계산 통합
- [ ] 다운로드 기능 구현

### Day 3 진행률: [ ] 0%
- [ ] UI 개선
- [ ] 일괄 처리 기능
- [ ] 에러 처리 강화

### Day 4 진행률: [ ] 0%
- [ ] 전체 테스트
- [ ] 버그 수정
- [ ] 문서 작성

### Day 5 진행률: [ ] 0%
- [ ] 추가 기능
- [ ] 최종 점검
- [ ] 배포 준비

---

## 🎉 완료 기준

다음주 월요일까지 다음이 완료되면 MVP 성공:

- [x] 엑셀 파일 업로드 가능
- [x] 급여명세서 자동 계산 작동
- [x] **엑셀 템플릿 기반 급여명세서 생성 작동**
- [x] **템플릿 기반 PDF 생성 작동**
- [x] PDF 다운로드 가능
- [x] 엑셀 다운로드 가능
- [x] 일괄 처리 가능 (템플릿 기반)
- [x] 기본 UI 완성
- [x] 로컬에서 실행 가능
- [x] README 작성 완료

---

## 📝 참고 사항

### 기존 코드 재사용 전략
1. **calculator.py**: 그대로 사용 (수정 불필요)
2. **excel_handler.py**: 템플릿 기반 생성 지원 (use_template=True 옵션 사용)
   - `write_payroll(use_template=True)`: 템플릿 파일 기반 생성
   - `write_payroll(use_template=False)`: 코드 기반 생성 (폴백)
3. **pdf_generator.py**: 템플릿 기반 생성 지원 (use_template=True 옵션 사용)
   - `generate_payslip(use_template=True)`: 템플릿 파일 기반 생성
   - `generate_payslip(use_template=False)`: 코드 기반 생성 (폴백)
4. **config.py**: 그대로 사용 (수정 불필요)
5. **utils.py**: 그대로 사용 (수정 불필요)
6. **템플릿 파일**: `payroll_generator/templates/payroll_template.xlsx` 사용

### 개발 팁
- 기존 코드를 최대한 재사용하여 개발 시간 단축
- **엑셀 템플릿 기반 생성 사용**: 양식 변경 시 템플릿 파일만 수정하면 됨
- Flask는 가볍고 빠르게 개발 가능
- HTML/CSS는 Bootstrap CDN 활용하여 빠르게 스타일링
- JavaScript는 최소한만 사용 (Vanilla JS)

### 템플릿 기반 생성의 장점
- ✅ 양식 변경이 쉬움: 엑셀 파일만 수정하면 됨
- ✅ 코드 수정 최소화: 양식 변경 시 코드 수정 불필요
- ✅ 하위 호환성: 템플릿이 없으면 코드 기반 생성으로 자동 폴백
- ✅ 유연성: 템플릿 사용 여부를 선택 가능

### 엑셀 템플릿 구조

템플릿 파일: `payroll_generator/templates/payroll_template.xlsx`

**템플릿 셀 위치 매핑:**
- A2: 지급기간 (`{PERIOD}`)
- B4: 성명 (`{EMPLOYEE_NAME}`)
- B5: 주민번호 (`{RESIDENT_NUMBER}`) - 자동 마스킹 처리
- B6: 입사일 (`{JOIN_DATE}`)
- B9-B12: 지급 항목 (기본급, 연장근무수당, 상여금, 총 지급액)
- B15-B21: 공제 항목 (국민연금, 건강보험, 장기요양, 고용보험, 소득세, 지방소득세, 총 공제액)
- A23: 실수령액 (`{NET_PAY}`)

**템플릿 커스터마이징:**
- 엑셀 파일을 직접 수정하여 양식 변경 가능
- 색상, 폰트, 레이아웃 자유롭게 변경 가능
- 코드 수정 없이 양식 업데이트 가능

### 다음 단계 (v2.0)
- 사용자 인증 시스템
- 데이터베이스 연동
- 대시보드 기능
- 클라우드 배포
- 결제 시스템 연동
- **템플릿 관리 기능**: 웹에서 템플릿 업로드/수정 기능

---

**작성일**: 2025-01-XX  
**목표 완료일**: 7일 (1주일)  
**작성자**: 개발팀  
**검토일**: 2025-01-XX (프로 개발자 관점 실무 검토)

---

## 🔄 업데이트 로그

- **2025-01-XX**: 초안 작성
- **2025-01-XX**: 엑셀 템플릿 기반 생성 방식으로 계획 수정
- **2025-01-XX**: 실무 검토 및 개선
  - 현재 코드 상태 반영 (`app.py` 이미 구현됨)
  - 유튜브 영상 제작 프로세스 통합
  - 일정 현실화 및 우선순위 명확화
  - 리스크 관리 강화
  - 영상 제작 체크포인트 추가

---

## 📚 관련 문서

- [실무 검토 개선안](./MVP_실무검토_개선안.md) - 상세한 실무 검토 내용
- [600만원 플랜](./600만원_플랜.md) - 수익 모델 및 전략

