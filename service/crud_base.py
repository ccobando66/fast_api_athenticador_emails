from sqlalchemy import Column


class CrudBase:
    def __init__(self, seccion) -> None:
        self.__seccion = seccion
    
    def get_data(self,model:object,field:Column,value:any):
        return self.__seccion.query(model).filter(field == value).first()
    
    def save_data(self,model:object, schema: dict):
        data = model(**schema)
        self.__seccion.add(data)
        self.__seccion.commit()
    
    def update_data(self,**kwargs):
        self.__seccion.query(kwargs['model']).filter(kwargs['field'] == kwargs['value']).update(kwargs['schema'])
        self.__seccion.commit()
    
    def delete_data(self,data: object):
        self.__seccion.delete(data)
        self.__seccion.commit()
        
    @property
    def get_seccion(self):
        return self.__seccion