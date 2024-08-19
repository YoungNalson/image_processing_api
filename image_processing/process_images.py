import cv2 as cv
import numpy as np

from utils import find_images


def main():
    images = find_images()
    results = process_images(images)


# Função principal de processamento de imagens
def process_images(images_paths):
    """
    Processa a imagem carregada, dividindo-a em partes e analisando cada parte.
    
    :param images_path: Lista de caminhos das imagens a serem processadas.
    :return: As imagens processadas como um array numpy.
    """
    if not images_paths:
        raise ValueError("Imagem não encontrada ou caminho inválido.")
    
    # Carregar as imagens
    processed_images = []
    for path in images_paths:
        img = cv.imread(path)
        pre_processed_img = pre_process_image(img)
        
        processed_images.append(pre_processed_img)
    
    return processed_images


def pre_process_image(img):
    ## Analises a serem feitas:

    # Detecção de Componentes Específicos
    # Segmentação por Cor
    # Detecção de Textura
    # Reconhecimento de Padrões
    # Medidas de Dimensões
    
    # Detecção de Bordas e Linhas
    contours = find_contours(img)
    filtered_contours = filter_contours(contours)
    
    # Detecção de Objetos e Classificação
    # Análise de Formas e Estruturas


def find_contours(img):
    width = int(img.shape[1] * 0.4)
    height = int(img.shape[0] * 0.4)
    dimensions = (width, height)

    rs_img = cv.resize(img, dimensions, cv.INTER_AREA)
    # cv.imshow('Secador', rs_img)
    blank = np.zeros(rs_img.shape[:2], dtype='uint8')
    gray = cv.cvtColor(rs_img, cv.COLOR_BGR2GRAY)
    
    # cv.imshow('Secador', img)
    # blank = np.zeros(img.shape[:2], dtype='uint8')
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # cv.imshow('Cinza', gray)

    # blurred = cv.GaussianBlur(gray, (5, 5), 0)
    # cv.imshow('Borrado', blurred)

    edges = cv.Canny(gray, 100, 200)
    # cv.imshow('Pontas', edges)

    # dilated = cv.dilate(edges, None, iterations=1)
    # cv.imshow('Dilatado', dilated)

    # eroded = cv.erode(dilated, None, iterations=1)
    # cv.imshow('Erodido', eroded)

    # ret, thresh = cv.threshold(gray, 70, 200, cv.THRESH_BINARY)
    # canny = cv.Canny(gray, 110, 175)
    
    # cv.imshow('Thresh', thresh)
    contours, hierarchies = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(blank, contours, -1, (255), 1)
    # cv.imshow('Contornos', blank)

    sliced_contours = cv.bitwise_and(rs_img, rs_img, mask=blank)
    # cv.imshow('Fios', sliced_contours)
    # cv.waitKey(0)

    return sliced_contours


def filter_contours(contours):
    filtered_contours = []

    ## Implementar função para filtrar os contornos

    return filtered_contours if filtered_contours else contours


# Exemplo de uso
if __name__ == "__main__":
    main()