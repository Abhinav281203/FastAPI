from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLBD = "sqlite:///./blog.db"

engine = create_engine(SQLBD, connect_args={"check_same_thread": False})

localsession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

base = declarative_base()
