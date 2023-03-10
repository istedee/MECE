from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

try:
    # if using mysql  database
    SQLALCHEMY_DATABASE_URL = "sqlite:///./server.db"
    engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except exc.DatabaseError:
    SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://root:toor@127.0.0.1/sampledb"
    engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    