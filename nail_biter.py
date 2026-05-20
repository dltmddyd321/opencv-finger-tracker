import cv2
import mediapipe as mp
import time
import numpy as np
import pygame
import os

pygame.mixer.init()

SIREN_PATH = os.path.expanduser("~/Downloads/siren.mp3")
siren = pygame.mixer.Sound(SIREN_PATH)

mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

MOUTH_LANDMARKS = [13, 14, 61, 291]
FINGERTIPS = [4, 8, 12, 16, 20]

ALERT_DELAY = 2.0
DISTANCE_RATIO = 0.55


def start_siren():
    if pygame.mixer.get_busy() is False or not siren.get_num_channels():
        siren.play(loops=-1)


def stop_siren():
    siren.stop()


def get_mouth_center(face_lm, w, h):
    pts = [(face_lm.landmark[i].x * w, face_lm.landmark[i].y * h)
           for i in MOUTH_LANDMARKS]
    return (sum(p[0] for p in pts) / len(pts),
            sum(p[1] for p in pts) / len(pts))


def get_face_width(face_lm, w, h):
    left = face_lm.landmark[33]
    right = face_lm.landmark[263]
    dx = (right.x - left.x) * w
    dy = (right.y - left.y) * h
    return np.sqrt(dx * dx + dy * dy)


def get_fingertips(hand_lm, w, h):
    return [(hand_lm.landmark[i].x * w, hand_lm.landmark[i].y * h)
            for i in FINGERTIPS]


def min_dist(tips, mouth):
    return min(np.sqrt((t[0] - mouth[0])**2 + (t[1] - mouth[1])**2)
               for t in tips)


def draw_timer_bar(frame, elapsed, total, w, h):
    ratio = min(elapsed / total, 1.0)
    bar_w = int(w * 0.6)
    bar_x = (w - bar_w) // 2
    bar_y = h - 60
    bar_h = 18
    color = (0, int(255 * (1 - ratio)), int(255 * ratio))
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h),
                  (60, 60, 60), -1)
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + int(bar_w * ratio), bar_y + bar_h), color, -1)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h),
                  (200, 200, 200), 1)


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    hand_near_since = None
    siren_playing = False

    print("교조증 감지 시작! 종료: q")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False

        face_res = face_mesh.process(rgb)
        hand_res = hands.process(rgb)

        mouth_center = None
        face_w = None

        if face_res.multi_face_landmarks:
            fl = face_res.multi_face_landmarks[0]
            mouth_center = get_mouth_center(fl, w, h)
            face_w = get_face_width(fl, w, h)
            cv2.circle(frame, (int(mouth_center[0]), int(mouth_center[1])),
                       6, (0, 220, 0), -1)

        hand_is_near = False

        if hand_res.multi_hand_landmarks and mouth_center and face_w:
            for hl in hand_res.multi_hand_landmarks:
                tips = get_fingertips(hl, w, h)
                dist = min_dist(tips, mouth_center)
                if dist / face_w < DISTANCE_RATIO:
                    hand_is_near = True
                    for t in tips:
                        cv2.circle(frame, (int(t[0]), int(t[1])),
                                   5, (0, 0, 255), -1)

        now = time.time()

        if hand_is_near:
            if hand_near_since is None:
                hand_near_since = now

            elapsed = now - hand_near_since
            draw_timer_bar(frame, elapsed, ALERT_DELAY, w, h)

            cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 220), 6)

            remaining = max(0.0, ALERT_DELAY - elapsed)
            cv2.putText(frame, f"손 치워! {remaining:.1f}s",
                        (w // 2 - 100, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

            if elapsed >= ALERT_DELAY:
                if not siren_playing:
                    start_siren()
                    siren_playing = True
                    print(f"경고 발동! ({time.strftime('%H:%M:%S')})")
                cv2.putText(frame, "손톱 물어뜯지 마세요!!",
                            (w // 2 - 160, h // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3)
        else:
            if siren_playing:
                stop_siren()
                siren_playing = False
            hand_near_since = None
            cv2.putText(frame, "OK", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 0), 2)

        cv2.imshow("nail biter alert", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stop_siren()
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    face_mesh.close()


if __name__ == "__main__":
    main()
