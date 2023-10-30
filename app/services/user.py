from sqlalchemy.orm import Session
from app.schemas.user import *
from app.models.user import User


def get_user_by_username(db:Session , username:str):
    """
    get user by username
    """
    return db.query(User).filter(User.username==username).first()

def get_user_by_id(db:Session , user_id:int):
    """
    get user by id
    """
    return db.query(User).filter(User.id==user_id).first()



def delete_user(db:Session , user_id:int):
    """
    delete user by id 
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()

def update_user(db: Session , user_id:int , new_user:ChangePasswordModel):
    """
    update user by id & new model 
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None 

    user.password = new_user.password
    db.commit()
    db.refresh(user)
    return user


def add_user(db:Session , new_user:RegisterUserModel):
    """
    create new user 
    """
    user = User(username = new_user.username , password = new_user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 
    

def get_users(db:Session):
    """
    get all users
    """
    return db.query(User).all()
