from sqlalchemy.orm import Session
from app.schemas.reservation import *
from app.models.reservation import Reservation

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

# def update_reservation(db:Session, reservation_id:int, Reservation_data:BasicReservationModel) -> Reservation: 
#     """
#     update Reservation by id
#     """
#     Reservation = db.query(Reservation).filter(Reservation.id == Reservation_id).first()
#     Reservation.price = Reservation_data.price 
#     Reservation.type = Reservation_data.type 
#     Reservation.in_service = Reservation_data.in_service
#     Reservation.code = Reservation_data.code.lower()
#     db.commit()
#     db.refresh(Reservation)
#     return Reservation

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
