import cv2
import sys

img = cv2.imread('imagens/1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

for x in range(5, 12):
    for y in range(4, x+1):
        ret, corners = cv2.findChessboardCornersSB(gray, (x, y), cv2.CALIB_CB_EXHAUSTIVE)
        if ret:
            print(f"FOUND! x={x}, y={y}")
            sys.exit(0)
print("Not found anywhere.")
