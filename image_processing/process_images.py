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
    
    try:
        image_base64 = image_json['imageBase64'].split(',')[1]
    except IndexError:
        image_base64 = image_json['imageBase64']
        
    decoded_image = base64.b64decode(image_base64)
    opened_image = Image.open(io.BytesIO(decoded_image))

    img = np.array(opened_image)
    if img.shape[-1] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    try:
        bounding_boxes = draw_boxes(img, items_to_process)
    except:
        print(e)
        raise Exception("Erro ao desenhar as caixas na imagem. " + 
                        "Verifique a resolução da imagem e as " +
                        "configurações dos itens a serem verificados.")
    
    try:
        cuts = make_cuts(img, items_to_process)
    except Exception as e:
        print(e)
        raise Exception("Erro ao cortar a imagem. " + 
                        "Verifique a resolução da imagem e as " + 
                        "configurações dos itens a serem verificados.")
    
    return {
        "boundingBoxes": bounding_boxes,
        "processedCuts": cuts,
    }


def draw_boxes(img, items_to_process):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    for item in items_to_process:
        Ymin = item['cut_config']['yx']
        Ymax = item['cut_config']['yy']
        Xmin = item['cut_config']['xx']
        Xmax = item['cut_config']['xy']
        cv2.rectangle(
            img_rgb,
            (Xmin, Ymin),
            (Xmin + (Xmax-Xmin), Ymin + (Ymax-Ymin)),
            (0, 255, 0),
            6
        )
        
    # plt.imshow(img_rgb)
    # plt.savefig('boxes.png')

    # cv2.imwrite('boxes.png', cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
    
    _, buffer = cv2.imencode('.png', img_rgb)
    img_rgb_base64 = 'data:image/png;base64,' + base64.b64encode(buffer).decode()

    return img_rgb_base64


def make_cuts(base, items_to_process:list):
    cuts = []

    for item in items_to_process:
        resize_factor = 0.05
        
        Ymin = item['cut_config']['yx']
        Ymax = item['cut_config']['yy']
        Xmin = item['cut_config']['xx']
        Xmax = item['cut_config']['xy']

        cut = base[Ymin:Ymax, Xmin:Xmax]
        original_height, original_width = cut.shape[:2]

        # Se o novo tamanho for menor que 0, vai arredondar para 0
        # Aumenta o resize_factor em 5% até conseguir cortar a imagem
        while True:
            try:
                new_size = (int(original_height * resize_factor), int(original_width * resize_factor))
                resized_cut = cv2.resize(cut, new_size)
                break
            except:
                resize_factor += 0.05
                continue
        
        resized_cut = cv2.cvtColor(resized_cut, cv2.COLOR_BGR2RGB)
        resized_cut = resized_cut / 255.0

        cuts.append(
            {
                "id": item['id'],
                "name": item['name'],
                "type": item['type'],
                "cut": resized_cut.tolist()
            }
        )

    return cuts