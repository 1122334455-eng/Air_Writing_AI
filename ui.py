import cv2
from config import COLORS

def draw_ui(img, current_color_name, mode, brush_size):
    cv2.rectangle(img, (0, 0), (800, 70), (40, 40, 40), -1)

    x = 10
    for name, color in COLORS.items():
        cv2.rectangle(img, (x, 10), (x+60, 60), color, -1)
        cv2.putText(img, name[0], (x+20, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        x += 70

    cv2.putText(img, f"Mode: {mode}", (400, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.putText(img, f"Brush: {brush_size}", (600, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
