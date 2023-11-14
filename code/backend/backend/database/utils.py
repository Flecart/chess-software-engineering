

from sqlalchemy import select
from backend.routes.user.data import LoginCredentials
from sqlalchemy.orm import Session
from .models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str)->str:
    return password
    #return pwd_context.hash(password) #TODO uncomment this line when the db is set up

# TODO temporaney to set up the db and show how it comunicate 
def check_login(login:LoginCredentials,db:Session)->bool:
    check_password = select(User).where(User.user == login.username,User.hashed_password==hash(login.password))
    result = db.execute(check_password)
    if result:
        return True
    return False

def check_user_exists(user:str,db:Session)->bool:
    check_password = select(User).where(User.user == user)
    result = db.execute(check_password)
    if result:
        return True
    return False


def create_user(login:LoginCredentials,db:Session)->bool:
    if not check_user_exists(login.username,db):
        new_user = User(user=login.username,hashed_password=hash(login.password),email="temp@temp.org",is_active=False)
        db.add(new_user)
        db.commit()
        return True
    return False

    

