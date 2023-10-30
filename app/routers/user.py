from fastapi import Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session
from app.db.dependancies import get_db
from app.schemas.user import UserModel , UserRegisterModel , FullUserModel
from app.services import user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add/",response_model=FullUserModel)
def add_user(user_data:UserRegisterModel , db: Session = Depends(get_db)) -> FullUserModel:
    """
    add new user
    """
    user = user.get_user_by_username(db , user_data.username.lower())
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    elif user_data.password != user_data.confirm:
        raise HTTPException(status_code=400 , detail="parsed password & confirmed password don't match ")

    hashed_password = user.get_hashed_password(user_data.password).decode("utf-8")
    user_data = UserModel(
            username = user_data.username.lower() , 
            password = hashed_password
    )
    return user.add_user(db,user_data)

    

    
    

@router.get("/all/", response_model=list[FullUserModel])
def get_users(db:Session = Depends(get_db)) -> FullUserModel:
    """
    get list of all users
    """
    
    users = user.get_users(db)
    return users
 
@router.get("/{user_id}/", response_model=FullUserModel)
def get_user_by_id(user_id:int , db:Session = Depends(get_db)) -> FullUserModel:
    """
    by id get user
    """
    user = user.get_user_by_id(db , user_id = user_id)
    if not user:
        raise HTTPException(status_code=400, detail=f"no user with id {user_id}")
    return user



    

@router.delete("/{user_id}/")
def delete_user(user_id:int, db:Session = Depends(get_db)):
    """
    delete user with id
    """
    user.delete_user(db , user_id = user_id)
    return {"message":f"user with id {user_id} deleted"}



    
