from os import getcwd, remove
import os
from traceback import print_tb
from pydantic import EmailStr
from fastapi.responses import FileResponse,JSONResponse
from pathlib import Path
from typing import Optional
from typing import List
from datetime import datetime
from fastapi import FastAPI, File, UploadFile,Depends,HTTPException,status,Request,Response,Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from .schemas import Item,User, UserCreate
from . import schemas, database, models, token,hashing, forms

from .database import SessionLocal, engine,get_db
from sqlalchemy.orm import Session
from .import crud,models,schemas,token

from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

loginPage = "login.html"
registerPage = "register.html"
homePage = "home.html"
errorMessage = "File not found."

app = FastAPI()

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

path='app/static/'
models.Base.metadata.create_all(bind=engine)

print(BASE_PATH)
print(os.getcwd())


@app.get("/")
async def home(request:Request):
    return templates.TemplateResponse(homePage, context={'request': request})


@app.post("/")
async def home(request:Request):
     return templates.TemplateResponse(homePage, context={'request': request})

@app.get("/register")
async def create_user(request:Request):
    return templates.TemplateResponse(registerPage, context={'request': request})


@app.post("/register")
async def create_user(request:Request,db: Session = Depends(get_db)):

    form = forms.RegistrationForm(request)
    await form.load_data()
        
    if await form.is_valid():
        user = UserCreate(username=form.username, email=form.email, password=form.password)

    db_email = crud.get_user_by_email(db, email=user.email)
    db_username=crud.get_user(db, username=user.username)

    if db_email :
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_username :
        raise HTTPException(status_code=400, detail="username already registered")

    crud.create_user(db=db, user=user)
    return templates.TemplateResponse(registerPage, form.__dict__)

