"""Celery worker entry point and task discovery."""

from celery import Celery

from app.core.config import settings

# Create Celery application
celery_app = Celery(
    "costintel",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.modules.ingestion.tasks",
        "app.modules.classification.tasks",
        "app.modules.decisions.tasks",
    ],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    result_expires=86400,  # Results expire after 24 hours
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "data-retention-cleanup": {
        "task": "app.modules.ingestion.tasks.cleanup_old_data",
        "schedule": 86400.0,  # Run daily
    },
}

if __name__ == "__main__":
    celery_app.start()
