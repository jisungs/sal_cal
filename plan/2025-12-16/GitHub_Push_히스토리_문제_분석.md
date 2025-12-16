# GitHub Push 히스토리 문제 분석 및 해결

**작성일**: 2025-12-16  
**에러**: `File payroll_generator/assets/nanum-all_new.zip is 125.32 MB; this exceeds GitHub's file size limit`  
**상태**: 🔍 원인 분석 완료

---

## 🔍 문제 원인 분석

### 에러 메시지
```
remote: error: File payroll_generator/assets/nanum-all_new.zip is 125.32 MB; 
this exceeds GitHub's file size limit of 100.00 MB
remote: error: GH001: Large files detected. You may want to try Git Large File Storage
```

### 핵심 문제

**`git rm --cached`로 파일을 제거했지만, Git 히스토리에 여전히 남아있음**

1. **현재 상태**:
   - ✅ 최신 커밋에서 큰 파일 제거됨
   - ❌ **이전 커밋 히스토리에 큰 파일이 남아있음**
   - ❌ GitHub는 전체 히스토리를 push할 때 큰 파일을 감지하여 거부

2. **왜 발생하는가?**
   - Git은 모든 커밋 히스토리를 저장합니다
   - 파일을 삭제해도 이전 커밋에 파일이 남아있습니다
   - GitHub는 push할 때 전체 히스토리를 검사합니다
   - 100MB 이상의 파일이 히스토리에 있으면 push를 거부합니다

---

## ✅ 해결 방법

### 방법 1: 얕은 클론으로 새 저장소 생성 (가장 간단, 권장) ⭐

현재 상태만 새 저장소로 만드는 방법:

```bash
# 1. 현재 작업 디렉토리 확인
cd /Users/jisungs/Documents/dev/sideprojects/salary_cal

# 2. 현재 상태 백업 (안전을 위해)
cd ..
cp -r salary_cal salary_cal_backup

# 3. 새 Git 저장소 초기화
cd salary_cal
rm -rf .git
git init

# 4. 현재 파일만 추가 (히스토리 없이)
git add .

# 5. 초기 커밋
git commit -m "Initial commit: 웹 프로젝트 배포용"

# 6. 원격 저장소 연결
git remote add origin https://github.com/jisungs/sal_cal.git

# 7. 기존 브랜치 삭제 후 새로 push (force push)
git branch -M main
git push -u origin main --force
```

**장점**:
- ✅ 가장 간단하고 빠름
- ✅ 히스토리 정리 불필요
- ✅ 저장소 크기 최소화

**단점**:
- ❌ 이전 커밋 히스토리 손실 (웹 배포에는 문제 없음)

### 방법 2: Git 히스토리에서 큰 파일 완전 제거

이전 히스토리를 유지하면서 큰 파일만 제거:

#### 2-1. git filter-branch 사용 (Git 내장)

```bash
# 큰 파일을 히스토리에서 완전히 제거
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch payroll_generator/assets/nanum-all_new.zip" \
  --prune-empty --tag-name-filter cat -- --all

# 원격 저장소에 force push
git push origin --force --all
```

**주의**: 이 방법은 시간이 오래 걸리고 복잡할 수 있습니다.

#### 2-2. git filter-repo 사용 (더 빠름, 권장)

```bash
# git-filter-repo 설치
pip install git-filter-repo

# 큰 파일 제거
git filter-repo --path payroll_generator/assets/nanum-all_new.zip --invert-paths

# 원격 저장소에 force push
git push origin --force --all
```

**장점**:
- ✅ 이전 히스토리 유지
- ✅ 더 빠르고 안전함

**단점**:
- ❌ 추가 도구 설치 필요
- ❌ 히스토리 재작성으로 인한 복잡성

### 방법 3: Git LFS 사용 (큰 파일 유지 필요 시)

큰 파일을 유지해야 하는 경우:

```bash
# Git LFS 설치
brew install git-lfs

# Git LFS 초기화
git lfs install

# 큰 파일을 LFS로 추적
git lfs track "*.zip"
git lfs track "payroll_generator/assets/nanum-all_new.zip"

# .gitattributes 파일 커밋
git add .gitattributes
git commit -m "chore: Git LFS 설정"

# 히스토리에서 큰 파일을 LFS로 마이그레이션
git lfs migrate import --include="payroll_generator/assets/nanum-all_new.zip" --everything

# Push
git push -u origin main
```

**주의**: Git LFS는 GitHub에서 무료로 제공하지만 용량 제한이 있습니다.

---

## 🎯 권장 해결 방법

### 웹 프로젝트만 배포하는 경우: **방법 1 (얕은 클론)** 권장

웹 프로젝트 배포에는 이전 히스토리가 필요하지 않으므로, 가장 간단한 방법을 권장합니다.

### 실행 스크립트

다음 명령어를 순서대로 실행하세요:

```bash
# 1. 백업 (선택사항)
cd /Users/jisungs/Documents/dev/sideprojects
cp -r salary_cal salary_cal_backup

# 2. 새 저장소 초기화
cd salary_cal
rm -rf .git
git init

# 3. 현재 파일만 추가
git add .

# 4. 초기 커밋
git commit -m "Initial commit: 웹 프로젝트 배포용

- Flask 웹 애플리케이션
- 급여명세서 자동 생성 기능
- 템플릿 디자인 지원
- 사용자 인증 시스템"

# 5. 원격 저장소 연결 (기존 원격 제거 후 재추가)
git remote remove origin
git remote add origin https://github.com/jisungs/sal_cal.git

# 6. 브랜치 이름 확인 및 설정
git branch -M main

# 7. Force push (기존 내용 덮어쓰기)
git push -u origin main --force
```

---

## 📊 예상 결과

### 성공 시
```
Enumerating objects: XXXX, done.
Counting objects: 100% (XXXX/XXXX), done.
Delta compression using up to 8 threads
Compressing objects: 100% (XXXX/XXXX), done.
Writing objects: 100% (XXXX/XXXX), XX.XX MiB | XX.XX MiB/s, done.
Total XXXX (delta XXXX), reused 0 (delta 0)
To https://github.com/jisungs/sal_cal.git
 + [remote rejected] main -> main (pre-receive hook declined)
 * [new branch]      main -> main
Branch 'main' set up to track 'remote branch 'main' from 'origin'.
```

### 저장소 크기 예상
- **이전**: 274.35 MiB (큰 파일 포함)
- **이후**: 약 50-100 MB (큰 파일 제외)

---

## ⚠️ 주의사항

1. **백업 필수**
   - 히스토리를 잃을 수 있으므로 백업을 먼저 하세요
   - `salary_cal_backup` 폴더에 백업 권장

2. **Force Push**
   - `--force` 옵션은 원격 저장소의 기존 내용을 덮어씁니다
   - 다른 사람과 협업 중이라면 주의하세요

3. **파일 확인**
   - 큰 파일이 제대로 제외되었는지 확인하세요
   - `git ls-files | xargs du -h | sort -rh | head -10` 명령어로 확인

---

## 🔧 문제 해결 체크리스트

- [ ] 백업 완료
- [ ] 큰 파일이 .gitignore에 포함되어 있는지 확인
- [ ] `git ls-files`로 큰 파일이 추적되지 않는지 확인
- [ ] 새 저장소 초기화
- [ ] 초기 커밋 생성
- [ ] 원격 저장소 연결
- [ ] Force push 실행
- [ ] GitHub에서 파일 확인

---

**다음 단계**: 위의 방법 1 (얕은 클론)을 실행하여 새 저장소로 push하세요!

