import urllib.request
import os

# URLs das imagens de exemplo do OpenCV
urls = [
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left01.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left02.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left03.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left04.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left05.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left06.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left07.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left08.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left09.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left11.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left12.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left13.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/left14.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right01.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right02.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right03.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right04.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right05.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right06.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right07.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right08.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right09.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right11.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right12.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right13.jpg",
    "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/right14.jpg"
]

diretorio_imagens = "imagens"
os.makedirs(diretorio_imagens, exist_ok=True)

print("Baixando imagens de exemplo para calibração...")
for url in urls:
    nome_arquivo = os.path.join(diretorio_imagens, url.split("/")[-1])
    if not os.path.exists(nome_arquivo):
        try:
            print(f"Baixando {nome_arquivo}...")
            urllib.request.urlretrieve(url, nome_arquivo)
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")
    else:
        print(f"Arquivo {nome_arquivo} já existe.")
print("Download concluído! Você pode usar essas imagens se não tiver as suas.")
