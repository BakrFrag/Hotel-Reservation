from pydantic import BaseModel , Literal

class BasicRoomModel(BaseModel):
    price: float 
    code: str 
    type: Literal["Single","Double","Suit"]
    in_serivce: bool = True 