from fastapi import (
    APIRouter,Depends,HTTPException,status
)
from service.auth_service import AuthService, UserAuthSchema ,LoginSchema
from config.configs import generate_seccion
from auth.jwt_bearer import JwtBearer

auth = APIRouter()

@auth.get("/email")
async def get_auth(seccion=Depends(generate_seccion),data=Depends(JwtBearer())):
    auth = AuthService(seccion).get_auth(data[0])
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auth is not in database"
        )
    return auth

@auth.post(path="/save",
           status_code=status.HTTP_201_CREATED
           )
async def save_auth(schema:UserAuthSchema,seccion=Depends(generate_seccion)):
    auth = AuthService(seccion).save_auth(schema)
    if type(auth) is str:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=auth
        )
    return auth

@auth.patch("/update")
async def update_auth(schema:LoginSchema,seccion=Depends(generate_seccion),data=Depends(JwtBearer())):
    schema.email = data[0]
    auth = AuthService(seccion).update_auth(schema)
    if type(auth) is str:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=auth
        )
    return auth

@auth.delete('/delete')
async def delete_auth(seccion=Depends(generate_seccion),data=Depends(JwtBearer())):
    auth = AuthService(seccion).delete_auth(data[0])
    if type(auth) is str:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=auth
        )
    return auth

#login

@auth.post(
    path="/login",
    tags=['Login']
    )
async def login_auth(schema:LoginSchema,seccion=Depends(generate_seccion)):
    auth = AuthService(seccion).login(schema)
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User o Password invalid"
        )
    return {'access_token':auth,'type_token':'bearer'}

    
    
