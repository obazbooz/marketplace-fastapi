from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean


class DbAdvertisement(Base):
    __tablename__ = 'advertisement'
    title = Column(String)
    description = Column(String)
    category = Column(String)
    id = Column(Integer, primary_key=True,index=True)
    is_reserved = Column(Boolean)
    is_sold = Column(Boolean)
    owner_id = Column(Integer)
