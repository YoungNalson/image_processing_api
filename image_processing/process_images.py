import cv2
import numpy as np
# import matplotlib.pyplot as plt
# from copy import deepcopy
import base64
import io
import math
from PIL import Image


# Função principal de processamento de imagens
def process_images(image_json):
    """
    Processa a imagem carregada, dividindo-a em partes e analisando cada parte.
    
    :param images_path: Lista de caminhos das imagens a serem processadas.
    :return: As imagens processadas como um array numpy.
    """
    if not image_json:
        raise ValueError("Imagem não encontrada ou caminho inválido.")
    
    items_to_process = image_json['itemsToProcess']
    image_base64 = image_json['imageBase64'].split(',')[1]
    decoded_image = base64.b64decode(image_base64)
    opened_image = Image.open(io.BytesIO(decoded_image))

    img = np.array(opened_image)
    if img.shape[-1] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    base = crop_base(img)
    bounding_boxes = draw_boxes(base, items_to_process)
    cuts = make_cuts(base, items_to_process)
    return {
        "boundingBoxes": bounding_boxes,
        "processedCuts": cuts,
    }


def crop_base(img):
    # Imagem RGB
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Imagem HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    points = find_points(img_hsv)

    # draw_lines(img_rgb, points)
    # plt.imshow(img_rgb)
    # plt.savefig('cantosEncontrados.png')

    img_rotated = rotate_img(img, points)

    # plt.imshow(cv2.cvtColor(img_rotated, cv2.COLOR_BGR2RGB))
    # plt.savefig('imagemEndireitada.png')

    img_rotated_hsv = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2HSV)

    rotated_points = find_points(img_rotated_hsv, 'mask2.png')

    # Criar uma máscara para recortar a imagem
    pts = np.array(rotated_points, dtype=np.float32)
    rect = cv2.boundingRect(pts)
    x, y, w, h = rect
    cropped_image = img_rotated[y:y+h, x:x+w]

    # plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    # plt.savefig('imagemRecortada')
    
    # cv2.imwrite('imagemRecortada.png', cropped_image)
    
    return cropped_image


def find_points(
        img_hsv, 
        file_name:str='mask.png', 
        color_interval1:list=[160, 100, 100], 
        color_interval2:list=[180, 255, 255]
    ):
    # Definir o intervalo de cor
    lowerb = np.array(color_interval1)
    upperb = np.array(color_interval2)

    mask = cv2.inRange(img_hsv, lowerb, upperb)
    
    # plt.imshow(mask)
    # plt.savefig(file_name)

    # Encontrar contornos que correspondem à máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    points = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Filtrar contornos pequenos
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                points.append((cX, cY))
    
    # Verificar se encontrou quatro pontos
    if len(points) == 4:
        # Ordenar pontos para formar um retângulo
        points = sort_points(points)

    return points


def sort_points(points):
    sorted_points = []
    center_x = sum(p[0] for p in points) / len(points)
    center_y = sum(p[1] for p in points) / len(points)

    def angulo_em_relacao_ao_centro(point):
        return np.arctan2(point[1] - center_y, point[0] - center_x)

    points.sort(key=angulo_em_relacao_ao_centro)

    # Dividir em quadrantes para identificar os quatro pontos
    sorted_points = [
        min(points, key=lambda p: (p[0] + p[1])),  # superior esquerdo
        min(points, key=lambda p: (p[0] - p[1])),  # superior direito
        max(points, key=lambda p: (p[0] + p[1])),  # inferior direito
        max(points, key=lambda p: (p[0] - p[1]))   # inferior esquerdo
    ]

    return sorted_points


def draw_lines(img_rgb, points):
    for i in range(len(points)):
        cv2.line(img_rgb, points[i], points[(i+1) % 4], (0, 0, 255), 10)


def draw_boxes(img, items_to_process):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    for item in items_to_process:
        Ymin = item['cut_config']['yx']
        Ymax = item['cut_config']['yy']
        Xmin = item['cut_config']['xx']
        Xmax = item['cut_config']['xy']
        cv2.rectangle(
            img_rgb, # imagem
            (Xmin, Ymin), # ponto 1
            (Xmin + (Xmax-Xmin), Ymin + (Ymax-Ymin)), # ponto 2
            (0, 255, 0), # cor
            6 # espessura da linha
        )
        
        # plt.imshow(img_rgb)
        # plt.savefig('boxes.png')

    # cv2.imwrite('boxes.png', cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
    
    _, buffer = cv2.imencode('.png', img_rgb)
    img_rgb_base64 = 'data:image/png;base64,' + base64.b64encode(buffer).decode()
    
    return img_rgb_base64


def rotate_img(img, pontos):
    # Pontos da linha de baixo (inferior esquerda e inferior direita)
    ponto_inferior_esquerdo = pontos[1]
    ponto_inferior_direito = pontos[2]

    # Calcular o ângulo da linha em relação ao eixo horizontal
    delta_x = ponto_inferior_direito[0] - ponto_inferior_esquerdo[0]
    delta_y = ponto_inferior_direito[1] - ponto_inferior_esquerdo[1]
    angle = math.degrees(math.atan2(delta_y, delta_x))

    height, width = img.shape[:2]

    # Calcular a matriz de rotação
    center = (height // 2, width // 2)
    rotating_matriz = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Rotacionar a imagem
    img_rotated = cv2.warpAffine(img, rotating_matriz, (width, height))
    
    return img_rotated


def make_cuts(base, items_to_process:list):
    cuts = []

    for item in items_to_process:
        Ymin = item['cut_config']['yx']
        Ymax = item['cut_config']['yy']
        Xmin = item['cut_config']['xx']
        Xmax = item['cut_config']['xy']
        cut = base[Ymin:Ymax, Xmin:Xmax]
        # cv2.imwrite(item['name'] + '.png', cut)
        cut = cv2.cvtColor(cut, cv2.COLOR_BGR2RGB)
        
        # plt.imshow(cut)
        # plt.savefig('chaveTemperatura.png')
        
        cut = cut / 255.0

        cuts.append(
            {
                "name": item['name'],
                "type": item['type'],
                "cut": base64.b64encode(cut.tobytes()).decode()
            }
        )

    return cuts