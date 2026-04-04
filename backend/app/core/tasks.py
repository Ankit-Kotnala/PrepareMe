from celery import Celery

from app.core.config import Settings, get_settings


def create_celery_app(settings: Settings) -> Celery:
    celery_app = Celery(
        "prepareme",
        broker=settings.celery_broker_url,
        backend=settings.celery_result_backend,
        include=[],
    )
    celery_app.conf.update(
        task_default_queue="prepareme.default",
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        task_track_started=True,
        broker_connection_retry_on_startup=True,
    )
    return celery_app


celery_app = create_celery_app(get_settings())

