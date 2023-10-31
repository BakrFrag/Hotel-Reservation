from fastapi import Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session
from app.db.dependancies import get_db
from app.schemas.reservation import InReservationModel , OutRservationModel
from app.services import reservation
from typing import List 

router = APIRouter(
    prefix="/reservation",
    tags=["reservation"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.post("/add/",response_model=OutRservationModel)
def add_reservation(reservation_data:InReservationModel = Depends(reservation.validate_reservation), db:Session= Depends(get_db)) -> OutRservationModel:
    """
    add new reservation object in database 
    """
    
    reservation_object = reservation.add_reservation(db , reservation_data)
    return reservation_object


@router.get("/all/",response_model = List[OutRservationModel])
def get_all_reservations(db:Session = Depends(get_db)) -> List[OutRservationModel]:
    """
    get all reservations
    """
    return reservation.get_all_reservations(db)


# @router.put("/{reservation_id}/", response_model = OutRservationModel)
# def update_reservation(reservation_id:int , reservation_data:InReservationModel , db:Session = Depends(get_db)):
#     """
#     update reservation data
#     """
#     reservation_by_id = reservation.get_reservation_by_id(db , reservation_id)
#     if not reservation_by_id:
#         raise HTTPException(status_code= 400 , detail = f"no reservation with id {reservation_id}")
    
#     reservation_code = reservation_data.code.lower()
#     if reservation.get_reservation_by_code(db , reservation_code):
#         raise HTTPException(status_code= 400 , detail = f"reservation with code {reservation_code} exists")

#     return reservation.update_reservation(db, reservation_id , reservation_data)

@router.delete("/{reservation_id}/")
def delete_reservation(reservation_id:int , db:Session = Depends(get_db)):
    """
    delete reservation
    """
    reservation_by_id = reservation.get_reservation_by_id(db , reservation_id)
    if not reservation_by_id:
        raise HTTPException(status_code= 400 , detail = f"no reservation with id {reservation_id}")

    reservation.delete_reservation(db , reservation_id)
    return {
        "message":"reservation removed successfully"
    }

@router.get("/{reservation_id}/", response_model= OutRservationModel)
def get_reservation_by_id(reservation_id : int , db:Session = Depends(get_db)):
    """
    get full reservation detail by id 
    """
    reservation_by_id = reservation.get_reservation_by_id(db , reservation_id)
    if not reservation_by_id:
        raise HTTPException(status_code= 400 , detail = "no reservation with parsed id")
    return reservation_by_id
