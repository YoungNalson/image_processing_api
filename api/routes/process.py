from fastapi import APIRouter, HTTPException
from image_processing.utils import find_images
from tasks.api_tasks import watch_process, process_images
from api.celery_config import redis_client
from pydantic import BaseModel
from typing import Dict

router = APIRouter()
redis_client.set('image_processing', 'False')


class ImageReceived(BaseModel):
    id: int
    base64:str
    cut_config: Dict[Dict[str, str]]


@router.post("/process")
def start_process_images(image_received:ImageReceived):
    try:
        task = process_images.delay(image_received.model_dump())
        return {
            "msg": "Image processing started successfully.",
            "task_id": f"{task.id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
