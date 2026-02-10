import cv2
from config import COLORS, BRUSH_THICKNESS, ERASER_THICKNESS

class DrawingBoard:
    def __init__(self):
        self.prev_x, self.prev_y = 0, 0
        self.color_names = list(COLORS.keys())
        self.color_index = 0
        self.brush_size = BRUSH_THICKNESS

    def change_color(self, index):
        self.color_index = index % len(self.color_names)

    def draw(self, canvas, x, y):
        color_name = self.color_names[self.color_index]
        color = COLORS[color_name]

        thickness = ERASER_THICKNESS if color_name == "ERASER" else self.brush_size

        if self.prev_x == 0:
            self.prev_x, self.prev_y = x, y

        # ✨ Smooth drawing
        x = int(0.7*self.prev_x + 0.3*x)
        y = int(0.7*self.prev_y + 0.3*y)

        cv2.line(canvas, (self.prev_x, self.prev_y), (x, y), color, thickness)
        self.prev_x, self.prev_y = x, y

    def reset(self):
        self.prev_x, self.prev_y = 0, 0
