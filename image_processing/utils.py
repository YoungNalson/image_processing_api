import os

from dotenv import load_dotenv


load_dotenv()

def find_images():
    """
    Lista os caminhos dos arquivos de imagem em um diretório específico.
    
    :return: Lista de caminhos completos das imagens.
    """
    images_path = []
    directory = os.getenv('IMAGES_DIRECTORY')
    extensions=['.jpg', '.png', '.jpeg']
    
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                images_path.append(os.path.join(root, file))
    
    return images_path
