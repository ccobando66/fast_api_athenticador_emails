from .crud_base import CrudBase
from models.model import User
from schema.schemas import UserSchema

class UserService(CrudBase):
    def __init__(self, seccion) -> None:
        super().__init__(seccion)
    
    def get_user(self,value: any) -> User | None:
        return super().get_data(User, User.nickname, value)
    
    def save_user(self,schema: UserSchema) -> str | User :
        
        schema.nickname = schema.nickname.strip()
         
        if self.get_user(schema.nickname) is not None:
            return "User is exists in database"
            
        super().save_data(model=User,schema=schema.dict(exclude_unset=True))
        return self.get_user(schema.nickname)
    
    def update_user(self,schema:UserSchema) -> str | User:
        
        if self.get_user(schema.nickname) is None:
            return "User is not exists in database"
        
        super().update_data(model=User,
                            field=User.nickname,
                            value=schema.nickname,
                            schema=schema.dict(exclude_unset=True)
                            )
        
        return self.get_user(schema.nickname)
    
    