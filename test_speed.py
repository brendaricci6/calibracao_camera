import cv2
import time
import sys

img = cv2.imread('imagens/1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("Image shape:", gray.shape)

t0 = time.time()
ret, corners = cv2.findChessboardCorners(gray, (9, 6), cv2.CALIB_CB_FAST_CHECK)
t1 = time.time()
print(f"findChessboardCorners (FAST_CHECK): {ret}, Time: {t1-t0:.2f}s")

if hasattr(cv2, 'findChessboardCornersSB'):
    t0 = time.time()
    retSB, cornersSB = cv2.findChessboardCornersSB(gray, (9, 6), cv2.CALIB_CB_EXHAUSTIVE | cv2.CALIB_CB_ACCURACY)
    t1 = time.time()
    print(f"findChessboardCornersSB: {retSB}, Time: {t1-t0:.2f}s")
