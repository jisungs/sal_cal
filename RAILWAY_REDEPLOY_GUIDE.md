# Railway 재배포 가이드

**문제**: Railway에 배포된 코드가 이전 버전으로, 루트 경로가 `index.html`을 렌더링하고 있습니다.

**해결**: Railway에서 최신 커밋을 수동으로 재배포해야 합니다.

---

## 🔄 Railway 수동 재배포 방법

### 방법 1: Railway 대시보드에서 재배포

1. **Railway 대시보드 접속**
   - https://railway.app 접속
   - 프로젝트 선택

2. **Deployments 탭 확인**
   - 좌측 메뉴에서 **"Deployments"** 클릭
   - 최신 배포 확인 (커밋 해시: `726c157`)

3. **재배포 실행**
   - 최신 배포 항목에서 **"Redeploy"** 버튼 클릭
   - 또는 **"Deploy"** 버튼 클릭하여 최신 커밋 강제 배포

4. **배포 완료 대기**
   - 배포 상태가 "Success"가 될 때까지 대기
   - 일반적으로 2-5분 소요

### 방법 2: Railway CLI 사용

```bash
# Railway CLI 설치 (없는 경우)
npm i -g @railway/cli

# Railway 로그인
railway login

# 프로젝트 선택
railway link

# 최신 커밋 강제 배포
railway up
```

**참고**: Railway CLI에서는 빌드 캐시를 직접 클리어할 수 없습니다. 빌드 캐시를 클리어하려면 Railway 대시보드에서 "Clear Build Cache" 버튼을 사용하세요.

---

## ✅ 배포 확인 방법

### 1. Railway 로그 확인

Railway 대시보드 → 프로젝트 → "Deployments" → 최신 배포 → "View Logs"

다음 로그가 보이면 성공:
```
루트 경로(/) 접근: pages/main.html 렌더링
```

### 2. Railway SSH에서 코드 확인

```bash
# Railway SSH 접속 후
cat app/routes/main.py | grep -A 15 "@main_bp.route('/')"
```

다음과 같이 표시되어야 함:
```python
@main_bp.route('/')
def index():
    """메인 페이지 - Main.html 렌더링"""
    ...
    activity_data={'page': 'main'}  # 'index'가 아닌 'main'
    ...
    return render_template('pages/main.html')  # pages/main.html
```

### 3. 웹사이트 테스트

- 웹사이트 루트 경로(`/`) 접속
- `pages/main.html`이 표시되는지 확인
- 엑셀 입력 페이지(`index.html`)가 아닌 Main 페이지가 표시되어야 함

---

## 🐛 문제 해결

### 문제 1: 재배포 후에도 이전 버전이 실행됨

**원인**: Railway가 이전 커밋을 캐시하고 있을 수 있음

**해결 방법**:
1. Railway 대시보드 → 프로젝트 → "Settings" → "Deploy" 탭
2. "Clear Build Cache" 클릭
3. 다시 재배포

### 문제 2: 배포가 실패함

**확인 사항**:
1. Railway 빌드 로그 확인
2. 에러 메시지 확인
3. 필요한 경우 `.gitignore` 확인 (필수 파일이 제외되지 않았는지)

---

## 📝 참고사항

- 최신 커밋 해시: `726c157`
- 변경된 파일: `app/routes/main.py`
- 변경 내용: 루트 경로가 `pages/main.html`을 렌더링하도록 수정

---

**다음 단계**: Railway에서 재배포를 완료한 후 웹사이트를 테스트하세요.

