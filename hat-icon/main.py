import cv2
import numpy as np
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

icon = Image.open("hat.png").convert("RGBA")

hat_shown = False

print("[INFO] Starting webcam...")
cap = cv2.VideoCapture(0)

def overlay_icon(frame, x, y):
    scale = 0.5
    icon_resized = icon.resize(
        (int(icon.width * scale), int(icon.height * scale)),
        Image.LANCZOS
    )
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert("RGBA")
    
    # Center the icon above the face
    icon_x = x + (w // 2) - (icon_resized.width // 2)
    icon_y = y - icon_resized.height + 40

    frame_pil.paste(icon_resized, (icon_x, icon_y), icon_resized)
    return cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGBA2BGR)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if not hat_shown:
            hat_shown = True
        if hat_shown:
            frame = overlay_icon(frame, x, y)
    cv2.imshow("Webcam - Hat", frame)

    # Exit on ESC or Q
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
