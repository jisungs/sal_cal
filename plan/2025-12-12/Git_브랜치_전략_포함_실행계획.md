# 🎨 급여명세서 디자인 선택 기능 추가 실행계획 (Git 브랜치 전략 포함)

**작성일**: 2025-12-12  
**버전**: 2.1 (Git 브랜치 전략 추가)  
**목표**: 사용자가 두 가지 급여명세서 디자인 중 선택하여 출력할 수 있는 기능 추가  
**원칙**: 기존 기능에 영향을 주지 않고 기능 업그레이드, Git 브랜치 전략을 통한 안전한 개발

---

## 📋 프로젝트 개요

### 목표
사용자가 제공된 두 가지 급여명세서 디자인 샘플(`급여명세서_sample.png`, `급여명세서_sample2.png`) 중 하나를 선택하여 급여명세서를 출력할 수 있도록 기능 추가

### 제약 사항
- ✅ **기존 기능 보존**: 현재 동작하는 모든 기능은 그대로 유지
- ✅ **하위 호환성**: 디자인 선택 없이도 기존 방식으로 동작 가능
- ✅ **점진적 개선**: 기존 코드를 최소한으로 수정하여 확장
- ✅ **안전한 개발**: Git 브랜치 전략을 통한 안전한 개발 및 배포

---

## 🌿 Git 브랜치 전략

### 브랜치 구조

```
master (메인 브랜치)
  │
  ├── develop (개발 브랜치)
  │     │
  │     └── feature/design-selection (기능 브랜치)
  │           │
  │           ├── feature/design-selection-phase-0 (준비 작업)
  │           ├── feature/design-selection-phase-1 (기본 구조)
  │           ├── feature/design-selection-phase-2 (디자인 1)
  │           ├── feature/design-selection-phase-3 (디자인 2)
  │           ├── feature/design-selection-phase-4 (통합)
  │           ├── feature/design-selection-phase-5 (웹 UI)
  │           ├── feature/design-selection-phase-6 (데스크톱 UI)
  │           └── feature/design-selection-phase-7 (테스트)
```

### 브랜치 명명 규칙

- **메인 브랜치**: `master` (프로덕션 준비 코드)
- **개발 브랜치**: `develop` (통합 개발 브랜치)
- **기능 브랜치**: `feature/design-selection` (메인 기능 브랜치)
- **단계별 브랜치**: `feature/design-selection-phase-{N}` (각 Phase별 작업)

---

## 🔄 Git 워크플로우

### 1. 초기 설정 (한 번만 실행)

```bash
# 현재 상태 확인
git status

# 변경사항 커밋 (필요시)
git add plan/2025-12-12/ sample/
git commit -m "docs: 디자인 선택 기능 실행계획 추가"

# develop 브랜치 생성 및 전환
git checkout -b develop
git push -u origin develop

# 메인 기능 브랜치 생성
git checkout -b feature/design-selection
git push -u origin feature/design-selection
```

### 2. Phase별 브랜치 전략

각 Phase는 독립적인 브랜치에서 작업하고, 완료 후 `feature/design-selection`에 병합합니다.

#### Phase 0: 준비 작업
```bash
# Phase 0 브랜치 생성
git checkout feature/design-selection
git checkout -b feature/design-selection-phase-0

# 작업 수행
# - 샘플 이미지 분석
# - 설정 파일 작성 (design_1.yaml, design_2.yaml)

# 커밋 및 푸시
git add payroll_generator/templates/designs/configs/
git commit -m "feat: Phase 0 - 디자인 설정 파일 작성"
git push -u origin feature/design-selection-phase-0

# feature/design-selection에 병합
git checkout feature/design-selection
git merge feature/design-selection-phase-0 --no-ff -m "merge: Phase 0 완료"
git push origin feature/design-selection

# Phase 브랜치 삭제 (선택사항)
git branch -d feature/design-selection-phase-0
git push origin --delete feature/design-selection-phase-0
```

