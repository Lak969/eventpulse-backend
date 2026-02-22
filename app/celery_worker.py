from celery import Celery

celery_app = Celery(
    "eventpulse",
    broker = "redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

import app.tasks.order_tasks