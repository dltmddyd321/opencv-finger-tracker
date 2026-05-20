# 교조증 감지기 👀

Mac 웹캠으로 손가락이 입 근처에 2초 이상 머물면 경고음을 울려주는 프로그램입니다.
손톱 물어뜯는 습관을 고치고 싶은 분들을 위해 만들었습니다.

## 동작 방식

1. 웹캠으로 얼굴과 손을 실시간 감지
2. 손가락 끝이 입 근처에 2초 이상 머물면 경고음 재생
3. 손을 떼는 순간 경고음 즉시 정지

## 실행 화면

| 상태 | 표시 |
|---|---|
| 정상 | 좌측 상단 **OK** (초록) |
| 손 감지 중 | 빨간 테두리 + 카운트다운 바 |
| 경고 발동 | 경고음 재생 + "손톱 물어뜯지 마세요!!" |

## 설치 및 실행

### 요구사항

- macOS
- Python 3.9 이상
- 웹캠

### 빠른 시작

```bash
# 1. 저장소 클론
git clone https://github.com/dltmddyd321/opencv-finger-tracker.git
cd opencv-finger-tracker

# 2. run.command 실행 권한 부여 (최초 1회)
chmod +x run.command

# 3. 더블클릭으로 실행
# run.command 파일을 Finder에서 더블클릭
```

> **처음 실행 시** macOS 보안 경고가 뜨면 **우클릭 → 열기** 를 선택하세요.
> 이후부터는 더블클릭으로 바로 실행됩니다.

### 직접 실행

```bash
pip3 install -r requirements.txt
python3 nail_biter.py
```

### 종료

카메라 창이 포커스된 상태에서 `q` 키, 또는 터미널에서 `Ctrl+C`

## 경고음 교체

기본 경고음 대신 원하는 MP3 파일을 사용하려면 `nail_biter.py` 상단의 경로를 수정하세요.

```python
SIREN_PATH = os.path.expanduser("~/Downloads/siren.mp3")
```

## 민감도 조정

`nail_biter.py` 상단의 상수를 수정해 동작을 조절할 수 있습니다.

```python
ALERT_DELAY = 2.0      # 경고 발동까지 대기 시간 (초)
DISTANCE_RATIO = 0.55  # 감지 거리 (값이 클수록 더 멀리서도 감지)
```

## 기술 스택

- [MediaPipe](https://mediapipe.dev) — 손/얼굴 랜드마크 감지
- [OpenCV](https://opencv.org) — 웹캠 영상 처리
- [pygame](https://www.pygame.org) — 경고음 재생
