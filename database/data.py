import re
import logging

from sqlalchemy import select, Text, update, MetaData, Table, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog


from . import engine
from .models import Settings


class data_commands:
    def __init__(self):
        pass
    
    #* Prints the name of all functions in this class in a readable string format
    def help(self):
        functions_list = [name for name in dir(self) if callable(getattr(self, name)) and not name.startswith("__")]
        functions = "\nList of commands: \n-------\n"
        for function in functions_list:
            if function == 'help':
                continue
            functions += f"{function}\n"
        print(functions)
        return functions
        
    #*query the database to get the current set video save path
    def get_video_save_path(self):
        with Session(engine) as session:
            try:
                settings_row = session.scalar(select(Settings))
                print(settings_row.video_save_path)
                return settings_row.video_save_path
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when trying to get video save path: {str(e)}")
                
    #*query the database to get the current Phone number
    def get_phone_number(self):
        with Session(engine) as session:
            try:
                settings_row = session.scalar(select(Settings))
                print(settings_row.phone_number)
                return settings_row.phone_number
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when trying to get phone number {str(e)}")
                
                
    #*gets set delay time from database
    def get_delay(self):
        with Session(engine) as session:
            try:
                settings_row = session.scalar(select(Settings))
                print(settings_row.delay_time)
                return settings_row.delay_time
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when trying to get delay time{str(e)}")
                
                
    #*update the video save path in the database       
    def change_video_save_path(self):
        with Session(engine) as session:
            try:
                new_savepath = filedialog.askdirectory(title="Select a folder")
                print(f"savepath updated to {new_savepath}")
                new_savepath == None
                if new_savepath == None:
                    return
                session.execute(update(Settings).values(video_save_path=new_savepath))
                session.commit()
            except SQLAlchemyError as e:
                logging.error(f"An SQL error has occured when trying to change video save path: {str(e)}")
                session.rollback()
                
    #*update the Phone number in the database
    def change_phone_number(self): 
        with Session(engine) as session:
            try: 
                while True:
                        new_phone_number = input("Phone number: ")
                        if len(new_phone_number) == 0:
                            return
                        elif valid := re.fullmatch(r"^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$",new_phone_number):
                            break
                        else:
                            print(f"{new_phone_number} is not a valid phone number")
                            continue
                
                new_phone_number.replace("-","")
                
                session.execute(update(Settings).values(phone_number=str(new_phone_number)))
                session.commit()
                return    
            except (SQLAlchemyError, KeyboardInterrupt) as e:
                logging.error(f"An error has occured in changing the user phone number: {str(e)}")
                session.rollback()

    #* changes the delay time    
    def change_delay(self):
         with Session(engine) as session:
            try:
                while True:
                    try:
                        new_delay_time = float(input("Delay Time: "))
                    except ValueError:
                        print("not a number")
                    else:
                        session.execute(update(Settings).values(delay_time=new_delay_time))
                        session.commit()
                        return
            except (SQLAlchemyError, ValueError) as e:
                logging.error(f"An error has occured when attempting to change delay time: {str(e)}")
                session.rollback()
                
  