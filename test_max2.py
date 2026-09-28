import cv2
import sys

img = cv2.imread('imagens/2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

for x in range(12, 5, -1):
    for y in range(x, 4, -1):
        ret, corners = cv2.findChessboardCornersSB(gray, (x, y), cv2.CALIB_CB_EXHAUSTIVE)
        if ret:
            print(f"2.jpg MAX found: x={x}, y={y}")
            sys.exit(0)
print("None found.")
