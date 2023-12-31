from fastapi import Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session
from app.db.dependancies import get_db
from app.schemas.user import LoginUserModel , RegisterUserModel , FullUserModel
from app.services import user
from app.authentication.jwt_token import JWTToken
router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add/",response_model=FullUserModel)
def add_user(user_data:RegisterUserModel , db: Session = Depends(get_db)) -> FullUserModel:
    """
    add new user
    """
    user_exits = user.get_user_by_username(db , user_data.username.lower())
    if user_exits:
        raise HTTPException(status_code=400, detail="Username already registered")
    elif user_data.password != user_data.confirm:
        raise HTTPException(status_code=400 , detail="parsed password & confirmed password don't match ")

    hashed_password = user.get_hashed_password(user_data.password).decode("utf-8")
    user_data = LoginUserModel(
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
    user_by_id = user.get_user_by_id(db , user_id = user_id)
    if not user_by_id:
        raise HTTPException(status_code=400, detail=f"no user with id {user_id}")
    return user_by_id



    

@router.delete("/{user_id}/")
def delete_user(user_id:int, db:Session = Depends(get_db)):
    """
    delete user with id
    """
    user_by_id = user.get_user_by_id(db , user_id = user_id)
    if not user_by_id:
        raise HTTPException(status_code=400, detail=f"no user with id {user_id}")
    user.delete_user(db , user_id = user_id)
    return {"message":f"user with id {user_id} deleted"}



    
@router.post("/login/")
def login_user(login_data:LoginUserModel,db:Session = Depends(get_db)):
   
    username = login_data.username.lower()
    user_by_username = user.get_user_by_username(db , username=username)
    password = login_data.password
    
    if ((not user_by_username) or (not password)):
        raise HTTPException(status_code=400 , detail = "wrong username or password")

    password_check = user.check_hashed_password(password , user_by_username.password)
    if not password_check:
        raise HTTPException(status_code=400 , detail = "wrong username or password")
    jwt = JWTToken()
    token_response = jwt.token_response(user_by_username.id)
    return token_response