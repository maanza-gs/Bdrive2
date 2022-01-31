from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.hashing import Hash
from . import schemas,authenticate,crud,database

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, status,Response


oauth2_scheme = authenticate.OAuth2PasswordBearerWithCookie (tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email: str = payload.get("sub")
       
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        return email
    except JWTError:
        raise credentials_exception
    #return token_data


def get_current_user(data: str = Depends(oauth2_scheme)):
  
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(data, credentials_exception)


def get_current_user_from_token(token: str = Depends(oauth2_scheme),db: Session=Depends(database.get_db)): 
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        #print("username/email extracted is ",username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    #print("ggggggggg:",username)
    user = crud.get_user(db=db,username=username)
    if user is None:
        print("USER NOT IN DATABASE!!")
        raise credentials_exception
    return user

def authenticate_user(username: str, password: str,db: Session=Depends(database.get_db)):
    
    user = crud.get_user(db=db,username=username)
    #print(user.username)
    #print("fuck")
    if not user:
        return False
    if not Hash.verify(password, user.password):
        return False
    return user

def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):  #added response as a function parameter
    user = authenticate_user(form_data.username, form_data.password, db)
    #print("adgfdddddddddddddddddddddddddddddddddddddddddd")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True)  #set HttpOnly cookie in response
    return {"access_token": access_token, "token_type": "bearer"}

    