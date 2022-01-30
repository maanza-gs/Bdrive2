import datetime 
from sqlalchemy import Column, ForeignKey, Integer,String
from .database import Base
from sqlalchemy.orm import relationship

class File(Base):
    __tablename__ ="files"
    id=Column(Integer,primary_key=True,index=True)
    filename=Column(String ,nullable=False)
    date_uploaded=Column(String,default=str(datetime.datetime.utcnow()))
    user_id=Column(Integer,ForeignKey("users.id"))
    #shared_to=Column(Integer)
    owner=relationship("User",back_populates="files")

class User(Base): 
    __tablename__ ="users"
    id=Column(Integer,primary_key=True,index=True)
    username = Column(String(20), unique=True, nullable=False)
    email =Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)

    
    files=relationship('File',back_populates="owner")