import os
from backend.routes.user.data import LoginCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .models import User, Auth

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_login(login: LoginCredentials, db: Session) -> bool:
    auth = db.query(Auth).filter(Auth.user == login.username).first()
    if auth and pwd_context.verify(auth.salt + login.password, auth.hashed_password):
        return True
    return False


def check_user_exists(username: str, db: Session) -> bool:
    user = db.query(User).filter(User.user == username).first()
    return user is not None


def generate_salt() -> str:
    return os.urandom(16).hex()


def create_user(login: LoginCredentials, db: Session) -> bool:
    if not check_user_exists(login.username, db):
        salt = generate_salt()
        new_auth = Auth(
            user=login.username,
            hashed_password=pwd_context.hash(salt + login.password),
            salt=salt,
        )
        new_user = User(
            user=login.username,
            auth=[new_auth],
            profile_image_url=f"https://api.dicebear.com/7.x/lorelei/png?seed={login.username}",
        )
        db.add(new_user)
        db.commit()
        return True

    return False
