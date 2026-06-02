import os
from celery import Celery

# config de redis, por defecto local
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "rag_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.worker.tasks"] # Lo linkeamos con las tareas
)

# Config de la documentacion(revisar??)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_ack_late=True, # La tarea no se borra de la cola hasta acabar(comprobar si lastra la app)
    worker_prefetch_multiplier=1
)