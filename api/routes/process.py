from fastapi import APIRouter, HTTPException, BackgroundTasks
from image_processing.process_images import process_images
from image_processing.utils import find_images
from tasks.api_tasks import process_states

router = APIRouter()

@router.get("/process")
async def start_process_images(background_tasks: BackgroundTasks):
    if process_states['image_processing']:
        return {"status": "Process is already running"}

    try:
        images_paths = find_images()
        process_images(images_paths)
        background_tasks.add_task(process_images, images_paths)
        return {"message": "Image processing started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