@app.post("/share",status_code=200)
def share(request:Request,filename:str= Form(...),share:str= Form(...),db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(access_token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = token.get_current_user_from_token(token=param, db=db)
    if not current_user:
         return templates.TemplateResponse(loginPage,{"request": request})

    shared: User =crud.get_user_by_email(db,share)

    if not shared:
        return JSONResponse(content={
            "shared": False,
            "error_message": "Shared User not found!"
        }, status_code=500) 
        

    print("hiii")
    already_file=db.query(models.File).filter(models.File.user_id ==shared.id).filter(models.File.filename ==filename).first()
    
    if already_file:
        return JSONResponse(content={
            "renamed": False,
            "error_message": "Already file exist in shared user"
        }, status_code=500)
    
    db_update = db.query(models.File).filter(models.File.user_id ==current_user.id).filter(models.File.filename ==filename).first()
    db_update.shared_to=shared.email
    db.commit()

    db_file = models.File(filename=filename,date_uploaded=str(datetime.utcnow()),user_id=shared.id)
    db.add(db_file)
    db.commit()
    return JSONResponse(content={
            "shared": True,
            "message": "Shared Successfully"
        }, status_code=200)


@app.post("/upload",status_code=200)
def create_upload_files(request: Request,myfiles: List[UploadFile]= File (...),db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")

    param = get_authorization_scheme_param(access_token)  # scheme will hold "Bearer" and param will hold actual token value
    user: User = token.get_current_user_from_token(token=param, db=db)
    if not user:
         return templates.TemplateResponse(loginPage,{"request": request})

    current_user = db.query(models.User).filter(models.User.email ==user.email).first()


    for file in myfiles:
        file_location = path+file.filename 
        
        with open(file_location, "wb+") as buffer:
            content = file.file.read()
            buffer.write(content)

        db_file = models.File(filename=file.filename,date_uploaded=str(datetime.utcnow()),user_id=current_user.id)
        db.add(db_file)
    db.commit()
    return JSONResponse(content={
            "uploaded": True,
            "message": "Uploaded Successfully"
        }, status_code=200)
    
    

@app.get("/files",status_code=200)
def get_all(request: Request, db: Session = Depends(get_db)):
    
    data=[]
    access_token = request.cookies.get("access_token")
    print("token: ", access_token)
    scheme, param = get_authorization_scheme_param(access_token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = token.get_current_user_from_token(token=param, db=db)
    print(current_user.username)
    if not current_user:
         return templates.TemplateResponse(loginPage,{"request": request})

    user = db.query(models.User).filter(models.User.email ==current_user.email).first()
    files = db.query(models.File).filter(models.File.user_id ==user.id)

    for file in files:
        data.append(file)
    return templates.TemplateResponse("files.html", {"request": request,"data":data})


@app.post("/files",status_code=200)
def get_all(request:Request,db: Session = Depends(get_db)):
    data=[]
    access_token = request.cookies.get("access_token")

    scheme, param = get_authorization_scheme_param(access_token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = token.get_current_user_from_token(token=param, db=db)
    if not current_user:
         return templates.TemplateResponse(loginPage,{"request": request})

    user = db.query(models.User).filter(models.User.email ==current_user.email).first()
    files = db.query(models.File).filter(models.File.user_id ==user.id)

    for file in files:
        data.append(file)

    return templates.TemplateResponse("files.html", {"request":Request,"data":data})


@app.post("/rename",status_code=200)#not yet deleted the old file entry
def rename_file(request:Request,db: Session = Depends(get_db),oldname:str= Form(...),newname:str= Form(...)):

    print(newname)
    access_token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(access_token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = token.get_current_user_from_token(token=param, db=db)
    if not current_user:
         return templates.TemplateResponse(loginPage,{"request": request})

    print("current_user_id ",current_user.id)

    file = db.query(models.File).filter(models.File.user_id == current_user.id ).filter(models.File.filename ==oldname ).first()
    already_file=db.query(models.File).filter(models.File.user_id == current_user.id).filter(models.File.filename ==newname).first()

    print(file)
    print(already_file)
    

    extention = newname.split(".")[1]
    old_extention= oldname.split(".")[1]

    if old_extention != extention:
        return JSONResponse(content={
            "removed": False,
            "error_message": "Not valid Extention"
        }, status_code=500)
    if already_file:
        return JSONResponse(content={
            "renamed": False,
            "error_message": "Already file exist in Rename"
        }, status_code=500)

    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=errorMessage)

    os.rename(path+oldname,path+newname)

    file.filename=newname
    db.add(file)
    db.commit()

    return JSONResponse(content={
            "reNamed": True
            }, status_code=200) 
    


@app.post("/download",status_code=200)
def download_file(request:Request,filename:str= Form(...),db: Session = Depends(get_db)):

    access_token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(access_token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = token.get_current_user_from_token(token=param, db=db)
    if not current_user:
         return templates.TemplateResponse(loginPage,{"request": request})

    user = db.query(models.User).filter(models.User.email ==current_user.email).first()
    file = db.query(models.File).filter(models.File.user_id ==user.id).first()

    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=errorMessage)
    return FileResponse(path + filename, media_type='application/octet-stream', filename=filename)



@app.post("/delete")
def delete_file(request:Request,db: Session = Depends(get_db),filename:str= Form(...)):
    
    access_token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(access_token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = token.get_current_user_from_token(token=param, db=db)
    if not current_user:
         return templates.TemplateResponse(loginPage,{"request": request})

    user = db.query(models.User).filter(models.User.email ==current_user.email).first()
    try:
        db.query(models.File).filter(models.File.user_id ==user.id).filter(models.File.filename ==filename).delete()
        db.commit()
        
        remove( path + filename)

        return JSONResponse(content={
            "removed": True
            }, status_code=200)   
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "error_message": errorMessage
        }, status_code=404)


@app.get("/login",response_model=User)
def login(request:Request):
    return templates.TemplateResponse('login.html', context={'request': request})

@app.post('/login',response_model=User)
async def login(request:Request, db: Session = Depends(database.get_db)):

    form = forms.LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = templates.TemplateResponse(loginPage, form.__dict__)
            token.login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
    return templates.TemplateResponse(loginPage, form.__dict__)
    
@app.post("/logout")
def logout(request:Request , response:Response):
    response=templates.TemplateResponse(homePage,{"request": request})
    response.delete_cookie("access_token")
    return response