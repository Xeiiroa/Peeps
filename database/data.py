import re
import logging

from sqlalchemy import select, Text, update, MetaData, Table, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from . import engine
from .models import Settings


class data_commands:
    def __init__(self):
        pass
    
    #* Prints the name of all functions in this class in a readable string format
    def help(self):
        functions_list = [name for name in dir(self) if callable(getattr(self, name))]
        functions = ""
        for function in functions_list:
            functions += f"{function}\n"
        return functions
        
    #*query the database to get the current set video save path
    def get_video_save_path(self):
        with Session(engine) as session:
            try:
                settings_row = session.scalar(select(Settings))
                return settings_row.video_save_path
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when trying to get video save path: {str(e)}")
                
    #*query the database to get the current Phone number
    def get_phone_number(self):
        with Session(engine) as session:
            try:
                settings_row = session.scalar(select(Settings))
                return settings_row.phone_number
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when trying to get phone number {str(e)}")
                
                
    #*gets set delay time from database
    def get_delay(self):
        with Session(engine) as session:
            try:
                settings_row = session.scalar(select(Settings))
                return settings_row.delay_time
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when trying to get delay time{str(e)}")
                
    #*update the video save path in the database       
    #todo when this function is called open a window to choose file savepath
    def change_video_save_path(self, new_savepath:str):
        with Session(engine) as session:
            try:
                stmt = update(Settings).where(Settings.video_save_path.in_('user_settings'))
                stmt = stmt.values(video_save_path="new value")
                session.execute(stmt) #? pretty sure that execute is done automatically so subject to removal with comfirmation
                session.commit()

            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when trying to change video save path: {str(e)}")
                session.rollback()
                
    #*update the Phone number in the database
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

    
        
        
    #* changes the delay time    
    def change_delay(self, new_delay_time):
         with Session(engine) as session:
            try:
                stmt = update(Settings).where(Settings.delay_time.in_('user_settings'))
                stmt = stmt.values(delay_time=new_delay_time)
                session.execute(stmt) #? pretty sure that execute is done automatically so subject to removal with comfirmation
                session.commit()

            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when attempting to change delay time: {str(e)}")
                session.rollback()
                
  