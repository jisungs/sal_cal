#!/bin/bash
# 급여명세서 자동생성기 빌드 스크립트 (macOS - .app 번들 및 .pkg 생성)

echo "=========================================="
echo "급여명세서 자동생성기 빌드 시작 (macOS)"
echo "=========================================="

# 가상환경 활성화 확인
if [ ! -d "venv" ]; then
    echo "❌ 가상환경이 없습니다. 먼저 가상환경을 생성하세요."
    exit 1
fi

# 가상환경 활성화
source venv/bin/activate

# PyInstaller 설치 확인
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller가 설치되어 있지 않습니다."
    echo "다음 명령어로 설치하세요: pip install pyinstaller"
    exit 1
fi

# macOS 확인
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  이 스크립트는 macOS용입니다."
    echo "Linux에서는 build_linux.sh를 사용하세요."
    exit 1
fi

# 이전 빌드 정리
echo "📦 이전 빌드 정리 중..."
rm -rf build/ dist/ *.pkg

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

# .app 번들 빌드 실행
echo "🔨 .app 번들 빌드 실행 중..."
pyinstaller build_configs/build_mac.spec --clean

# 빌드 결과 확인
if [ -d "dist/급여명세서생성기.app" ]; then
    echo ""
    echo "✅ .app 번들 빌드 성공!"
    echo "📁 빌드 결과: dist/급여명세서생성기.app"
    echo "📊 파일 크기: $(du -sh dist/급여명세서생성기.app | cut -f1)"
    
    # .pkg 인스톨러 생성
    echo ""
    echo "📦 .pkg 인스톨러 생성 중..."
    
    # 임시 패키징 디렉토리 생성
    PKG_DIR="dist/pkg_temp"
    rm -rf "$PKG_DIR"
    mkdir -p "$PKG_DIR/Applications"
    
    # .app을 Applications 폴더 구조로 복사
    cp -R "dist/급여명세서생성기.app" "$PKG_DIR/Applications/"
    
    # pkgbuild로 .pkg 생성
    if pkgbuild --root "$PKG_DIR" \
                --identifier "com.salarycal.payrollgenerator" \
                --version "1.0.0" \
                --install-location "/" \
                "dist/급여명세서생성기.pkg" 2>/dev/null; then
        # 성공
        :
    else
        # 실패 시 절대 경로로 재시도
        ABS_PKG_DIR=$(cd "$PKG_DIR" && pwd)
        pkgbuild --root "$ABS_PKG_DIR" \
                 --identifier "com.salarycal.payrollgenerator" \
                 --version "1.0.0" \
                 --install-location "/" \
                 "$(pwd)/dist/급여명세서생성기.pkg" 2>/dev/null || true
    fi
    
    # 임시 디렉토리 정리
    rm -rf "$PKG_DIR"
    
    if [ -f "dist/급여명세서생성기.pkg" ]; then
        echo ""
        echo "✅ .pkg 인스톨러 생성 성공!"
        echo "📁 인스톨러: dist/급여명세서생성기.pkg"
        echo "📊 파일 크기: $(du -sh dist/급여명세서생성기.pkg | cut -f1)"
        echo ""
        echo "실행 방법:"
        echo "  .app 번들: open dist/급여명세서생성기.app"
        echo "  .pkg 인스톨러: open dist/급여명세서생성기.pkg"
    else
        echo ""
        echo "⚠️  .pkg 생성 실패 (선택사항)"
        echo "✅ .app 번들은 정상적으로 생성되었습니다."
    fi
else
    echo ""
    echo "❌ 빌드 실패!"
    exit 1
fi

