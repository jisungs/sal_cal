#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WSGI 진입점 - Railway 배포용"""

import os
from dotenv import load_dotenv
from app import create_app

# .env 파일에서 환경 변수 로드 (로컬 개발 환경용)
# Railway에서는 환경 변수를 대시보드에서 설정하므로 .env 파일은 무시됨
load_dotenv()

# 환경 변수에서 설정 이름 가져오기
config_name = os.environ.get('FLASK_ENV', 'production')

# Flask 앱 생성
app = create_app(config_name)

if __name__ == '__main__':
    # 개발 환경에서만 디버그 모드 활성화
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # 포트 설정: Railway는 PORT 환경 변수를 제공, 없으면 FLASK_RUN_PORT 또는 기본값 5001 사용
    port = int(os.environ.get('PORT', os.environ.get('FLASK_RUN_PORT', 5001)))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

