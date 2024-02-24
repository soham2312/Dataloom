from fastapi import FastAPI, UploadFile,APIRouter,Depends
from fastapi.exceptions import HTTPException
from pathlib import Path
from database import *
from models import *

# Init App
UPLOAD_DIR=Path()/'uploads'
router = APIRouter()

# @router.post("/file/upload")
# async def upload_file(file: list[UploadFile]):
#     for files in file:
#         data=await files.read()
#         save_to=UPLOAD_DIR/files.filename
#         with open(save_to,'wb') as f:
#             f.write(data)
    
#     return {"filename":[f.filename for f in file]}

@router.post("/file/upload")
async def upload_file(file: UploadFile, current_user: User = Depends(get_user)):
    # Read file contents
    file_data = await file.read()
    # Upload file to database with the username of the current user
    upload_file_to_database(username=current_user.username, filename=file.filename, file_data=file_data)
    return {"message": "File uploaded successfully"}

# @app.post("/file/uploadndownload")
# def upload_n_downloadfile(file: UploadFile):
#     """Return a YAML FIle for the uploaded JSON File"""
#     if file.content_type != "application/json":
#         raise HTTPException(400,detail="Invalid document type")
#     else:
#         json_data = json.loads(file.file.read())
#         new_filename = "{}_{}.yaml".format(os.path.splitext(file.filename)[0],timestr)
#         # Write the data to a file
#         # Store the saved file
#         SAVE_FILE_PATH = os.path.join(UPLOAD_DIR,new_filename)
#         with open(SAVE_FILE_PATH,"w") as f:
#             yaml.dump(json_data,f)

#         # Return as a download
#         return FileResponse(path=SAVE_FILE_PATH,media_type="application/octet-stream",filename=new_filename)