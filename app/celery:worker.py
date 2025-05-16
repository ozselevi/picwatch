from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",    # Kubernetesben, ha localhostban akkor 'redis://localhost:6379/0'
    backend="redis://redis:6379/0"
)

@celery_app.task
def test_task(message):
    print(f"Celery task received message: {message}")
    return f"Processed message: {message}"