#### Phase 1: 기본 구조 구축
```bash
# Phase 1 브랜치 생성
git checkout feature/design-selection
git checkout -b feature/design-selection-phase-1

# 작업 수행
# - 디렉토리 구조 생성
# - base_design.py 구현
# - design_factory.py 구현
# - PyYAML 의존성 추가

# 커밋 및 푸시
git add payroll_generator/templates/designs/
git add requirements.txt
git commit -m "feat: Phase 1 - 디자인 시스템 기본 구조 구축"
git push -u origin feature/design-selection-phase-1

# 테스트 실행
python -m pytest tests/test_design_system.py

# feature/design-selection에 병합
git checkout feature/design-selection
git merge feature/design-selection-phase-1 --no-ff -m "merge: Phase 1 완료"
git push origin feature/design-selection
```

#### Phase 2-7: 동일한 패턴 반복

각 Phase마다 동일한 패턴으로 진행:
1. 브랜치 생성
2. 작업 수행
3. 커밋 및 푸시
4. 테스트 실행
5. 병합

---

## 📝 커밋 메시지 규칙

### 커밋 타입
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅, 세미콜론 누락 등
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드 추가/수정
- `chore`: 빌드 업무 수정, 패키지 매니저 설정 등

### 커밋 메시지 형식
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 예시
```bash
# 기능 추가
git commit -m "feat(design): Phase 1 - BaseDesign 클래스 구현"

# 버그 수정
git commit -m "fix(design): 설정 파일 경로 찾기 오류 수정"

# 문서 수정
git commit -m "docs(plan): Git 브랜치 전략 추가"

# 테스트 추가
git commit -m "test(design): Design1 PDF 생성 테스트 추가"
```

---

## 🔀 병합 전략

### 1. Feature 브랜치 → Feature 메인 브랜치
- **방법**: `--no-ff` 옵션 사용 (병합 커밋 생성)
- **이유**: 각 Phase의 작업 이력을 명확히 보존

```bash
git checkout feature/design-selection
git merge feature/design-selection-phase-1 --no-ff -m "merge: Phase 1 완료"
```

### 2. Feature 브랜치 → Develop 브랜치
- **시점**: 모든 Phase 완료 후
- **방법**: Pull Request 생성 (권장) 또는 직접 병합

```bash
# Pull Request 생성 (GitHub/GitLab 등)
# 또는 직접 병합
git checkout develop
git merge feature/design-selection --no-ff -m "merge: 디자인 선택 기능 완료"
git push origin develop
```

### 3. Develop 브랜치 → Master 브랜치
- **시점**: 모든 테스트 통과 및 검증 완료 후
- **방법**: Pull Request 생성 및 코드 리뷰 후 병합

```bash
# Pull Request 생성
# 코드 리뷰 후 병합
git checkout master
git merge develop --no-ff -m "release: 디자인 선택 기능 v1.0"
git tag -a v1.0 -m "디자인 선택 기능 추가"
git push origin master --tags
```

---

## 🧪 테스트 전략

### 각 Phase별 테스트

#### Phase 1: 기본 구조 구축
```bash
# 단위 테스트
python -m pytest tests/test_base_design.py
python -m pytest tests/test_design_factory.py

# 통합 테스트
python -m pytest tests/test_design_system_integration.py
```

#### Phase 2-3: 디자인 구현
```bash
# 각 디자인별 테스트
python -m pytest tests/test_design_1.py
python -m pytest tests/test_design_2.py

# 출력 파일 검증
python -m pytest tests/test_design_output.py
```

#### Phase 4: 통합
```bash
# 기존 기능 호환성 테스트
python -m pytest tests/test_backward_compatibility.py

# 회귀 테스트
python -m pytest tests/test_regression.py
```

#### Phase 7: 전체 테스트
```bash
# 전체 테스트 스위트 실행
python -m pytest tests/

# 커버리지 확인
python -m pytest tests/ --cov=payroll_generator --cov-report=html
```

---

## 🚨 롤백 전략

### 1. Phase별 롤백
각 Phase에서 문제 발생 시 해당 브랜치만 롤백:

```bash
# 병합 취소
git checkout feature/design-selection
git revert <merge-commit-hash>

# 또는 브랜치 삭제 후 재작업
git branch -D feature/design-selection-phase-X
```

### 2. Feature 브랜치 롤백
전체 기능에 문제 발생 시:

```bash
# develop 브랜치에서 병합 취소
git checkout develop
git revert <merge-commit-hash>
git push origin develop
```

### 3. Master 브랜치 롤백
프로덕션 배포 후 문제 발생 시:

