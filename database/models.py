import os
import pathlib

from sqlalchemy import Column, String, Boolean, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



#might have to do db.Column

class Base(DeclarativeBase):
    pass


class Settings(Base):
    #todo Maybe : might have to insert a table that has all the data but might not have to
    vidpath = str(os.path.dirname("Security-Camera"))
    
    #table wasnt created
    
    __tablename__ = 'user_settings'
    
    #* created a id just to hold the primary key since the documentation says its needed can be removed if not actually needed
    id: Mapped[int] = mapped_column(primary_key=True)
    video_save_path: Mapped[str] = mapped_column(String, server_default=vidpath + "/static")
    phone_number : Mapped[int] = mapped_column(nullable=True, server_default=None)   
    delay_time : Mapped[int] = mapped_column(default=120)   
    