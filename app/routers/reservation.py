from fastapi import Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session
from app.db.dependancies import get_db
from app.schemas.reservation import InReservationModel , OutRservationModel
from app.authentication.http_authorization import JWTBearer
from app.authentication.utils import get_current_user
from app.services import reservation
from typing import List 

router = APIRouter(
    prefix="/reservation",
    tags=["reservation"],
    dependencies=[Depends(get_db),Depends(JWTBearer())],
    responses={404: {"description": "Not found"}},
)

@router.post("/add/",response_model=OutRservationModel)
def add_reservation(reservation_data:InReservationModel = Depends(reservation.validate_reservation),user_id:int = Depends(get_current_user),db:Session= Depends(get_db)) -> OutRservationModel:
    """
    add new reservation object in database 
    """
    print("current user id:",user_id)
    reservation_object = reservation.add_reservation(db ,user_id = user_id ,  reservation_data = reservation_data)
    return reservation_object


@router.get("/all/",response_model = List[OutRservationModel])
def get_all_reservations(user_id:int=Depends(get_current_user),db:Session = Depends(get_db)):
    """
    get all reservations
    """
 
    return reservation.get_all_reservations(db , user_id = user_id)




@router.delete("/{reservation_id}/")
def delete_reservation(reservation_id:int = Depends(reservation.check_rservation_can_be_deleted) , db:Session = Depends(get_db)):
    """
    delete reservation
    """
    

    reservation.delete_reservation(db , reservation_id)
    return {
        "message":"reservation removed successfully"
    }

@router.get("/{reservation_id}/", response_model= OutRservationModel)
def get_reservation_by_id(reservation_id : int, user_id:int = Depends(get_current_user) , db:Session = Depends(get_db)):
    """
    get full reservation detail by id 
    """
    reservation_by_id = reservation.get_reservation_by_id(db , reservation_id)
    if not reservation_by_id:
        raise HTTPException(status_code= 400 , detail = "no reservation with parsed id")
    if reservation_by_id.user_id != user_id:
        raise HTTPException(status_code= 403, detail="Invalid access for resources")
    return reservation_by_id
