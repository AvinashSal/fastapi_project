from sqlalchemy import create_engine,Integer,String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session,sessionmaker
import os 
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


DB_url="postgresql://postgres:Password@localhost:5432/blogedb"
engine=create_engine(DB_url)

sessionlocal=sessionmaker(autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass


    

    
