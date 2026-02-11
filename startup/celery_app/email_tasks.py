from startup.celery_app.celery_config import celery_app


@celery_app.task(name="startup.email.send_welcome")
def send_welcome_email(user_id: int, email: str):

    print(f"Sending welcome email to {email} (user {user_id})")
    return True
