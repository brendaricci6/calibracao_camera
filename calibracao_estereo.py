import numpy as np
import cv2
import glob

# msm config de sempre do vri
num_intersecoes_y = 6
num_intersecoes_x = 9
tamanho_quadrado_mm = 25.0

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((num_intersecoes_x * num_intersecoes_y, 3), np.float32)
objp[:, :2] = np.mgrid[0:num_intersecoes_x, 0:num_intersecoes_y].T.reshape(-1, 2)
objp = objp * tamanho_quadrado_mm

objpoints = [] 
imgpoints_left = [] 
imgpoints_right = [] 

images_left = sorted(glob.glob('imagens/left*.jpg'))
images_right = sorted(glob.glob('imagens/right*.jpg'))

if not images_left or not images_right:
    print("Mano n achei par de fotos L/R. roda o dowload_samples la.")
    exit()

img_shape = None

print("Iniciando baguncinha do estereo...")
for imgLeft_path, imgRight_path in zip(images_left, images_right):
    print(f"Lendo parzinho: {imgLeft_path} e {imgRight_path}...")
    imgL = cv2.imread(imgLeft_path)
    imgR = cv2.imread(imgRight_path)
    
    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
    
    if img_shape is None:
        img_shape = grayL.shape[::-1]

    # fast check eh vida
    flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
    retL, cornersL = cv2.findChessboardCorners(grayL, (num_intersecoes_x, num_intersecoes_y), flags)
    retR, cornersR = cv2.findChessboardCorners(grayR, (num_intersecoes_x, num_intersecoes_y), flags)

    if retL and retR:
        objpoints.append(objp)
        corners2L = cv2.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), criteria)
        corners2R = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)
        imgpoints_left.append(corners2L)
        imgpoints_right.append(corners2R)

if len(objpoints) > 0:
    print("Rodando calibracao pra esq...")
    retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpoints_left, img_shape, None, None)
    
    print("Agora calib. pra camera da dir...")
    retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpoints_right, img_shape, None, None)

    print("Juntando td e fzendo a calib estéreo valendo msm...")
    flags = 0
    flags |= cv2.CALIB_FIX_INTRINSIC
    
    criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
    
    # essa func aq devolve um caminhao de varivel
    retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(
        objpoints, imgpoints_left, imgpoints_right, mtxL, distL, mtxR, distR, img_shape, criteria=criteria_stereo, flags=flags)
    
    print(f"Terminooou! Erro RMS: {retStereo}")
    print("Vetor de translaçaõ entre a cam 1 e 2:\n", trans)
    print("Matrix rotação:\n", rot)
    
    # savlando ne
    np.savez("parametros_estereo.npz", mtxL=mtxL, distL=distL, mtxR=mtxR, distR=distR, R=rot, T=trans)
    print("Ta salvo no npz")

    # --- Ponto bonus fessor: triangulação no espaco ---
    print("\n[Bônus] tentanto fazer a triangulaçào de um uníco ponto...")
    
    # pra fzr iss a gnt precisa montar a matriz de projecao P1 e P2. 
    # como a Cam 1 eh o 0,0,0: P1 eh so a intrisec dela msm
    P1 = np.dot(mtxL, np.hstack((np.eye(3), np.zeros((3, 1))))) 
    
    # P2 leva a R e T q acamos de achar do estereo calibrate
    P2 = np.dot(mtxR, np.hstack((rot, trans)))
    
    # pegano o pixel da img esq e dir do primeiro ponto pra cruzar a reta
    pt1 = imgpoints_left[0][0].reshape(2, 1)
    pt2 = imgpoints_right[0][0].reshape(2, 1)
    
    # cv2 triangulate da na corrdena homogenea (w) 
    ponto_3d_homogeneo = cv2.triangulatePoints(P1, P2, pt1, pt2)
    
    # tem q diviir pelo W p ter x,y,z puro
    ponto_3d = ponto_3d_homogeneo[:3] / ponto_3d_homogeneo[3]
    
    print(f"Pixels do canto Esq/Dir: {pt1.ravel()} / {pt2.ravel()}")
    print(f"Se calculamo certo, ele ta nesse cm no mundo real (base cam1): {ponto_3d.ravel()}")

else:
    print("Ixi, nao rolou foto com tabuleiro nas duas juntas n.")
