# 📄 Day 6 실행 파일 문제 분석 및 해결 보고서

**작성일**: 2025-11-12  
**문제**: dist 폴더에 실행 파일이 생성되었지만 실행 시 문제 발생  
**상태**: ✅ 해결 완료

---

## 🔍 문제 분석

### 발견된 문제점

1. **폰트 파일 경로 문제** ⚠️
   - 로그: `한글 폰트 파일을 찾을 수 없습니다`
   - 원인: PyInstaller 환경에서 `__file__` 기반 경로가 임시 디렉토리를 가리킴
   - 실제 경로: `/var/folders/.../_MEI54d6un/payroll_generator/assets/NanumGothic.ttf` (존재하지 않음)
   - 예상 경로: `assets/NanumGothic.ttf` (build.spec에서 `assets`로 복사됨)

2. **템플릿 파일 경로 문제** ⚠️
   - 기본 템플릿 파일을 찾지 못할 수 있음
   - 같은 원인: PyInstaller 환경에서 상대 경로 처리 문제

3. **설정/로그 파일 경로 문제** ⚠️
   - 임시 디렉토리에 설정 파일 저장 시 프로그램 종료 시 삭제됨
   - 사용자 데이터가 유지되지 않음

---

## ✅ 해결 방법

### 1. PyInstaller 리소스 경로 처리 함수 추가

**파일**: `payroll_generator/utils.py`

```python
def resource_path(relative_path):
    """PyInstaller로 빌드된 실행 파일에서 리소스 경로를 올바르게 반환"""
    try:
        # PyInstaller로 빌드된 실행 파일인지 확인
        base_path = sys._MEIPASS
    except Exception:
        # 개발 환경에서는 현재 파일의 디렉토리 기준
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)
```

### 2. 폰트 파일 경로 수정

**파일**: `payroll_generator/pdf_generator.py`

- `resource_path('assets/NanumGothic.ttf')` 추가
- PyInstaller 환경과 개발 환경 모두 지원

### 3. 템플릿 파일 경로 수정

**파일**: `main.py`

- `resource_path('templates/employee_template.xlsx')` 추가
- 여러 경로를 시도하여 찾기

### 4. 설정/로그 파일 경로 수정

**파일**: `payroll_generator/logger.py`, `payroll_generator/settings.py`, `payroll_generator/history_manager.py`

- PyInstaller 환경에서는 사용자 홈 디렉토리 사용
- 경로: `~/.급여명세서생성기/`
- 개발 환경에서는 기존 경로 유지

---

## 📝 수정된 파일 목록

1. ✅ `payroll_generator/utils.py`
   - `resource_path()` 함수 추가

2. ✅ `payroll_generator/pdf_generator.py`
   - 폰트 경로에 `resource_path()` 사용

3. ✅ `main.py`
   - 템플릿 파일 경로에 `resource_path()` 사용
   - `resource_path` import 추가

4. ✅ `payroll_generator/logger.py`
   - PyInstaller 환경에서 홈 디렉토리에 로그 저장

5. ✅ `payroll_generator/settings.py`
   - PyInstaller 환경에서 홈 디렉토리에 설정 저장

6. ✅ `payroll_generator/history_manager.py`
   - PyInstaller 환경에서 홈 디렉토리에 이력 저장

---

## 🧪 테스트 방법

### 1. 재빌드
```bash
cd /Users/jisungs/Documents/dev/sideprojects/salary_cal
./build.sh
```

### 2. 실행 테스트
```bash
./dist/급여명세서생성기
```

### 3. 확인 사항
- [ ] 프로그램 정상 실행
- [ ] 폰트 파일 정상 로드 (로그 확인)
- [ ] 템플릿 파일 정상 로드
- [ ] 설정 파일 홈 디렉토리에 저장
- [ ] 로그 파일 홈 디렉토리에 저장

---

## 📊 예상 결과

### 수정 전
```
WARNING - 한글 폰트 파일을 찾을 수 없습니다
```

### 수정 후
```
INFO - 한글 폰트 등록 완료: /var/folders/.../_MEIxxx/assets/NanumGothic.ttf
```

---

## ⚠️ 주의사항

1. **재빌드 필요**: 코드 수정 후 반드시 재빌드 필요
2. **홈 디렉토리 권한**: 사용자 홈 디렉토리에 쓰기 권한 필요
3. **경로 일치**: `build.spec`의 데이터 경로와 코드의 경로가 일치해야 함

---

## 🔗 관련 파일

- `build.spec`: 빌드 설정 파일
- `payroll_generator/utils.py`: 리소스 경로 처리 함수
- `plan/Day6_PyInstaller빌드설정_보고서.md`: 빌드 설정 보고서

---

**작성자**: AI Assistant  
**상태**: ✅ 해결 완료  
**다음 작업**: 재빌드 및 테스트

