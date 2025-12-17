# Railway 배포 문제 해결 가이드

**문제**: Railway에서 재배포를 했지만 여전히 이전 버전의 코드(`index.html`)가 실행되고 있습니다.

**원인**: Railway가 최신 커밋을 배포하지 않거나, 빌드 캐시 문제일 수 있습니다.

---

## 🔍 문제 확인

Railway SSH에서 확인한 결과:
- 배포된 코드: `return render_template('index.html')` (이전 버전)
- 로컬 코드: `return render_template('pages/main.html')` (최신 버전)
- 최신 커밋: `726c157`

---

## ✅ 해결 방법

### 방법 1: Railway 설정에서 브랜치 확인 및 재배포

1. **Railway 대시보드 접속**
   - https://railway.app 접속
   - 프로젝트 선택

2. **Settings 탭 확인**
   - 좌측 메뉴에서 **"Settings"** 클릭
   - **"Source"** 섹션 확인
   - **Branch**가 `main`으로 설정되어 있는지 확인
   - **Repository**가 올바른 저장소를 가리키는지 확인

3. **빌드 캐시 클리어**
   - **"Settings"** → **"Deploy"** 탭
   - **"Clear Build Cache"** 버튼 클릭
   - 확인 대화상자에서 **"Clear"** 클릭

4. **수동 재배포**
   - **"Deployments"** 탭으로 이동
   - **"Deploy"** 버튼 클릭
   - 또는 최신 배포에서 **"Redeploy"** 클릭

### 방법 2: Railway CLI 사용

```bash
# Railway CLI 설치 (없는 경우)
npm i -g @railway/cli

# Railway 로그인
railway login

# 프로젝트 선택
railway link

# 재배포 (빌드 캐시 클리어는 Railway 대시보드에서만 가능)
railway up
```

### 방법 3: Railway에서 특정 커밋 강제 배포

1. **Railway 대시보드 접속**
   - 프로젝트 선택

2. **Settings → Source**
   - **"Deploy from GitHub"** 확인
   - **"Branch"**가 `main`인지 확인
   - 필요시 `main` 브랜치로 변경

3. **Deployments 탭**
   - **"Deploy"** 버튼 클릭
   - 최신 커밋(`726c157`)이 배포되는지 확인

---

## 🔧 추가 확인 사항

### 1. Git 저장소 확인

로컬에서 다음 명령어로 확인:

```bash
# 최신 커밋 확인
git log --oneline -3

# 원격 저장소와 동기화 확인
git fetch origin
git status

# 필요시 원격 저장소에 푸시
git push origin main
```

### 2. Railway 빌드 로그 확인

Railway 대시보드 → 프로젝트 → "Deployments" → 최신 배포 → "View Logs"

다음 내용을 확인:
- 빌드가 성공적으로 완료되었는지
- 어떤 커밋 해시가 배포되었는지
- 에러 메시지가 있는지

### 3. Railway SSH에서 코드 확인

재배포 후 Railway SSH에서 확인:

```bash
# 코드 확인
cat app/routes/main.py | grep -A 15 "@main_bp.route('/')"

# Git 커밋 확인
cd /app && git log --oneline -1
```

다음과 같이 표시되어야 함:
```python
@main_bp.route('/')
def index():
    """메인 페이지 - Main.html 렌더링"""
    ...
    activity_data={'page': 'main'}  # 'index'가 아닌 'main'
    ...
    logger.info("루트 경로(/) 접근: pages/main.html 렌더링")
    return render_template('pages/main.html')  # pages/main.html
```

---

## 🐛 문제 해결

### 문제 1: 재배포 후에도 이전 버전이 실행됨

**원인**: Railway 빌드 캐시 문제

**해결 방법**:
1. Railway 대시보드 → 프로젝트 → "Settings" → "Deploy" 탭
2. **"Clear Build Cache"** 클릭
3. 다시 재배포

### 문제 2: Railway가 다른 브랜치를 배포함

**원인**: Railway 설정에서 잘못된 브랜치 지정

**해결 방법**:
1. Railway 대시보드 → 프로젝트 → "Settings" → "Source"
2. **"Branch"**를 `main`으로 설정
3. 재배포

### 문제 3: Git 저장소와 동기화되지 않음

**원인**: 로컬 변경사항이 원격 저장소에 푸시되지 않음

**해결 방법**:
```bash
# 로컬 변경사항 확인
git status

# 원격 저장소에 푸시
git push origin main

# Railway에서 재배포
```

---

## 📝 참고사항

- 최신 커밋 해시: `726c157`
- 변경된 파일: `app/routes/main.py`
- 변경 내용: 루트 경로가 `pages/main.html`을 렌더링하도록 수정
- 로컬 브랜치: `main`
- 원격 브랜치: `origin/main`

---

## 🚀 빠른 해결 방법

1. **Railway 대시보드 접속**
2. **Settings → Deploy → "Clear Build Cache"** 클릭
3. **Deployments → "Deploy"** 클릭
4. 배포 완료 대기 (2-5분)
5. 웹사이트 테스트

---

**다음 단계**: Railway에서 빌드 캐시를 클리어하고 재배포한 후 웹사이트를 테스트하세요.

