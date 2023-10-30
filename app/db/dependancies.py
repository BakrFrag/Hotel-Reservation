from .database import SessionLocal , engine
from app.models import user as user_model

#migrate User Table to Database
user_model.Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()