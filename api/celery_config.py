from celery import Celery
import redis

redis_client = redis.Redis(host='localhost')

# Configuração do Celery
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  # URL do broker Redis
    backend='redis://localhost:6379/0',  # URL do backend Redis
    include=['image_processing.process_images', 'tasks.api_tasks']
)

# Configurações adicionais, se necessário
# celery_app.conf.update(
#     task_routes={
#         'myapp.tasks.add': 'low-priority',
#     },
#     timezone='UTC',
# )

# from image_processing.process_images import process_images