from pydantic import BaseModel
from datetime import date 

class InReservationModel(BaseModel):
    """
    validate data aganist reservation model
    """
    room_id: int 
    from_date: date 
    to_date: date 


class OutRservationModel(InReservationModel):
    """
    for reservation model show 
    """
    id: int 
    user_id: int
    total_days: int 
    total_price: float
   

