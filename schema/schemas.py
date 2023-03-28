from pydantic import BaseModel,Extra,EmailStr


class UserSchema(BaseModel, extra=Extra.allow):
    name : str | None
    subname: str | None
    nickname: str | None
    
    
    
   
class UserAuthSchema(BaseModel):
    email: EmailStr  | None
    passwd : str | None
    nickname: str 
    
    
    
    
class LoginSchema(BaseModel):
    email: EmailStr
    passwd : str 
    
    
    