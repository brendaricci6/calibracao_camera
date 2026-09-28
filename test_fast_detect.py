import cv2
import time

img = cv2.imread('imagens/1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = gray.shape

t0 = time.time()
scale = 1024.0 / max(w, h)
new_w, new_h = int(w * scale), int(h * scale)
gray_small = cv2.resize(gray, (new_w, new_h))

ret, corners_small = cv2.findChessboardCorners(gray_small, (9, 6), cv2.CALIB_CB_FAST_CHECK)

if ret:
    corners = corners_small / scale
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    t1 = time.time()
    print(f"Found and refined! Time: {t1-t0:.2f}s")
else:
    t1 = time.time()
    print(f"Not found in small image. Time: {t1-t0:.2f}s")
