import imp
from typing import Optional
from typing import List

from fastapi import FastAPI, File, UploadFile,Depends,HTTPException
from .schemas import Item,User, UserCreate

from .database import SessionLocal, engine,get_db
from sqlalchemy.orm import Session
from .import crud,models,schemas

app = FastAPI()
models.Base.metadata.create_all(bind=engine)



@app.post("/user/register",response_model=User)
async def create_item(user: UserCreate,db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
    


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile],db: Session = Depends(get_db)):
    
    return {"filenames": [file.filename for file in files]}
