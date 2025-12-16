# 🖥️ GUI 실행 가이드

**작성일**: 2025-11-11  
**프로젝트**: 급여명세서 자동생성기

---

## 📋 GUI 실행 방법

### 방법 1: 터미널에서 실행 (권장)

#### 1단계: 프로젝트 디렉토리로 이동
```bash
cd /Users/jisungs/Documents/dev/sideprojects/salary_cal
```

#### 2단계: 가상환경 활성화
```bash
source venv/bin/activate
```

#### 3단계: GUI 실행
```bash
python main.py
```

또는 한 줄로:
```bash
cd /Users/jisungs/Documents/dev/sideprojects/salary_cal && source venv/bin/activate && python main.py
```

---

### 방법 2: 실행 스크립트 사용

프로젝트에 `run_dashboard.sh` 파일이 있다면:
```bash
./run_dashboard.sh
```

또는 직접 실행:
```bash
bash run_dashboard.sh
```

---

## 🔍 GUI 실행 확인 사항

### 급여명세서 생성 탭 테스트

#### 1. 파일 선택 및 미리보기
1. **"급여명세서 생성"** 탭 클릭
2. **"찾아보기"** 버튼 클릭
3. `payroll_generator/templates/employee_template.xlsx` 파일 선택
4. **미리보기 트리뷰**에 데이터가 표시되는지 확인
   - 이름, 주민번호(마스킹), 입사일, 기본급 표시 확인
5. 주민번호가 `123456-*******` 형식으로 마스킹되어 있는지 확인

#### 2. 오류 메시지 테스트
1. **"찾아보기"** 버튼 클릭
2. 파일 선택 다이얼로그에서 **취소** 버튼 클릭
3. **"생성하기"** 버튼 클릭
4. **인라인 오류 메시지**가 표시되는지 확인
   - "직원 정보 파일을 선택해주세요! 😊" 메시지 확인

#### 3. 급여명세서 생성 테스트
1. 파일 선택 (employee_template.xlsx)
2. 미리보기 확인
3. **"생성하기"** 버튼 클릭
4. **진행 상태** 확인
   - 진행률 바 업데이트 확인
   - "처리 중: [직원명] (1/3)" 메시지 확인
5. 완료 후 **"📁 출력 폴더 열기"** 버튼이 활성화되는지 확인
6. 버튼 클릭하여 출력 폴더가 열리는지 확인

#### 4. 출력 파일 확인
1. 출력 폴더 열기
2. 생성된 엑셀 파일 확인
   - `홍길동_급여명세서.xlsx`
   - `김영희_급여명세서.xlsx`
   - `이철수_급여명세서.xlsx`
3. 파일을 열어 내용 확인
   - 급여 계산 결과 정확성 확인
   - 스타일링 확인

---

### 대시보드 탭 테스트

#### 1. 기본 파일 로드
1. **"대시보드"** 탭 클릭
2. 기본 파일이 자동으로 로드되는지 확인
   - 카드 위젯에 데이터 표시 확인
   - 그래프 표시 확인

#### 2. 파일 선택 및 업데이트
1. **"📁 파일 선택"** 버튼 클릭
2. `payroll_generator/templates/employee_template.xlsx` 파일 선택
3. 대시보드가 업데이트되는지 확인
   - 카드 내용 업데이트
   - 그래프 업데이트

#### 3. 카드 위젯 확인
- **총 직원 수** 카드: 직원 수, 총급여, 총공제 표시
- **근무현황** 카드: 정규직, 계약직, 신입 수 표시
- **특이사항** 카드: 특이사항 목록 표시

#### 4. 그래프 확인
- **월별 급여 지출 현황**: 막대 그래프 표시
- **근무자 구성**: 도넛 차트 표시

---

## ⚠️ 문제 해결

### GUI가 실행되지 않는 경우

#### 1. 가상환경이 활성화되지 않은 경우
```bash
# 가상환경 활성화 확인
which python
# 출력: /Users/jisungs/Documents/dev/sideprojects/salary_cal/venv/bin/python

# 가상환경 활성화
source venv/bin/activate
```

#### 2. 필요한 패키지가 설치되지 않은 경우
```bash
# 패키지 설치
pip install -r requirements.txt
```

#### 3. Python 버전 확인
```bash
python --version
# Python 3.8 이상 필요
```

#### 4. tkinter가 설치되지 않은 경우 (macOS)
```bash
# tkinter는 Python과 함께 설치되어야 함
python -m tkinter
# GUI 창이 열리면 정상
```

---

## 🎯 테스트 체크리스트

### 급여명세서 생성 탭
- [ ] 파일 선택 버튼 동작
- [ ] 미리보기 트리뷰 표시
- [ ] 주민번호 마스킹 처리
- [ ] 인라인 오류 메시지 표시
- [ ] 급여명세서 생성
- [ ] 진행 상태 표시
- [ ] 출력 폴더 열기 버튼 동작

### 대시보드 탭
- [ ] 기본 파일 자동 로드
- [ ] 파일 선택 버튼 동작
- [ ] 카드 위젯 표시
- [ ] 그래프 표시
- [ ] 데이터 업데이트

### 전체 기능
- [ ] 탭 전환 동작
- [ ] 창 크기 조절
- [ ] 오류 처리 동작

---

## 📝 실행 로그 확인

GUI 실행 중 오류가 발생하면 로그 파일을 확인하세요:
```bash
cat payroll_generator/logs/app.log
```

또는 실시간 로그 확인:
```bash
tail -f payroll_generator/logs/app.log
```

---

## 🚀 빠른 실행 명령어

터미널에서 다음 명령어로 바로 실행:
```bash
cd /Users/jisungs/Documents/dev/sideprojects/salary_cal && source venv/bin/activate && python main.py
```

또는 별칭(alias) 설정:
```bash
# ~/.zshrc 또는 ~/.bashrc에 추가
alias run-payroll="cd /Users/jisungs/Documents/dev/sideprojects/salary_cal && source venv/bin/activate && python main.py"
```

그 다음:
```bash
run-payroll
```

---

**마지막 업데이트**: 2025-11-11

