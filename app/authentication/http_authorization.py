from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from decouple import config
from .jwt_token import JWTToken

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
      
            if not credentials.scheme == config("KEY"):
                raise HTTPException(status_code=401, detail="Invalid authentication scheme.")

            if not self.verify_jwt(credentials.credentials):
              
                raise HTTPException(status_code=401, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid Authentication")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
                
                jwt = JWTToken()
                token_verification  = jwt.verify_token(jwtoken)
                return True if token_verification is not None else False 
                
        except Exception as E:
            
                return False
    