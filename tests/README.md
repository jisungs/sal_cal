# 🧪 테스트 가이드

**작성일**: 2025-12-11

---

## 📋 테스트 파일 목록

### 단위 테스트
1. **test_config.py** - 설정 파일 테스트
2. **test_cleanup.py** - 파일 정리 기능 테스트
3. **test_app_init.py** - Flask 앱 초기화 테스트
4. **test_error_handlers.py** - 에러 핸들러 테스트

### 통합 테스트
5. **integration_test_scenarios.md** - 통합 테스트 시나리오

### 유틸리티
6. **run_all_tests.py** - 전체 테스트 실행 스크립트

---

## 🚀 테스트 실행 방법

### 1. 환경 준비

```bash
# 가상환경 활성화
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# 의존성 확인
pip install -r requirements-web.txt
```

### 2. 단위 테스트 실행

```bash
# 개별 테스트 실행
python tests/test_config.py
python tests/test_cleanup.py
python tests/test_app_init.py
python tests/test_error_handlers.py

# 전체 테스트 실행
python tests/run_all_tests.py
```

### 3. 통합 테스트 실행

```bash
# Flask 앱 실행
python app.py

# 브라우저에서 테스트
# http://localhost:5001
```

---

## 📊 예상 결과

모든 테스트가 통과해야 합니다. 실패하는 테스트가 있으면 해당 기능을 확인하세요.

---

**작성자**: AI Assistant  
**작성일**: 2025-12-11
