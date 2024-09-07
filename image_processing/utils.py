import os
import base64

from dotenv import load_dotenv


load_dotenv()

def find_images():
    """
    Lista os caminhos dos arquivos de imagem em um diretório específico.
    
    :return: Lista de caminhos completos das imagens.
    """
    images = []
    directory = os.getenv('IMAGES_DIRECTORY')
    extensions=['.jpg', '.png', '.jpeg']
    
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                with open(os.path.join(root, file), 'rb') as image:
                    image_bytes = image.read()
                    images.append(
                        'data:image/jpg;base64,' + base64.b64encode(image_bytes).decode()
                    )
    
    return images
