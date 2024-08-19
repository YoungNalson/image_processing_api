import time
from typing import Dict

# Dicionário para armazenar o estado do processo
process_states: Dict[str, bool] = {
    'image_processing': False
}


def define_bcg_task(func):
    async def wrapper(*args, **kwargs):
        process_states['image_processing'] = True
        await func(*args, **kwargs)
        process_states['image_processing'] = False
    return wrapper