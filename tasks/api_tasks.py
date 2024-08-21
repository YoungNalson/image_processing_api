import time
from typing import Dict
from api.celery_config import celery_app
from celery.result import AsyncResult
from image_processing.process_images import process_images


process_images = celery_app.task(process_images)

@celery_app.task
def watch_process(task_id, tasks_dict):
    while True:
        result = AsyncResult(task_id)

        if result.state in ['SUCCESS', 'FAILURE']:
            tasks_dict['image_processing'] = False
            tasks_dict['image_processing_task'] = ''
            break