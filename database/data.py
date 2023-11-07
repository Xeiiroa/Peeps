import re
import logging

from sqlalchemy import select, Text, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

from . import engine
from .models import Settings


class data_commands:
    def __init__(self):
        pass
    
    def help(self):
        functions = [name for name in dir(self) if callable(getattr(self, name))]
        
    #query the database to get the current set video save path
    def get_video_save_path(self):
        with Session(engine) as session:
            try:
                save_path = select(Settings).where(Settings.video_save_path.in_('user_settings'))
                return save_path
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured: {str(e)}")
                
    #query the database to get the current Phone number
    def get_phone_number(self):
        with Session(engine) as session:
            try:
                phone_number = select(Settings).where(Settings.phone_number.in_('user_settings'))
                return phone_number
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when trying to get phone number {str(e)}")
                
    #update the video save path in the database
    def change_video_save_path(self, new_savepath:str):
        with Session(engine) as session:
            try:
                stmt = update(Settings).where(Settings.video_save_path.in_('user_settings'))
                stmt = stmt.values(video_save_path="new value")
                session.execute(stmt) #? pretty sure that execute is done automatically so subject to removal with comfirmation
                session.commit()

            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured: {str(e)}")
                session.rollback()
                
    #update the Phone number in the database
    def change_phone_number(self,new_phone_number): #new email will be gotten from the settings form
        with Session(engine) as session:
            try: 
                if len(new_phone_number) == 0:
                    return None
                
                elif valid := re.fullmatch(r"^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$",new_phone_number):
                    stmt = update(Settings).where(Settings.phone_number.in_('user_settings'))
                
                    stmt = stmt.values(new_phone_number)
                    session.execute(stmt) #? pretty sure that execute is done automatically so subject to removal with comfirmation
                    session.commit()
                    
                    #return select info from database     
                else:
                    return False
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured in changing the user phone number: {str(e)}")
                session.rollback()
