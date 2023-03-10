from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
import os


if os.environ.get("EXTERNAL-IP"):
    IP = os.environ.get("EXTERNAL-IP")
    SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://root:toor@{IP}/sampledb"
    engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./server.db"
    engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    