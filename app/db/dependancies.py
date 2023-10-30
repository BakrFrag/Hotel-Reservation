from .database import SessionLocal , engine
from app.models.user import User

#migrate User Table to Database
User.Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()