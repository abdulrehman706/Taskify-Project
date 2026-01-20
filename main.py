from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

class Data(BaseModel):
    name:str

@app.post("/create/")
async def create(data: Data):
    return {"data":data}


@app.get("/test/")
async def read_test():
    return {"message": "Test endpoint is working!"}
