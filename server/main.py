from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
import jwt

from database import *
from models import User
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

SECRET_KEY = "cairocoders123456789"
ALGORITHM = "HS256"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins=["http://localhost:3000"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(user: User):
    db_user = get_user(user.username)
    if db_user and db_user["password"] == user.password:
        token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/")
def read_root(token: str = Depends(oauth2_scheme)):
    return {"Hello": "World"}

@app.post("/login")
def login(data: User):
    db_user = get_user(data.username)
    if db_user and db_user['password'] == data.password:
        encoded_jwt = jwt.encode({"sub": data.username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"status": "success","token":encoded_jwt}
    else:
        return {"status": "failed", "message": "Login failed"}
    
@app.post("/signup")
def signup(data: User):
    db_user = get_user(data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    create_user(data)
    return {"message": "User created successfully"}
