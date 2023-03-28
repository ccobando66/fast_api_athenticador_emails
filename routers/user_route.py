from fastapi import (
    APIRouter,Depends,HTTPException,status
)
from service.user_sevice import UserService,UserSchema 
from config.configs import generate_seccion
import uuid
from auth.jwt_bearer import JwtBearer

user = APIRouter()

@user.get("/whoaim")
async def get_user(seccion=Depends(generate_seccion),auth = Depends(JwtBearer())):
    return UserService(seccion=seccion).get_user(auth[1]) 

@user.post( 
           path="/save",
           status_code=status.HTTP_201_CREATED
           )
async def save_user(schema:UserSchema,seccion=Depends(generate_seccion)):
    schema.id = uuid.uuid4()
    user = UserService(seccion=seccion).save_user(schema)
    if type(user) is str:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=user
        )
    return user

@user.patch("/update")
async def update_user(schema:UserSchema,seccion=Depends(generate_seccion),auth = Depends(JwtBearer())):
    schema.nickname = auth[1]
    user = UserService(seccion=seccion).update_user(schema)
    if type(user) is str:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=user
        )
    return user

