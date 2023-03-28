from models.model import UserAuth, User
from schema.schemas import UserAuthSchema,LoginSchema
from.crud_base import CrudBase
from passlib.hash import bcrypt
from datetime import datetime, timedelta
from auth.jwt_bearer import generate_token
from os import getenv
from fastapi.encoders import jsonable_encoder


class AuthService(CrudBase):
    def __init__(self, seccion) -> None:
        super().__init__(seccion)
    
    def get_auth(self,value: any) -> UserAuth | None:
        return super().get_data(UserAuth, UserAuth.email, value)
    
    def save_auth(self, schema: UserAuthSchema) -> UserAuth | None :
        if self.get_auth(schema.email.strip()) is not None:
            return "Auth is exists in database"
        
        schema.passwd = bcrypt.encrypt(schema.passwd.strip())
        super().save_data(UserAuth, schema.dict(exclude={'nickname'}))
        
        user = super().get_data(User,User.nickname,schema.nickname)
        
        
        if user is None:
            return "User is not exists in database"
        
        auth = self.get_auth(schema.email.strip())
        
        auth.user_id = user.id
        auth.user = user
        
        super().get_seccion.commit()
        
        return self.get_auth(schema.email.strip())
    
    def update_auth(self, schema:LoginSchema) -> UserAuth | None:
        
        if self.get_auth(schema.email) is None:
            return "Auth is exists in not database"
        
        
        if schema.passwd is not None:
            schema.passwd = bcrypt.encrypt(schema.passwd.strip())
            
        super().update_data(model=UserAuth,
                            field=UserAuth.email,
                            value=schema.email.strip(),
                            schema=schema.dict()
                            )
    
        return self.get_auth(schema.email)
    
    def delete_auth(self, email:str) -> str | UserAuth:
        auth = self.get_auth(email)
        if auth is None:
            return "Auth is exists in not database"
        
        super().delete_data(auth)
        return auth
    
    #login and generate token
    def login(self,schema:LoginSchema) -> None | str:
        
        is_auth_valid = self.get_auth(schema.email)
        
        if is_auth_valid is None or bcrypt.verify(schema.passwd.strip(),is_auth_valid.passwd) == False:
            return None
        
        if  is_auth_valid.expirate is None or datetime.now() >= is_auth_valid.expirate:
            is_auth_valid.expirate = datetime.isoformat(
            datetime.now() + timedelta(minutes=int(getenv('JWT_EXPIRATE')))
            )
        
            login = super().get_seccion.query(
                                            UserAuth.email,
                                            UserAuth.expirate,
                                            User.nickname
                                            ).join(
                                                User,User.id == UserAuth.user_id
                                            ).filter(
                                                UserAuth.email == schema.email
                                            ).first()
                                            
            token = generate_token(jsonable_encoder(login._asdict()))                     
            is_auth_valid.token = token
            super().get_seccion.commit()
            return token
        
        return is_auth_valid.token