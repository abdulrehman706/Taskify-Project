from startup.celery_app.celery_config import celery_app


@celery_app.task(name="startup.notifications.send_notification")
def send_notification(task_id: int, message: str):
    print(f"Notification for task {task_id}: {message}")
    return {"task_id": task_id, "message": message}
