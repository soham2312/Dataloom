from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from typing import Union
import jwt
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

dummy_data = {
    "username":"admin",
    "password":"admin"
}

SECRET_KEY = "cairocoders123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins=["http://localhost:3000"])

class Loginclass(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
def login(data: Loginclass):
    data = jsonable_encoder(data)
    if data['username'] == dummy_data['username'] and data['password'] == dummy_data['password']:
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return {"token": encoded_jwt, "status": "success"}
    else:
        return {"status": "failed", "message": "Login failed"}
