from os import path

import sqlalchemy
from sqlalchemy import create_engine #gbt added
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .models import Settings, Base

load_dotenv()

DB_NAME = 'DATABASE_NAME'
engine = create_engine(f'sqlite:///{DB_NAME}', echo=True) 

def create_database():
    if not path.exists("database/" + DB_NAME):
        engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
        Base.metadata.create_all(engine)
        
        with Session(engine) as session:
            default_settings = Settings()
            session.add(default_settings)
            session.commit()