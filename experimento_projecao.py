import numpy as np
import cv2
import os

#carrega os paramentros calculados
try:
    dados = np.load("parametros_camera.npz")
    mtx = dados['mtx']
    dist = dados['dist']
    rvecs = dados['rvecs']
    tvecs = dados['tvecs']
    # bora pegar os pontos obj q foram usados e jogar dvolta na primeira imgem util q deu bom (index 0)
    objp_original = dados['objpoints'][0]
except FileNotFoundError:
    print("Vish: Arquivo 'parametros_camera.npz' nao ta aqui. Roda o 'calibrar_camera.py' primeiro vei.")
    exit()

print("Show, parametros carregados.")

# 

pontos_3d_eixo = np.float32([
    [0, 0, 0],       # aqui eh o (0,0,0) msm
    [75, 0, 0],      #ponta do eixo X (3 quadrados de tamanho)
    [0, 75, 0],      #eixo Y indo pra baxo no tabuleito
    [0, 0, -75]      # ixo Z "saindo" da tela/mesa apontando p cima pra dir da camera
])

#samos a transf da primeir imagem processada
img_index = 0
rvec = rvecs[img_index]
tvec = tvecs[img_index]

#projeta do mundo 3d devolta pro 2d do pixel
pontos_2d_projetados, jac = cv2.projectPoints(pontos_3d_eixo, rvec, tvec, mtx, dist)

# carregar a imagem
import glob
images = glob.glob('imagens/*.jpg')
if not images:
    print("kd as imagens?")
    exit()

img = cv2.imread(images[img_index])

# pega s pixel e  converte pra inteiro
p0 = tuple(map(int, pontos_2d_projetados[0].ravel()))
px = tuple(map(int, pontos_2d_projetados[1].ravel()))
py = tuple(map(int, pontos_2d_projetados[2].ravel()))
pz = tuple(map(int, pontos_2d_projetados[3].ravel()))

#desenhando as linhaz
#Vermelho p/ X, Verde p/ Y e Azul pro Z !!
cv2.line(img, p0, px, (0, 0, 255), 5)
cv2.line(img, p0, py, (0, 255, 0), 5)
cv2.line(img, p0, pz, (255, 0, 0), 5)

cv2.imwrite("projecao_3d_result.jpg", img)
print(f"ponto inicial 3D q a gnt mandou: {pontos_3d_eixo[0]}")
print(f"Pixel 2D q ele achou q eh: {pontos_2d_projetados[0].ravel()}")
print("Eixos desenhados na 'projecao_3d_result.jpg'")