```bash
# 태그를 사용한 롤백
git checkout master
git revert <release-commit-hash>
git push origin master

# 또는 이전 태그로 롤백
git checkout v0.9  # 이전 버전
git checkout -b hotfix/critical-fix
# 수정 후 병합
```

---

## 📊 전체 개발 흐름

### 단계별 워크플로우

```
1. [master] 현재 상태 확인 및 커밋
   ↓
2. [develop] develop 브랜치 생성
   ↓
3. [feature/design-selection] 메인 기능 브랜치 생성
   ↓
4. [feature/design-selection-phase-0] Phase 0 작업
   ├─ 작업 수행
   ├─ 커밋
   └─ feature/design-selection에 병합
   ↓
5. [feature/design-selection-phase-1] Phase 1 작업
   ├─ 작업 수행
   ├─ 테스트
   ├─ 커밋
   └─ feature/design-selection에 병합
   ↓
6. [Phase 2-7 반복] 동일한 패턴
   ↓
7. [develop] feature/design-selection 병합
   ├─ 통합 테스트
   └─ 코드 리뷰
   ↓
8. [master] develop 병합
   ├─ 최종 테스트
   ├─ 태그 생성
   └─ 배포
```

---

## 🔧 Git 명령어 체크리스트

### 초기 설정
- [ ] 현재 변경사항 커밋
- [ ] develop 브랜치 생성 및 전환
- [ ] feature/design-selection 브랜치 생성

### 각 Phase별 작업
- [ ] Phase 브랜치 생성
- [ ] 작업 수행
- [ ] 커밋 (명확한 메시지)
- [ ] 푸시
- [ ] 테스트 실행
- [ ] feature/design-selection에 병합
- [ ] Phase 브랜치 삭제 (선택사항)

### 최종 병합
- [ ] develop 브랜치에 병합
- [ ] 통합 테스트 실행
- [ ] 코드 리뷰
- [ ] master 브랜치에 병합
- [ ] 태그 생성 및 배포

---

## 📋 Phase별 Git 작업 상세

### Phase 0: 준비 작업

```bash
# 브랜치 생성
git checkout feature/design-selection
git checkout -b feature/design-selection-phase-0

# 작업 수행
# 1. 샘플 이미지 분석
# 2. design_1.yaml 작성
# 3. design_2.yaml 작성

# 커밋
git add payroll_generator/templates/designs/configs/design_1.yaml
git add payroll_generator/templates/designs/configs/design_2.yaml
git commit -m "feat(design): Phase 0 - 디자인 설정 파일 작성

- 급여명세서_sample.png 분석 결과를 design_1.yaml로 작성
- 급여명세서_sample2.png 분석 결과를 design_2.yaml로 작성
- 레이아웃, 색상, 폰트 스펙 정의"

# 푸시
git push -u origin feature/design-selection-phase-0

# 병합
git checkout feature/design-selection
git merge feature/design-selection-phase-0 --no-ff -m "merge: Phase 0 완료 - 설정 파일 작성"
git push origin feature/design-selection
```

### Phase 1: 기본 구조 구축

```bash
# 브랜치 생성
git checkout feature/design-selection
git checkout -b feature/design-selection-phase-1

# 작업 수행
# 1. 디렉토리 구조 생성
mkdir -p payroll_generator/templates/designs/configs
touch payroll_generator/templates/designs/__init__.py

# 2. base_design.py 구현
# 3. design_factory.py 구현
# 4. requirements.txt에 PyYAML 추가

# 커밋
git add payroll_generator/templates/designs/
git add requirements.txt
git commit -m "feat(design): Phase 1 - 디자인 시스템 기본 구조 구축

- BaseDesign 추상 클래스 구현
- DesignFactory 클래스 구현
- 설정 파일 로드 기능 구현
- PyYAML 의존성 추가"

# 테스트 (테스트 파일이 있다면)
python -m pytest tests/test_base_design.py -v

# 푸시 및 병합
git push -u origin feature/design-selection-phase-1
git checkout feature/design-selection
git merge feature/design-selection-phase-1 --no-ff -m "merge: Phase 1 완료 - 기본 구조 구축"
git push origin feature/design-selection
```

### Phase 2: 디자인 1 구현

