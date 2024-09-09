from fastapi import APIRouter, HTTPException
# from image_processing.utils import find_images
# from tasks.api_tasks import watch_process
from image_processing.process_images import process_images
# from api.celery_config import redis_client
from pydantic import BaseModel
from typing import Dict, List, Union

router = APIRouter()
# redis_client.set('image_processing', 'False')


class ImageReceived(BaseModel):
    dryerId: int
    dryerBaseSize:str
    imageBase64:str
    itemsToProcess: List[Dict[str, Union[str, int, Dict[str, Union[str, int]]]]]


@router.post("/process")
def start_process_images(image_received:ImageReceived):
    try:
        result = process_images(image_received.model_dump())
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
