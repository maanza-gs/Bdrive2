
from typing import Optional, List
from fastapi import Request


class RegistrationForm:
    
    def __init__(self,request:Request):
        self.request: Request=request
        self.errors: List=[]
        self.username:Optional[str]=None
        self.email:Optional[str]=None
        self.password:Optional[str]=None


    async def load_data(self):
        form=await self.request.form()
        self.username=form.get("username")
        self.email=form.get("email")
        self.password=form.get("password")

    async def is_valid(self):
        if not self.errors:
            return True
        return False
        
class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("email")  # since outh works on username field we are considering email as username
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
            
        if not self.errors:
            return True
        return False