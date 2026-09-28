import cv2
import time

img = cv2.imread('imagens/1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = gray.shape

scale = 1024.0 / max(w, h)
new_w, new_h = int(w * scale), int(h * scale)
gray_small = cv2.resize(gray, (new_w, new_h))

for x in range(5, 11):
    for y in range(5, 11):
        if x < y: continue # avoid duplicates due to symmetry
        ret, corners_small = cv2.findChessboardCorners(gray_small, (x, y), cv2.CALIB_CB_FAST_CHECK)
        if ret:
            print(f"Found! x={x}, y={y}")
            exit(0)
print("Not found for any size between 5 and 10.")
