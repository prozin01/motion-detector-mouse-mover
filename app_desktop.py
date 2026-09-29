import time
from collections import deque
import subprocess
import sys

try:
    import cv2
    import numpy as np
    import pyautogui
except ImportError:
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "opencv-python", "numpy", "PyAutoGUI"])
    import cv2
    import numpy as np
    import pyautogui

WINDOW = "Motion Tracker - clique em um alvo; F ativa/desativa o mouse real"
CAMERA_WIDTH, CAMERA_HEIGHT = 640, 480
MIN_CONTOUR_AREA = 900
SMOOTHING = 5

# Fail-safe: mover o mouse para o canto superior esquerdo interrompe o programa.
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

selected = None
follow_enabled = False
positions = deque(maxlen=SMOOTHING)


def on_mouse(event, x, y, _flags, _param):
    global selected
    if event == cv2.EVENT_LBUTTONDOWN:
        selected = (x, y)


def find_motion(previous, current):
    previous_gray = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
    previous_gray = cv2.GaussianBlur(previous_gray, (21, 21), 0)
    current_gray = cv2.GaussianBlur(current_gray, (21, 21), 0)

    difference = cv2.absdiff(previous_gray, current_gray)
    _, threshold = cv2.threshold(difference, 28, 255, cv2.THRESH_BINARY)
    threshold = cv2.dilate(threshold, None, iterations=2)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    targets = []
    for contour in contours:
        if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        targets.append((x + w // 2, y + h // 2, x, y, w, h))
    return targets


def select_nearest(targets):
    if selected is None or not targets:
        return None
    return min(targets, key=lambda target: (target[0] - selected[0]) ** 2 + (target[1] - selected[1]) ** 2)


def move_system_mouse(target, frame_width, frame_height):
    if target is None:
        return
    positions.append((target[0], target[1]))
    average_x = sum(position[0] for position in positions) / len(positions)
    average_y = sum(position[1] for position in positions) / len(positions)
    screen_width, screen_height = pyautogui.size()
    screen_x = int(np.clip(average_x / frame_width * screen_width, 0, screen_width - 1))
    screen_y = int(np.clip(average_y / frame_height * screen_height, 0, screen_height - 1))
    pyautogui.moveTo(screen_x, screen_y, duration=0.03)


def main():
    global selected, follow_enabled
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    if not camera.isOpened():
        raise RuntimeError("Não foi possível abrir a câmera.")

    cv2.namedWindow(WINDOW)
    cv2.setMouseCallback(WINDOW, on_mouse)
    previous = None
    print("\n✓ Câmera iniciada!")
    print("Clique em um alvo na janela. Pressione F para seguir com o mouse real; ESC para sair.\n")

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            display = frame.copy()
            targets = [] if previous is None else find_motion(previous, frame)
            target = select_nearest(targets)

            for center_x, center_y, x, y, width, height in targets:
                color = (0, 220, 255) if target and (center_x, center_y) == target[:2] else (120, 120, 120)
                cv2.rectangle(display, (x, y), (x + width, y + height), color, 2)
                cv2.circle(display, (center_x, center_y), 5, color, -1)

            if selected:
                cv2.drawMarker(display, selected, (255, 90, 90), cv2.MARKER_CROSS, 24, 2)
            if follow_enabled and target:
                move_system_mouse(target, frame.shape[1], frame.shape[0])

            state = "ATIVO: mouse real" if follow_enabled else "PAUSADO: pressione F"
            cv2.putText(display, state, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (70, 230, 150) if follow_enabled else (220, 220, 220), 2)
            cv2.putText(display, "Clique no objeto | F liga/desliga | ESC sai", (12, frame.shape[0] - 14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230, 230, 230), 1)
            cv2.imshow(WINDOW, display)
            previous = frame

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            if key in (ord("f"), ord("F")):
                follow_enabled = not follow_enabled
                positions.clear()
                print("Acompanhamento do mouse real:", "ATIVO" if follow_enabled else "PAUSADO")
            time.sleep(0.005)
    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("\n✓ Aplicação finalizada.")
