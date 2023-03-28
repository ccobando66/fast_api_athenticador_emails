from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from jwt import encode, decode
from os import getenv
from datetime import datetime

class JwtBearer(HTTPBearer):
    async def __call__(self, request:Request):
        auth = await super().__call__(request)
        data = decode_token(auth.credentials)
        if datetime.isoformat(datetime.now()) >= data['expirate']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token as expirated, i'm sorry"
            )
            
        return (data['email'],data['nickname'])
    
def generate_token(data: dict) -> str :
    return encode(data,getenv('JWT_KEY'),algorithm=getenv('JWT_ALGORITH'))

def decode_token(token:str) -> dict :
    return decode(token,getenv('JWT_KEY'),algorithms=[getenv('JWT_ALGORITH')])
        