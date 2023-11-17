from datetime import timedelta
from datetime import datetime
from logging import Logger
from typing import Annotated
from fastapi import Depends
from fastapi.security import APIKeyHeader, OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from backend.config import Config
from jose import jwt, JWTError
from backend.routes.exception import JSONException
import uuid
from .user.data import LoginCredentials

SECRET_KEY:str =  "b821bcc3363eda4506ba5af73af81b5945069293a05e58a324ebfaa040d7a4f1" if Config()['secret_key']==None else Config()['secret_key']
ALGORITHM = "HS256"
#TODO da commentare se va bene
ACCESS_TOKEN_EXPIRE_MINUTES = 90

oauth2_scheme = APIKeyHeader(name="Authorization", auto_error=False)

def _create_access_token(data: dict, expires_delta: timedelta | None = None)->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = JSONException(status_code=401, error={"message": "Could not validate jwt"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not('guest' in payload) or not ('sub' in payload):
            raise credentials_exception
        username: dict = payload.get("sub")
        guest: dict = payload.get("guest")
        # TODO the schema should be insert in some other way 
    except  JWTError :
        Logger('debug').error(f"Error decoding jwt, {JWTError}, {token} {SECRET_KEY}") 
        raise credentials_exception
    return {'username':username, 'guest': guest}

def decode_user_token(token: Annotated[dict, Depends(decode_access_token)]):
    if token['guest'] == True:
        raise JSONException(status_code=401, error={'message': 'this route is only for authenticated users'})
    return token

def create_guest_access_token(id: int):
    # TODO: the database should save that this guest connected
    return _create_access_token({"sub":  'guest-'+str(id), 'guest':True})

def create_login_access_token(login: LoginCredentials) -> str:
    # TODO: first make request to database to verify this.
    return  _create_access_token({"sub": login.username, "guest": False},)
