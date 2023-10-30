from typing import Dict 
import jwt 
import time 
from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
 
class JWTToken(object):
    secret_key = SECRET_KEY
    algorithm = ALGORITHM
    
    def __init__(self):
        self.payload = {
            "user_id":None , 
            "expires": time.time() + 2400
        }

    def token_response(self,user_id:int) -> Dict[str,str]:
        """
        response access token
        """
        token = self.get_token(user_id)
        return { 
            "access":token
        }

    def get_token(self, user_id:int) -> str:
        """
        get jwt token 
        """
        self.payload["user_id"]=user_id
        token = jwt.encode(self.payload, self.secret_key, algorithm=self.algorithm)
        return token


    def verify_token(self , token:str) -> dict: 
        """
        verify token if it is still valid or not
        """
        
        decoded_token = jwt.decode(
            token, 
            self.secret_key, 
            algorithms=[self.algorithm])
        return decoded_token if decoded_token.get("expires") > time.time() else None
              