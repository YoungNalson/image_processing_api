from fastapi import APIRouter, HTTPException
from image_processing.utils import find_images
from tasks.api_tasks import watch_process, process_images
from api.celery_config import redis_client

router = APIRouter()


@router.get("/process")
def start_process_images():
    image_processing = redis_client.get('image_processing')

    if image_processing and image_processing.decode('utf-8') == 'True':
        return {"status": "Process is already running"}

    try:
        images_paths = find_images()
        task = process_images.delay(images_paths)

        # Atualiza o estado no Redis
        redis_client.set('image_processing', 'True')
        redis_client.set('image_processing_task', task.id)
        
        watch_process.delay(task.id)
        
        return {"message": "Image processing started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
