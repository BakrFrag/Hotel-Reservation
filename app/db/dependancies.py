from .database import SessionLocal , engine
from app.models import user as user_model
from app.models import room as room_model
from app.models import reservation as reservation_model
#migrate User Table to Database
user_model.Base.metadata.create_all(bind=engine)
room_model.Base.metadata.create_all(bind=engine)
reservation_model.Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()