import numpy as np
import cv2
import glob
import os

# config do tabuleiro 
num_intersecoes_y = 6
num_intersecoes_x = 9 # default do opencv eh 9x6
tamanho_quadrado_mm = 25.0 # arrumar isso aq pro tamanho em milimetros do tabuleiro q a gnt usou

#criterio de parada pro calculo subpixel p ajuda a ficar mais preciso)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# gera os pontos no 3d tipo (0,0,0), (1,0,0)...
# multiplicando dps pelo tamanho em mm pra ter o mundo real 
objp = np.zeros((num_intersecoes_x * num_intersecoes_y, 3), np.float32)
objp[:, :2] = np.mgrid[0:num_intersecoes_x, 0:num_intersecoes_y].T.reshape(-1, 2)
objp = objp * tamanho_quadrado_mm

#listas pra guardar tudo q achar nas fots
objpoints = [] #pontos no mundao 3d
imgpoints = [] #pontos 2d no plano da imgem

print("Iniciando processo de calibração... vamo q vamo")
images = glob.glob('imagens/*.jpg') # mudando pra pegar td jpg q tiver na pasta

if not images:
    print("Nenhuma imagem encontrada! Coloca as fotos na pasta 'imagens/' pelamor.")
    exit()

img_shape = None

for fname in images:
    print(f"Processando {fname}...")
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img_shape is None:
        img_shape = gray.shape[::-1]

    # fast check 
    flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
    ret, corners = cv2.findChessboardCorners(gray, (num_intersecoes_x, num_intersecoes_y), flags)

    # se achou os cantos,refinada neles e guarda
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        
        #dbug
        # cv2.drawChessboardCorners(img, (num_intersecoes_x, num_intersecoes_y), corners2, ret)
        # cv2.imshow('img', img)
        # cv2.waitKey(500)

cv2.destroyAllWindows()

if len(objpoints) > 0:
    print(f"Calibrando câmera com {len(objpoints)} imagens q deram certo...")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_shape, None, None)
    
    print("Calibração finalizada sucesso!")
    print("Matriz da câmera (Intrínseca):\n", mtx)
    print("Coeficientes da lente (distorção):\n", dist)
    
    # gravando as vars no arq
    np.savez("parametros_camera.npz", mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs, objpoints=objpoints, imgpoints=imgpoints)
    print("Parâmetros salvos em 'parametros_camera.npz'")
    
    #pegando a primeria img pra fzr o teste de undistort (tira aquela distorcao 
    img = cv2.imread(images[0])
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    # removendo a distorcao
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    
    #corta as bordas preta q sobram (depende do roi)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite('undistorted_result.jpg', dst)
    print("Imagem corrigida salva como 'undistorted_result.jpg' (da pra ver q desentortou)")
    
    #calculo do erro total de reprojeção
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        # re-modela (reshape) pra nao bugar no numpy 
        pts_originais = imgpoints[i].reshape(-1, 2)
        pts_projetados = imgpoints2.reshape(-1, 2)
        
        # dist euclidiana msm
        error = np.linalg.norm(pts_originais - pts_projetados, axis=1).mean()
        mean_error += error
    print(f"Erro médio de reprojeção: {mean_error/len(objpoints)}")
    
else:
    print("nao foi possivel achar as quinas em nenhuma das imagens")
