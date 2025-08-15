from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    adv_posts = relationship('DbAdvertisement',back_populates='user')



class DbAdvertisement(Base):
    __tablename__ = 'advertisement'
    title = Column(String)
    description = Column(String)
    category = Column(String)
    is_reserved = Column(Boolean)
    is_sold = Column(Boolean)
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer,ForeignKey('users.id'))
    user = relationship("DbUser", back_populates='adv_posts')
