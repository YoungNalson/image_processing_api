import cv2 as cv
import numpy as np

from utils import find_images


def main():
    images = find_images()
    results = process_images(images)
    
    for r in results:
        # print(f"Parte {r['parte']}: Resultado da análise = {r['resultado']}")
        print(type(r))


# Função principal de processamento de imagens
def process_images(images_paths, num_linhas=2, num_colunas=2):
    """
    Processa a imagem carregada, dividindo-a em partes e analisando cada parte.
    
    :param images_path: Lista de caminhos das imagens a serem processadas.
    :param num_linhas: Número de linhas para dividir a imagem.
    :param num_colunas: Número de colunas para dividir a imagem.
    :return: Resultados da análise de cada parte da imagem.
    """
    if not images_paths:
        raise ValueError("Imagem não encontrada ou caminho inválido.")
    
    # Carregar as imagens
    processed_images = []
    for path in images_paths:
        img = cv.imread(path)
        pre_processed_img = pre_process_image(img)
        
        contours, _ = cv.findContours(
            pre_processed_img, 
            cv.RETR_LIST, 
            cv.CHAIN_APPROX_SIMPLE
        )
        contours_array = np.array(contours, dtype=object)
        
        processed_images.append(contours)
    
    # Dividir a imagem em partes
    # divided_images = divide_images(images, num_linhas, num_colunas)
    
    # Analisar cada parte da imagem
    # results = []

    # for image_nuber, parts in enumerate(divided_images):
    #     for i, part in enumerate(parts):
    #         result = analise_part(part)
    #         results.append({
    #             "imagem": image_nuber + 1,
    #             "parte": i + 1,
    #             "resultado": result
    #         })
    
    return processed_images


def pre_process_image(img):
    width = int(img.shape[1] * 0.4)
    height = int(img.shape[0] * 0.4)
    dimensions = (width, height)
    rs_img = cv.resize(img, dimensions, cv.INTER_AREA)
    # cv.imshow('Secador', rs_img)

    # blank = np.zeros(rs_img.shape, dtype='uint8')
    gray = cv.cvtColor(rs_img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 70, 200, cv.THRESH_BINARY)
    # canny = cv.Canny(gray, 110, 175)
    
    # cv.imshow('Thresh', thresh)
    # contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # cv.drawContours(blank, contours, -1, (0, 0, 255), 1)
    # cv.imshow('Contornos', blank)
    # cv.waitKey(0)

    return thresh


# Função para dividir a imagem em várias partes
def divide_images(images, num_linhas, num_colunas):
    """
    Divide as imagens em partes menores.
    
    :param images: Imagens carregada pelo OpenCV.
    :param num_linhas: Número de linhas de divisão.
    :param num_colunas: Número de colunas de divisão.
    :return: Lista de partes da imagem.
    """
    divided_images = []

    for image in images:
        altura, largura, _ = image.shape
        altura_parte = altura // num_linhas
        largura_parte = largura // num_colunas
        
        parts = []
        for i in range(num_linhas):
            for j in range(num_colunas):
                parte = image[i*altura_parte:(i+1)*altura_parte, j*largura_parte:(j+1)*largura_parte]
                parts.append(parte)
        
        divided_images.append(parts)
    
    return divided_images


# Função para analisar uma parte da imagem (exemplo básico)
def analise_part(part):
    """
    Realiza uma análise simples em uma parte da imagem.
    
    :param part: Parte da imagem a ser analisada.
    :return: Resultado da análise (ex: média dos pixels).
    """
    # Exemplo: calcular a média dos valores dos pixels
    media = np.mean(part)
    return media


# Exemplo de uso
if __name__ == "__main__":
    main()