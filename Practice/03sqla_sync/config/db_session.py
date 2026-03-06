import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker

from pathlib import Path

from typing import Optional 

from sqlalchemy.orm import Session

from sqlalchemy.future.engine import Engine

from models.model_base import ModelBase

__engine: Optional[Engine] = None


def create_engine(sqlite: bool = False)->Engine:
    """"
    Función para configurar la conexión a un banco de datos
    """
    global __engine
    
    if __engine:
        return 
    
    if sqlite:
    
        archivo_db = 'db/picoles.sqlite'
        folder = Path(archivo_db).parent
        folder.mkdir(parents=True,exist_ok= True)
        
        conn_str = f'sqlite:///{archivo_db}'
        __engine = sa.create_engine(url=conn_str, echo=False, connect_args={"check_same_thread":False})
    else:
        conn_str = "postgresql://geek:university@localhost:5432/picoles"
        __engine = sa.create_engine(url=conn_str, echo=False)
        
    return __engine

def create_session()->Session:
    """
    Función para crear la sesión de conexión a un banco de datos
    """
    global __engine
    
    if not __engine:
        create_engine() # create_engine(sqlite=True)
    
    __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)
    
    session:Session = __session()
    
    return session


def create_tables()->None:
    global __engine 
    
    if not __engine:
        create_engine()
    
    import models.__all_models
    
    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)


