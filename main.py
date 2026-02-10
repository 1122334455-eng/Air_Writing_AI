import cv2
import numpy as np
from hand_tracking import HandTracker
from drawing import DrawingBoard
from ui import draw_ui
from config import COLORS
import time

cap = cv2.VideoCapture(0)
tracker = HandTracker()
board = DrawingBoard()

canvas = None
mode = "DRAW"

history = []
prev_time = 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    lm_list = tracker.get_landmarks(frame)

    color_name = list(COLORS.keys())[board.color_index]
    draw_ui(frame, color_name, mode, board.brush_size)

    if lm_list:
        x1, y1 = lm_list[8][1:]
        x2, y2 = lm_list[12][1:]

        # 2 finger select
        if abs(y1 - y2) < 40:
            mode = "SELECT"
            board.reset()

            if y1 < 70:
                index = x1 // 70
                board.change_color(index)

        else:
            mode = "DRAW"
            board.draw(canvas, x1, y1)

            # save history for undo
            history.append(canvas.copy())
            if len(history) > 20:
                history.pop(0)

        # ✋ 3 finger clear
        if len(lm_list) > 16:
            if lm_list[8][2] < lm_list[6][2] and lm_list[12][2] < lm_list[10][2] and lm_list[16][2] < lm_list[14][2]:
                canvas = np.zeros_like(frame)

        # 👍 thumb save
        if lm_list[4][2] < lm_list[3][2]:
            filename = f"saved/auto_{int(time.time())}.png"
            cv2.imwrite(filename, canvas)
            print("Auto Saved")

    frame = cv2.add(frame, canvas)

    # FPS
    curr_time = time.time()
    fps = 1/(curr_time-prev_time) if curr_time!=prev_time else 0
    prev_time = curr_time

    cv2.putText(frame, f"FPS:{int(fps)}", (10,450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.putText(frame, "S=Save  U=Undo  C=Clear  +/- Brush  Q=Quit",
                (10,480), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    cv2.imshow("🔥 Air Writing AI Pro MAX", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        filename = f"saved/drawing_{int(time.time())}.png"
        cv2.imwrite(filename, canvas)
        print("Saved:", filename)

    if key == ord('u') and history:
        canvas = history.pop()

    if key == ord('c'):
        canvas = np.zeros_like(frame)

    if key == ord('+'):
        board.brush_size += 2

    if key == ord('-'):
        board.brush_size = max(2, board.brush_size - 2)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
