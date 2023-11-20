import os
import re
import logging

from sqlalchemy import select, Text, update, MetaData, Table, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from database import engine
from database.models import Settings


    
#! THE CODE WORKS BUT WHEN OPENING THE DATABASE IT ISNT UPDATING IN THERE
#! it even stays after running the program a second time    
    
    
    
with Session(engine) as session:
    try:
        session.execute(update(Settings).values(video_save_path="meth"))
        session.commit()
    except SQLAlchemyError as e:
        pass
    

with Session(engine) as session:
    try:
        settings_row = session.scalar(select(Settings))
        print(settings_row.video_save_path)
    except SQLAlchemyError as e:
        pass
    
    




