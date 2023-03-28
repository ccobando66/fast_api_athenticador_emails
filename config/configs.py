from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv



connect = create_engine(f"postgresql://{getenv('PSQL_USER')}:{getenv('PSQL_PASSWD')}@"
                        f"{getenv('PSQL_HOST')}/{getenv('PSQL_DB')}")

SqlBase = declarative_base()
Seccion = sessionmaker(bind=connect)


def generate_seccion():
    seccion = Seccion()
    try:
        yield seccion
    except:
        seccion.close()
    finally:
        seccion.close()