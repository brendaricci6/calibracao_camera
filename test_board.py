import cv2
import sys

img = cv2.imread('imagens/1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.resize(gray, (0,0), fx=0.2, fy=0.2) # speed up

for x in range(3, 12):
    for y in range(3, 12):
        ret, corners = cv2.findChessboardCorners(gray, (x, y), cv2.CALIB_CB_FAST_CHECK)
        if ret:
            print(f"Found! x={x}, y={y}")
            sys.exit(0)
print("Not found in quick test.")
