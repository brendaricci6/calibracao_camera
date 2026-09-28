import cv2

img = cv2.imread('imagens/1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, corners = cv2.findChessboardCornersSB(gray, (9, 6), cv2.CALIB_CB_EXHAUSTIVE | cv2.CALIB_CB_ACCURACY)
if ret:
    print("Found with SB 9x6!")
else:
    print("Not found with SB 9x6.")
