#!/bin/bash

# 이 파일이 있는 폴더로 이동
cd "$(dirname "$0")"

# macOS 격리 속성 제거 (처음 실행 시 두 번 열어야 하는 문제 방지)
xattr -dr com.apple.quarantine . 2>/dev/null

echo "=============================="
echo "  교조증 감지기 시작 중..."
echo "=============================="

# Python3 설치 확인
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "Python3가 설치되어 있지 않습니다."
    echo "https://www.python.org/downloads/ 에서 설치 후 다시 실행해주세요."
    read -p "엔터를 눌러 종료..."
    exit 1
fi

# 패키지 설치 (이미 설치된 경우 스킵)
echo ""
echo "필요한 패키지 확인 중..."
pip3 install -r requirements.txt -q

echo ""
echo "카메라 창이 뜨면 시작된 겁니다."
echo "종료하려면 카메라 창에서 q 를 누르세요."
echo ""

python3 nail_biter.py
