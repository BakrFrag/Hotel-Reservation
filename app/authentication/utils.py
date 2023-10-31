from fastapi import Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer
from .jwt_token  import JWTToken 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        jwt = JWTToken()
        payload = jwt.verify_token(token)
        user_id = payload.get("user_id")
       
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except Exception as E:
       
        raise HTTPException(status_code=401, detail="Invalid token")

