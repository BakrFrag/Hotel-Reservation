from fastapi import Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer
from .jwt_token  import JWTToken 
from decouple import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
# Authentication dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        jwt = JWTToken()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except Exception as E:
        raise HTTPException(status_code=401, detail="Invalid token")

