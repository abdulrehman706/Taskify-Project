Celery + Redis integration

Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run Redis (local):

```bash
redis-server
```

3. Start a Celery worker from project root:

```bash
export REDIS_URL=redis://localhost:6379/0
export CELERY_BACKEND=redis://localhost:6379/1
celery -A app.celery_app.celery_app worker --loglevel=info
```

4. Run the FastAPI app (example):

```bash
uvicorn app.main:app --reload
```

5. Trigger background job:
- Assign a task via the API: `PUT /tasks/{task_id}/assign` — this will enqueue `app.tasks.send_notification`.

Notes
- Configure `REDIS_URL` and `CELERY_BACKEND` via environment variables as needed.
- Celery tasks are defined in `app/tasks.py` and the Celery instance is in `app/celery_app.py`.
