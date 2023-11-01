from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException , Depends
from app.schemas.reservation import  InReservationModel
from app.models.reservation import Reservation
from app.models.room import Room
from app.models.room import Room
from app.services.room import get_room_by_id
from app.services.user import get_user_by_id
from app.db.dependancies import get_db
from app.authentication.utils import get_current_user
from sqlalchemy.orm import Session

def get_reservation_by_id(db:Session , reservation_id:int) -> Reservation:
    """
    get Reservation by id
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    return reservation 



def get_all_reservations(db:Session , user_id:int):
    """
    get list of all Reservations
    """
    return db.query(Reservation).filter(Reservation.user_id==user_id).all()

def delete_reservation(db:Session , reservation_id:int) -> None:
    """
    delete Reservation by id 
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if Reservation is not None:
        return None 

    db.delete(reservation)
    db.commit()



def add_reservation(db:Session ,user_id:int,  reservation_data:InReservationModel) -> Reservation:
    """
    add new Reservation object 
    """
    reservation_data = reservation_data.dict()
    reservation = Reservation(**reservation_data,user_id = user_id)
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation




def date_ranges_overlap(start_date1, end_date1, start_date2, end_date2):
    """
    check if two date ranges overlapped
    """
    return start_date1 <= end_date2 and start_date2 <= end_date1


def validate_reservation(reservation_data:InReservationModel , db:Session = Depends(get_db)):
    """
    validate aganist reservation data
    """
    room_id = reservation_data.room_id 
    from_date = reservation_data.from_date
    to_date = reservation_data.to_date
    today_date = datetime.today().date()
    room = get_room_by_id(db , room_id)
    
    if not room:
        raise HTTPException(status_code = 400 , detail = "Invalid Room ID")

    

    if ((from_date < today_date) or (to_date < today_date)):
        raise HTTPException(status_code = 400 , detail = "Dates mustn't be in past")
    if (to_date - from_date).days < 1:
        raise HTTPException(status_code = 400 , detail = "Minium 1 Day for Reservation")

    
    if not room.in_service:
               
       
        raise HTTPException(status_code=400 , detail = f"room {room_id} out of service")

    reservations = db.query(Reservation).join(Room).filter(
        Room.in_service== True , 
        Reservation.room_id == room_id
    ).all()
    
    if any(date_ranges_overlap(reservation.from_date , reservation.to_date , from_date , to_date) for reservation in reservations):
        raise HTTPException(status_code=400 , detail = f"room {room_id} has a reservation overlapped with desired reservation")
    return reservation_data


def check_rservation_can_be_deleted(reservation_id:int ,user_id:int=Depends(get_current_user),  db:Session = Depends(get_db)):
    """
    check against delete reservation 
    only before 2 days of start date [from_date]
    """
    reservation_by_id = get_reservation_by_id(db , reservation_id)
    if not reservation_by_id:
        raise HTTPException(status_code = 400 , detail = "invalid reservation id")
    
    if reservation_by_id.user_id != user_id:
        raise HTTPException(status_code= 403, detail = "Invalid access for resources")
    today_date = datetime.today().date()
    if not reservation_by_id:
        raise HTTPException(status_code= 400, detail = "Invalid Reservation ID")

    start_date = reservation_by_id.from_date 
    if (start_date - today_date).days < 2:
         
        raise HTTPException(status_code = 400 , detail = "Reservation Can't Be Cancelled")

    return reservation_id



