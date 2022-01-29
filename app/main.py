from os import getcwd, remove
import os
from fastapi.responses import FileResponse,JSONResponse
from pathlib import Path
from typing import Optional
from typing import List
from datetime import datetime
from fastapi import FastAPI, File, UploadFile,Depends,HTTPException,status,Request,Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from .schemas import Item,User, UserCreate
from . import schemas, database, models, token,hashing, forms

from .database import SessionLocal, engine,get_db
from sqlalchemy.orm import Session
from .import crud,models,schemas,token

from fastapi.templating import Jinja2Templates


app = FastAPI()

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

models.Base.metadata.create_all(bind=engine)


#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/register",response_model=User)
async def create_user(request:Request):
    return templates.TemplateResponse('register.html', context={'request': request})


@app.post("/register",response_model=User)
async def create_user(request:Request,db: Session = Depends(get_db)):

    form = forms.RegistrationForm(request)
    await form.load_data()
        
    if await form.is_valid():
        user = UserCreate(username=form.username, email=form.email, password=form.password)

    db_email = crud.get_user_by_email(db, email=user.email)
    db_username=crud.get_user_by_username(db, username=user.username)

    if db_email :
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_username :
        raise HTTPException(status_code=400, detail="username already registered")

    crud.create_user(db=db, user=user)
    return templates.TemplateResponse("register.html", form.__dict__)


    


@app.post("/uploadfiles/")#,response_model=schemas.TokenData)
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

@app.get("/file",status_code=200)
def get_all(request:Request,db: Session = Depends(get_db)):
    #path='D:/sem 8/Hackathon/app/static/'
    files_of_user=[]
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = token.get_current_user_from_token(token=param, db=db)

    user = db.query(models.User).filter(models.User.email ==current_user.email).first()
    files = db.query(models.File).filter(models.File.user_id ==user.id)

    for file in files:
        files_of_user.append(file.owner)

    return templates.TemplateResponse("files.html", files=files_of_user)
    #FileResponse(path + name_file, media_type='application/octet-stream', filename=name_file)


@app.get("/download/{name_file}",status_code=200)
def download_file(name_file: str,db: Session = Depends(get_db), email: str = Depends(token.get_current_user)):
    path='D:/sem 8/Hackathon/app/static/'
    user = db.query(models.User).filter(models.User.email ==email).first()
    
    file = db.query(models.File).filter(models.File.user_id ==user.id).first()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="File not found")
    return FileResponse(path + name_file, media_type='application/octet-stream', filename=name_file)

@app.delete("/delete/{name_file}")
def delete_file(name_file: str,db: Session = Depends(get_db), email: str = Depends(token.get_current_user)):
    path='D:/sem 8/Hackathon/app/static/'
    user = db.query(models.User).filter(models.User.email ==email).first()
    try:
        file= db.query(models.File).filter(models.File.user_id ==user.id)
        file.delete(synchronize_session=False)
        db.commit()
        remove( path + name_file)

        return JSONResponse(content={
            "removed": True
            }, status_code=200)   
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "error_message": "File not found"
        }, status_code=404)


@app.get("/login",response_model=User)
def login(request:Request):
    print("loooooo")
    return templates.TemplateResponse('login.html', context={'request': request})

@app.post('/login',response_model=User)
async def login(request:Request, db: Session = Depends(database.get_db)):

    form = forms.LoginForm(request)
    
    await form.load_data()
    # print(form.password)
    # print(form.username)
    # print("sadsda")
    if await form.is_valid():
  
    #user = db.query(models.User).filter(models.User.email == request.email).first()
    #print(user.email)

        try:
            response = templates.TemplateResponse("login.html", form.__dict__)
            #print(response.body)
            token.login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
    #print("shdfljsdhf;i")
    return templates.TemplateResponse("login.html", form.__dict__)
    
    
    