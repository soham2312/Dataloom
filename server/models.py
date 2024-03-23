from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class File(BaseModel):
    username: str
    filename: str
    file_path: str

class Dataset(BaseModel):
    id: int
    name: str