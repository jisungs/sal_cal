#!/bin/bash
# 웹 서버 실행 스크립트 (Linux/Mac)

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

# 가상환경 활성화
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ 가상환경을 찾을 수 없습니다. venv 폴더를 확인하세요."
    exit 1
fi

# 의존성 확인 및 설치
if ! python -c "import flask" 2>/dev/null; then
    echo "⚠️ Flask가 설치되어 있지 않습니다. 설치 중..."
    pip install -r requirements-web.txt
fi

# Flask 앱 실행
export FLASK_APP=app.py
export FLASK_DEBUG=True
# FLASK_ENV는 Flask 3.x에서 deprecated되었으므로 제거
# 포트 설정: 기본값 5001 (macOS AirPlay와 충돌 방지)
# 다른 포트를 사용하려면: export FLASK_RUN_PORT=5002
export FLASK_RUN_PORT=${FLASK_RUN_PORT:-5001}

echo "🌐 웹 서버 시작 중..."
echo "📍 접속 주소: http://localhost:${FLASK_RUN_PORT}"
echo ""

python app.py

