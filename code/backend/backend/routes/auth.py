
from datetime import timedelta
from datetime import datetime
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from backend.config import Config
from jose import jwt, JWTError
from backend.routes.exception import JSONException
import uuid
from .user.data import LoginCredentials

SECRET_KEY =  "b821bcc3363eda4506ba5af73af81b5945069293a05e58a324ebfaa040d7a4f1" if Config()['secret_key']==None else Config()['secret_key']
ALGORITHM = "HS256"
#TODO da commentare se va bene
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
        data: dict = payload.get("sub")
        #TODO the schema should be insert in some other way 
        if not('guest' in data) or not ('username' in data):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return data

def decode_user_token(token:Annotated[dict, Depends(decode_access_token)]):
    if token['guest'] == True:
        raise JSONException(status_code=401, error={'message': 'this route is only for authenticated users'})
    return token

def create_guest_access_token(id: int):
    # TODO: the database should save that this guest connected
    return _create_access_token({"sub": {"username": id, 'guest':True}})

def create_login_access_token(login: LoginCredentials) -> str:
    # TODO: first make request to database to verify this.
    return  _create_access_token({"sub": {'username':login.username, "guest": False}},)
