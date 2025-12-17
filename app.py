#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""급여명세서 자동생성기 웹 버전 - Flask 애플리케이션 진입점"""

import os
from app import create_app

# 환경 변수에서 설정 이름 가져오기
config_name = os.environ.get('FLASK_ENV', 'development')

# Flask 앱 생성
app = create_app(config_name)

if __name__ == '__main__':
    # 개발 환경에서만 디버그 모드 활성화
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # 포트 설정: Railway는 PORT 환경 변수를 제공, 없으면 FLASK_RUN_PORT 또는 기본값 5001 사용
    port = int(os.environ.get('PORT', os.environ.get('FLASK_RUN_PORT', 5001)))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
