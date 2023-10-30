from pydantic import BaseModel

class UserNameModel(BaseModel):
    """
    username only from user table
    """
    username: str 


class LoginUserModel(UserNameModel):
    """
    login user by username & password
    """
    password: str 


class RegisterUserModel(LoginUserModel):
    """
    add anther field for confirm password
    """
    confirm: str 

class FullUserModel(LoginUserModel):
    """
    all user model atributes 
    """
    id: int 

class ChangePasswordModel(BaseModel):
    """
    allow user to change password
    """
    password: str