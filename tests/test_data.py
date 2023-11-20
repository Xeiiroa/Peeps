from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker, Mapped, mapped_column, Session
from datetime import datetime
import os
#from database.data import data_commands as Data
import pytest
from database.data import data_commands as DATA


class Base(DeclarativeBase):
    pass

class Setup(Base):
    vidpath = str(os.path.dirname("Security-Camera"))
    
    __tablename__ = 'setngs'
    
    
    id: Mapped[int] = mapped_column(primary_key=True)
    video_save_path: Mapped[str] = mapped_column(String, server_default=vidpath + "/static")
    phone_number : Mapped[int] = mapped_column(nullable=True, server_default=None)   
    delay_time : Mapped[int] = mapped_column(default=120)
    
    

class TestSettings:
    def setup_class(self):
        Data=DATA()
        Base.metadata.create_all(engine)
        self.session = Session()
        self.valid_data = Setup(
            video_save_path = "SAD",
            phone_number= 1234567890,
            delay_time = 4
        )
    
    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    
    @pytest.mark.xfail(raises=ValueError)    
    def test_no_phone_number(self):
        setup = Setup(
            video_save_path = "SAD",
            delay_time = 4
        )
        self.session.add(setup)
        try:
            self.session.commit()
        except ValueError:
            self.session.rollback()
     
    @pytest.mark.xfail(raises=ValueError)    
    def test_no_vid_path(self):
        setup = Setup(
        video_save_path = "SAD",
        delay_time = 4
    )
        self.session.add(setup)
        try:
            self.session.commit()
        except ValueError:
            self.session.rollback()
    


engine = create_engine(f'sqlite:///test.db', echo=True)
Base.metadata.create_all(engine)
