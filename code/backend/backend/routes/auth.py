
from datetime import timedelta
from datetime import datetime
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from backend.config import Config
from jose import jwt, JWTError
from backend.routes.exception import JSONException

SECRET_KEY =  "b821bcc3363eda4506ba5af73af81b5945069293a05e58a324ebfaa040d7a4f1" if Config()['secret_key']==None else Config()['secret_key']
ALGORITHM = "HS256"
#TODO da commentare se va bene
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None)->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = JSONException(status_code=401, error={"message": "Could not validate credentials"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

