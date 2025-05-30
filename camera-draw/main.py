import cv2
import numpy as np
import mediapipe as mp

# Inicializamos MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Capturamos video de la webcam
cap = cv2.VideoCapture(0)
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# Variables para almacenar la posición anterior del dedo
prev_x, prev_y = 0, 0

# Color inicial del trazo: rojo
draw_color = (0, 0, 255)
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]

# Función para contar cuántos dedos están levantados
def count_fingers(landmarks):
    tips = [8, 12, 16, 20]
    fingers = []
    for tip in tips:
        fingers.append(landmarks[tip].y < landmarks[tip - 2].y)
    return sum(fingers)

# Bucle principal
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_copy = frame.copy()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            h, w, _ = frame.shape
            cx, cy = int(lm[8].x * w), int(lm[8].y * h)

            finger_count = count_fingers(lm)

            if finger_count == 4:
                canvas = np.zeros_like(canvas)

            if finger_count == 2:
                draw_color = colors[(colors.index(draw_color) + 1) % len(colors)]

            if finger_count == 1:
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = cx, cy
                cv2.line(canvas, (prev_x, prev_y), (cx, cy), draw_color, 15)
                prev_x, prev_y = cx, cy
            else:
                prev_x, prev_y = 0, 0

            mp_draw.draw_landmarks(frame_copy, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    combined = cv2.addWeighted(frame_copy, 0.5, canvas, 0.5, 0)
    cv2.imshow("Air Drawing Paint App", combined)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()