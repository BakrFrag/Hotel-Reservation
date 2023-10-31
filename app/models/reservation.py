from sqlalchemy import  Column, Integer,  Date,  ForeignKey
from app.db.database import Base 
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.hybrid import hybrid_property

class Reservation(Base):
    """
    reservation reprsents reservation entity
    """
    __tablename__ = "reservation"
    id = Column(Integer , index = True , primary_key = True )
    from_date = Column(Date) 
    to_date = Column(Date)
    room_id = Column(Integer, ForeignKey('room.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    room = relationship("Room", back_populates="reservations")
    user = relationship("User", back_populates="reservations")

    @hybrid_property
    def total_days(self):
        """
        calculate reservation number of days
        """
        return (self.to_date - self.from_date).days

    @hybrid_property
    def total_price(self):
        """
        calculate total reservation price
        """
        return self.room.price * self.total_days
    