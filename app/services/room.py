from sqlalchemy.orm import Session
from app.schemas.room import *
from app.models.room import Room 
from fastapi import  HTTPException
def get_room_by_id(db:Session , room_id:int) -> Room:
    """
    get room by id
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    return room 

def get_room_by_code(db:Session, code:str) -> Room:
    """
    get room by code
    """
    room = db.query(Room).filter(Room.code == code).first()
    return room 

def get_all_rooms(db:Session):
    """
    get list of all rooms
    """
    return db.query(Room).all()

def delete_room(db:Session , room_id:int) -> None:
    """
    delete room by id 
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if room is not None:
        return None 

    db.delete(room)
    db.commit()

def update_room(db:Session, room_id:int, room_data:BasicRoomModel) -> Room: 
    """
    update room by id
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    room.price = room_data.price 
    room.type = room_data.type 
    room.in_service = room_data.in_service
    room.code = room_data.code.lower()
    db.commit()
    db.refresh(room)
    return room

def add_room(db:Session , room_data:BasicRoomModel) -> Room:
    """
    add new room object 
    """
    room_data = room_data.dict()
    room_data["code"]=room_data["code"].lower()
    room = Room(**room_data)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def validate_room_data(room_data:BasicRoomModel):
    """
    validate parsed room data
    """
    room_price = room_data.price
    if room_price <=0:
        raise HTTPException(status_code = 400 , detail = "room price must be greater than 0")

    return room_data