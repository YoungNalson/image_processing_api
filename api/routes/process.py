from fastapi import APIRouter, HTTPException
from image_processing.utils import find_images
from tasks.api_tasks import watch_process, process_images
from typing import Dict

router = APIRouter()

# Dicionário para armazenar o estado do processo
process_states: Dict[str, bool] = {
    'image_processing': False,
    'image_processing_task': ''
}


@router.get("/process")
def start_process_images():
    print(process_states['image_processing'])
    if process_states['image_processing']:
        return {"status": "Process is already running"}

    try:
        images_paths = find_images()
        task = process_images.delay(images_paths)

        process_states['image_processing'] = True
        process_states['image_processing_task'] = task.id
        
        watch_process.delay(task.id, process_states)
        
        return {"message": "Image processing started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
