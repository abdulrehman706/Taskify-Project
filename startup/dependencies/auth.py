from fastapi import Depends, HTTPException
from startup.database import get_db
from startup.repositories.user_repo import UserRepository


async def get_current_user(db=Depends(get_db)):
    user = UserRepository(db).get(1)
    if not user:
        raise HTTPException(status_code=401)
    return user
