from fastapi import APIRouter

router = APIRouter(prefix="/auth")


@router.post("/login")
def login():
    return {"access_token": "fake-token"}


@router.post("/register")
def register():
    return {"status": "registered"}
