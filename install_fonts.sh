#!/bin/bash
# Railway 빌드 시 한글 폰트 설치 스크립트

set -e

echo "한글 폰트 설치 시작..."

# 폰트 디렉토리 생성
mkdir -p /usr/share/fonts/truetype/nanum
mkdir -p ~/.fonts

# 프로젝트의 한글 폰트 파일 찾기 및 복사
FONT_SOURCE=""
if [ -f "payroll_generator/assets/NanumGothic.ttf" ]; then
    FONT_SOURCE="payroll_generator/assets/NanumGothic.ttf"
elif [ -f "payroll_generator/assets/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf" ]; then
    FONT_SOURCE="payroll_generator/assets/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf"
fi

if [ -n "$FONT_SOURCE" ]; then
    echo "폰트 파일 찾음: $FONT_SOURCE"
    cp "$FONT_SOURCE" /usr/share/fonts/truetype/nanum/
    cp "$FONT_SOURCE" ~/.fonts/
    echo "폰트 파일 복사 완료"
else
    echo "경고: 한글 폰트 파일을 찾을 수 없습니다. 시스템 폰트를 사용합니다."
fi

# 추가 한글 폰트 설치 (apt를 통해)
apt-get update && apt-get install -y fonts-nanum fonts-nanum-coding fontconfig || true

# 폰트 캐시 업데이트
fc-cache -fv

echo "한글 폰트 설치 완료"

