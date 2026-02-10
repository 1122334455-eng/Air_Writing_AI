import cv2

# Colors: Blue, Green, Red, Black (eraser)
colors = [(255,0,0), (0,255,0), (0,0,255), (0,0,0)]
color_names = ["BLUE","GREEN","RED","ERASER"]

def draw_ui(img, current_color):
    # top panel background
    cv2.rectangle(img, (0,0), (640,60), (50,50,50), -1)

    # color boxes
    for i, color in enumerate(colors):
        cv2.rectangle(img, (10+i*80,10), (70+i*80,50), color, -1)

    # current color text
    cv2.putText(img, f"Color: {color_names[current_color]}",
                (350,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
