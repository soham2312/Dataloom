from fastapi import FastAPI, HTTPException, Depends,UploadFile, File, Form,Request
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from typing import List
import jwt
import pandas as pd
from fastapi.responses import JSONResponse
from database import *
from models import *
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

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Check if the user exists in the mock database (replace with your actual user database logic)
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except :
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/token")
async def login_for_access_token(user: User):
    db_user = get_user(user.username)
    if db_user and db_user["password"] == user.password:
        token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.post("/login")
def login(data: User):
    db_user = get_user(data.username)
    print(db_user)
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

UPLOAD_DIR = "uploads"


@app.post("/upload")
async def upload_file(request:Request, file: UploadFile = Form(...)):
    # Create directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    # Save the uploaded file
    headers = dict(request.headers)
    authorization = headers.get("authorization")
    user=verify_token(authorization)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    # Save file details to database
    add_file({"username": user['username'], "filename": file.filename, "file_path": file_path})
    return {"message":"success"}

@app.get("/mydatasets")
async def get_my_datasets(token: str = Depends(oauth2_scheme)):
    # Verify the token and extract user information
    user = verify_token(token)
    if not user:
        return {"message": "Invalid token"}
    # Get datasets associated with the user (assuming get_files returns a list of datasets)
    datasets = get_files(user['username'])
    print("ubrwjbere")
    print(datasets)
    return {"msg": "success", "datasets": datasets}

