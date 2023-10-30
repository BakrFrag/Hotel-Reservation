from sqlalchemy import  Column, Integer, String , Enum , Float , Boolean
from app.db.database import Base 



class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String ,unique=True )
    price = Column(Float , nullable = False)
    type = Column(Enum("Single","Double","Suit",name="room_types"),nullable = False)
    in_service = Column(Boolean , default = True)
    