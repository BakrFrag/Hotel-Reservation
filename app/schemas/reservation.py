from pydantic import BaseModel
from datetime import date 

class InReservationModel(BaseModel):
    """
    validate data aganist reservation model
    """
    user_id: int 
    room_id: int 
    from_date: date 
    to_date: date 

class OutRservationModel(InReservationModel):
    """
    for reservation model show 
    """
    id: int 
    total_days: int 
    total_price: float
   

