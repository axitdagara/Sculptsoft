import os
from celery import Celery
from celery.schedules import crontab

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "lms",
    broker=redis_url,
    backend=redis_url,
    include=["config.library_tasks"]
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "check-overdue-daily": {
        "task": "config.library_tasks.send_overdue_notifications",
        "schedule": 86400.0, # Every 24 hours
    }
}