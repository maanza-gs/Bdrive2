import os,shutil
from typing import Optional
from typing import List
from datetime import datetime
from fastapi import FastAPI, File, UploadFile,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import Item,User, UserCreate
from . import schemas, database, models, token,hashing

from .database import SessionLocal, engine,get_db
from sqlalchemy.orm import Session
from .import crud,models,schemas,token

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@app.post("/register",response_model=User)
async def create_item(user: UserCreate,db: Session = Depends(get_db)):
    db_email = crud.get_user_by_email(db, email=user.email)
    db_username=crud.get_user_by_username(db, username=user.username)

    if db_email :
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_username :
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)

    


@app.post("/uploadfiles/",response_model=schemas.TokenData)
async def create_upload_files(files: List[UploadFile]= File (...),db: Session = Depends(get_db), email: str = Depends(token.get_current_user)):
    #print(user.username)
    user = db.query(models.User).filter(models.User.email ==email).first()
    #print(user.username)
    
    for file in files:
        print(file.filename)
        
        file_location = os.path.join(f'D:/sem 8/Hackathon/app/static/{file.filename}')
        
        with open(file_location, "wb+") as buffer:
            content = await file.read()
            buffer.write(content)
            buffer.close()
        db_file = models.File(filename=file.filename,date_uploaded=str(datetime.utcnow()),user_id=user.id)
        db.add(db_file)
    
    db.commit()
    return user
    
    #return {"filenames": [file.filename for file in files]}
@app.post('/login',response_model=schemas.Token)
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    #print( request.username,"Fuck" )
    user = db.query(models.User).filter(models.User.email == request.username).first()
    #print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}