```bash
# 브랜치 생성
git checkout feature/design-selection
git checkout -b feature/design-selection-phase-2

# 작업 수행
# 1. design_1.py 구현
# 2. PDF 생성 메서드 구현
# 3. 엑셀 생성 메서드 구현
# 4. 테스트 작성

# 커밋
git add payroll_generator/templates/designs/design_1.py
git add tests/test_design_1.py
git commit -m "feat(design): Phase 2 - 디자인 1 구현 완료

- Design1 클래스 구현
- PDF 생성 메서드 구현 (reportlab 기반)
- 엑셀 생성 메서드 구현 (openpyxl 기반)
- 단위 테스트 작성"

# 테스트
python -m pytest tests/test_design_1.py -v

# 푸시 및 병합
git push -u origin feature/design-selection-phase-2
git checkout feature/design-selection
git merge feature/design-selection-phase-2 --no-ff -m "merge: Phase 2 완료 - 디자인 1 구현"
git push origin feature/design-selection
```

### Phase 3-7: 동일한 패턴

각 Phase마다 동일한 패턴으로 진행합니다.

---

## 🎯 병합 전 체크리스트

### 각 Phase 병합 전
- [ ] 코드 작성 완료
- [ ] 단위 테스트 통과
- [ ] 코드 스타일 확인 (PEP 8)
- [ ] 커밋 메시지 명확히 작성
- [ ] 불필요한 주석/디버그 코드 제거

### Develop 병합 전
- [ ] 모든 Phase 완료
- [ ] 통합 테스트 통과
- [ ] 기존 기능 회귀 테스트 통과
- [ ] 문서 업데이트 완료
- [ ] 코드 리뷰 완료 (필요시)

### Master 병합 전
- [ ] Develop 브랜치에서 모든 테스트 통과
- [ ] 프로덕션 환경 테스트 완료
- [ ] 버전 태그 준비
- [ ] 릴리스 노트 작성
- [ ] 배포 계획 수립

---

## 📚 Git 브랜치 전략 요약

### 핵심 원칙
1. **안전한 개발**: 각 Phase를 독립 브랜치에서 작업
2. **명확한 이력**: 병합 커밋으로 작업 단위 명확히 구분
3. **롤백 용이**: 각 단계별로 롤백 가능
4. **협업 친화적**: Pull Request를 통한 코드 리뷰 가능

### 브랜치 전략 선택 이유
- **Feature Branch 전략**: 기능별로 독립적인 개발 가능
- **Phase별 브랜치**: 각 단계별로 명확한 작업 단위 구분
- **병합 커밋 보존**: `--no-ff` 옵션으로 작업 이력 보존

---

## 🚀 빠른 시작 가이드

### 1. 초기 설정 (한 번만)
```bash
# 현재 상태 확인 및 커밋
git status
git add plan/2025-12-12/ sample/
git commit -m "docs: 디자인 선택 기능 실행계획 추가"

# develop 브랜치 생성
git checkout -b develop
git push -u origin develop

# 기능 브랜치 생성
git checkout -b feature/design-selection
git push -u origin feature/design-selection
```

### 2. Phase 0 시작
```bash
git checkout feature/design-selection
git checkout -b feature/design-selection-phase-0

# 작업 수행 후
git add .
git commit -m "feat(design): Phase 0 - 설정 파일 작성"
git push -u origin feature/design-selection-phase-0

# 병합
git checkout feature/design-selection
git merge feature/design-selection-phase-0 --no-ff -m "merge: Phase 0 완료"
git push origin feature/design-selection
```

### 3. 이후 Phase들도 동일한 패턴으로 진행

---

## 📝 참고사항

### .gitignore 확인
다음 파일들은 커밋하지 않도록 확인:
- `app.db` (데이터베이스 파일)
- `__pycache__/` (Python 캐시)
- `*.pyc` (컴파일된 Python 파일)
- `.env` (환경 변수 파일)
- `outputs/` (생성된 출력 파일)

### 충돌 해결
병합 시 충돌 발생 시:
1. 충돌 파일 확인: `git status`
2. 충돌 해결: 파일 편집
3. 해결 확인: `git add <file>`
4. 병합 완료: `git commit`

---

**작성자**: AI Assistant  
**작성일**: 2025-12-12  
**버전**: 2.1 (Git 브랜치 전략 포함)  
**상태**: ✅ Git 브랜치 전략 포함 실행계획 작성 완료
