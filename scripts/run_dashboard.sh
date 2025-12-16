#!/bin/bash
# 대시보드 실행 스크립트

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."
source venv/bin/activate
python scripts/view_dashboard.py

