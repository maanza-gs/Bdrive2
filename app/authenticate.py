
# from bcrypt import re
# from fastapi import APIRouter, Depends, status, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from . import schemas, database, models, token,hashing

# from sqlalchemy.orm import Session
# router = APIRouter(tags=['Authentication'])

# @router.post('/login',response_model=schemas.Token)
# def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     print( request.username )
#     user = db.query(models.User).filter(models.User.email == request.username).first()
#     print(user)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Invalid Credentials")
#     if not hashing.Hash.verify(user.password, request.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Incorrect password")

#     access_token = token.create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}