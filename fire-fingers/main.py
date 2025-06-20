import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

ICON_PATH = "diamond.png"

def load_icon(scale):
    icon = Image.open(ICON_PATH).convert("RGBA")
    w, h = icon.size
    return icon.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

fire_icon = load_icon(scale=0.15)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def draw_fire(frame, x, y):
    icon_w, icon_h = fire_icon.size
    icon_x = int(x - icon_w / 2)
    icon_y = int(y - icon_h - 10)

    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert("RGBA")
    frame_pil.paste(fire_icon, (icon_x, icon_y), fire_icon)
    return cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGBA2BGR)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        h, w, _ = frame.shape
        fingertip_ids = [4, 8, 12, 16, 20]

        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            for tip_id in fingertip_ids:
                tip = landmarks[tip_id]
                pip = landmarks[tip_id - 2]

                if tip.y < pip.y:
                    cx, cy = int(tip.x * w), int(tip.y * h)
                    frame = draw_fire(frame, cx, cy)

    cv2.imshow("🔥 Finger Fire", frame)

    if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
        break

cap.release()
cv2.destroyAllWindows()
