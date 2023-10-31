from sqlalchemy import  Column, Integer,  Date,  ForeignKey
from app.db.database import Base 
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.hybrid import hybrid_property

class Reservation(Base):
    """
    reservation reprsents reservation entity
    """
    id = Column(Integer , index = True , primary_key = True )
    from_date = Column(Date) 
    to_date = Column(Date)
    room = Column(Integer, ForeignKey('room.id'))
    user = Column(Integer, ForeignKey('user.id'))

    rooms = relationship("Rom", back_populates="rooms")
    users = relationship("User", back_populates="users")


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
    