from celery import shared_task


@shared_task
def my_example_task():
    """Examle task."""
    return "HELLO!"
