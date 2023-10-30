from fastapi import Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session
from app.db.dependancies import get_db
from app.schemas.room import BasicRoomModel , FullRoomModel
from app.services import room
from typing import List 

router = APIRouter(
    prefix="/room",
    tags=["room"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.post("/add/",response_model=FullRoomModel)
def add_room(room_data:BasicRoomModel , db:Session= Depends(get_db)) -> FullRoomModel:
    """
    add new room object in database 
    """
    room_by_code = room.get_room_by_code(db , room_data.code.lower())
    if room_by_code:
        raise HTTPException(status_code = 400 , detail = "Room with this code exists")
    room_object = room.add_room(db , room_data)
    return room_object


@router.get("/all/",response_model = List[FullRoomModel])
def get_all_rooms(db:Session = Depends(get_db)) -> List[FullRoomModel]:
    """
    get all rooms
    """
    return room.get_all_rooms(db)


@router.put("/{room_id}/", response_model = FullRoomModel)
def update_room(room_id:int , room_data:BasicRoomModel , db:Session = Depends(get_db)):
    """
    update room data
    """
    room_by_id = room.get_room_by_id(db , room_id)
    if not room_by_id:
        raise HTTPException(status_code= 400 , detail = f"no room with id {room_id}")
    
    room_code = room_data.code.lower()
    if room.get_room_by_code(db , room_code):
        raise HTTPException(status_code= 400 , detail = f"room with code {room_code} exists")

    return room.update_room(db, room_id , room_data)

@router.delete("/{room_id}/")
def delete_room(room_id:int , db:Session = Depends(get_db)):
    """
    delete room
    """
    room_by_id = room.get_room_by_id(db , room_id)
    if not room_by_id:
        raise HTTPException(status_code= 400 , detail = f"no room with id {room_id}")

    room.delete_room(db , room_id)
    return {
        "message":"room removed successfully"
    }

@router.get("/{room_id}/", response_model= FullRoomModel)
def get_room_by_id(room_id : int , db:Session = Depends(get_db)):
    """
    get full room detail by id 
    """
    room_by_id = room.get_room_by_id(db , room_id)
    if not room_by_id:
        raise HTTPException(status_code= 400 , detail = "no room with parsed id")
    return room_by_id
