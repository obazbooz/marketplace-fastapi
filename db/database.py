from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#Database definition
SQLALCHEMY_DATABASE_URL = "sqlite:///./marketplace-fastapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# we will use the Base to create our models as with databases we have (important)
#schema - model - respose
# Base = declarative_base()
class Base(DeclarativeBase):
    pass
#this function to get the hall database
#so we can perform operations any way in our code
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
