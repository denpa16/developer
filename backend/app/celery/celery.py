from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)
celery_app.autodiscover_tasks()
celery_app.conf.beat_schedule = {}

if __name__ == "__main__":
    celery_app.start()
