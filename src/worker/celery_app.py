# Location: /src/worker/celery_app.py
from celery import Celery
from src.core.config import settings

# Create the Celery instance
celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Tell Celery to find tasks in a file named 'tasks.py' inside 'src.worker'
celery_app.conf.imports = ("src.worker.tasks",)

import os
if os.getenv("CELERY_TASK_ALWAYS_EAGER", "False").lower() in ("true", "1"):
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True

print("--- Celery App Configured ---")