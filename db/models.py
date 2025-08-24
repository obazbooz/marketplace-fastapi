from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float, DateTime, Numeric
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import func
from sqlalchemy import Enum as SAEnum
from enum import Enum
from sqlalchemy import UniqueConstraint , CheckConstraint

#Pydantic model.

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    rating_avg = Column(Float, nullable=True)
    rating_count = Column(Integer, nullable=True)
    adv_posts = relationship('DbAdvertisement',back_populates='owner')


class AdvStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"


class DbAdvertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    category = Column(String)
    status = Column(
        SAEnum(AdvStatus, name="adv_status"),
        nullable=False,
        default=AdvStatus.AVAILABLE,
        index=True,
    )

    owner = relationship("DbUser", back_populates='adv_posts')
    price = Column(Numeric(12, 2), nullable=True, index=True)   # not strictly required by the bullets
    location = Column(String(120), nullable=True, index=True)   # if you’ll ever filter by location

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    reserved_at = Column(DateTime(timezone=True), nullable=True)
    sold_at = Column(DateTime(timezone=True), nullable=True)



class DbMessage(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    advertisement_id = Column(Integer, ForeignKey("advertisement.id"))
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("DbUser",foreign_keys=[sender_id])
    receiver = relationship("DbUser",foreign_keys=[receiver_id])
    advertisement = relationship("DbAdvertisement")


class DbTransaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    advertisement_id = Column(Integer, ForeignKey("advertisement.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    advertisement = relationship("DbAdvertisement")
    buyer = relationship("DbUser", foreign_keys=[buyer_id])
    seller = relationship("DbUser", foreign_keys=[seller_id])


class RatingScore(int,Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class DbRating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    rater_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ratee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    transaction= relationship("DbTransaction")
    rater = relationship("DbUser",foreign_keys=[rater_id])
    ratee = relationship("DbUser",foreign_keys=[ratee_id])

    __table_args__ = (
        UniqueConstraint('transaction_id', 'rater_id', name='uq_rating_transaction_rater'),
        CheckConstraint('score BETWEEN 1 AND 5', name='ck_rating_score_range')
    )




