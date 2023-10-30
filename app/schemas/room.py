from pydantic import BaseModel 
from typing import Literal

class BasicRoomModel(BaseModel):
    price: float 
    code: str 
    type: Literal["Single","Double","Suit"]
    in_service: bool = True 
    #in_serivce
    

class FullRoomModel(BasicRoomModel):
    id: int 