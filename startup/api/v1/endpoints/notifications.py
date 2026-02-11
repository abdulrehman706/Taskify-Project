from fastapi import APIRouter

router = APIRouter(prefix="/notifications")


@router.post("/send")
def send_notification():
    return {"status": "queued"}
