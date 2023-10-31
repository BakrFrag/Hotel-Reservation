from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base 
from sqlalchemy.orm import  relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True )
    password = Column(String)
    
    reservations = relationship("Reservation",back_populates="user")