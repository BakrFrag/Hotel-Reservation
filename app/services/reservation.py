from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException , Depends
from app.schemas.reservation import  InReservationModel
from app.models.reservation import Reservation
from app.services.room import get_room_by_id
from app.services.user import get_user_by_id
from app.db.dependancies import get_db
from sqlalchemy.orm import Session

def get_reservation_by_id(db:Session , reservation_id:int) -> Reservation:
    """
    get Reservation by id
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    return reservation 



def get_all_reservations(db:Session):
    """
    get list of all Reservations
    """
    return db.query(Reservation).all()

def delete_reservation(db:Session , reservation_id:int) -> None:
    """
    delete Reservation by id 
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if Reservation is not None:
        return None 

    db.delete(reservation)
    db.commit()



def add_reservation(db:Session , reservation_data:InReservationModel) -> Reservation:
    """
    add new Reservation object 
    """
    reservation_data = reservation_data.dict()
    reservation = Reservation(**reservation_data)
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def validate_reservation(reservation_data:InReservationModel , db:Session = Depends(get_db)):
    """
    validate aganist reservation data
    """
    room_id = reservation_data.room_id 
    user_id = reservation_data.user_id
    from_date = reservation_data.from_date
    to_date = reservation_data.to_date
    today_date = datetime.today().date()
    room = get_room_by_id(db , room_id)
    print("dates condition",(to_date - from_date).days)
    if not room:
        raise HTTPException(status_code = 400 , detail = "Invalid Room ID")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code = 400 , detail = "Invalid User ID")

    if ((from_date < today_date) or (to_date < today_date)):
        raise HTTPException(status_code = 400 , detail = "Dates mustn't be in past")
    if (to_date - from_date).days < 1:
        raise HTTPException(status_code = 400 , detail = "Minium 1 Day for Reservation")
    return reservation_data