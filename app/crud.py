from sqlalchemy.orm import Session
import secrets,os
from . import models, schemas   
from . hashing import Hash
from fastapi import Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer
import shutil


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def get_user(db: Session, user_id: int):
#   return db.query(models.User).filter(models.User.id == user_id).first()

# def rename(db: Session, oldname:str,newname:str):

#     new_user = models.User(username=user.username,email=user.email,password=Hash.bcrypt(user.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.email == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(username=user.username,email=user.email,password=Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_file_of_user(db: Session, email: str):
    user=db.query(models.File).filter(models.File.email == email).first()
    return db.query(models.File).filter(models.File.email == email).first()

def save_file(file_uploaded:UploadFile):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file_uploaded.filename)
    hashed_name=random_hex+f_ext
    file_location = os.path.join('D:/sem 8/Cloudwiry/bdrivestatic/',hashed_name)
    with open(file_location, "wb+") as buffer:
        shutil.copyfileobj(file_uploaded.file, buffer)
    return hashed_name
    # new_file = models.Blog(title=request.title, body=request.body,user_id=1)
    # db.add(new_file)



