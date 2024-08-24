import time
from typing import Dict
from api.celery_config import celery_app
from celery.result import AsyncResult
from image_processing.process_images import process_images
from api.celery_config import redis_client


process_images = celery_app.task(process_images)

@celery_app.task
def watch_process(task_id):
    while True:
        result = AsyncResult(task_id)

        if result.state in ['SUCCESS', 'FAILURE']:
            redis_client.set('image_processing', 'False')
            redis_client.set('image_processing_task', '')
            break