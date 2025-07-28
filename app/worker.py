# app/worker.py
from celery import Celery
import os

# Use in-memory broker for development (no Redis required)
celery_app = Celery(
    "smartcloud",
    broker="memory://",
    backend="rpc://"
)

celery_app.autodiscover_tasks(["app.tasks"])

# Optional: Configure Celery to handle connection errors gracefully
celery_app.conf.update(
    task_always_eager=False,  # Set to True for synchronous execution (no broker needed)
    task_eager_propagates=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=True,
)
