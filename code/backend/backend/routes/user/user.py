from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.config import Config
from backend.database.models import Game, User
from backend.routes.exception import JSONException
from backend.routes.user.data import LeaderBoardResponse, LoginCredentials 
from backend.database.database import get_db
from backend.database.utils import create_user, check_login
from ..auth import decode_access_token, create_guest_access_token, create_login_access_token, decode_user_token

def create_user_routes(app: FastAPI,prefix:str=''):
    prefix = f'{prefix}/user'

    @app.post(prefix+'/guest')
    def guest(db: Session=Depends(get_db)) -> str:
        """
        Login a user
        return a user id or a token we don't know yet
        """
        import random
        return create_guest_access_token(random.randint(0, 100000))

    @app.post(prefix + "/login")
    def login_api(login: LoginCredentials, db:Session=Depends(get_db)) -> str:
        """
        Login a user
        return a user id or a token we don't know yet
        """
        if check_login(login, db):
            return create_login_access_token(login)
        else:
            raise JSONException(status_code=400, error={"message": "User or password wrong"})


    @app.post(prefix + "/signup")
    def create_user_api(login: LoginCredentials, db: Session=Depends(get_db)) -> str:
        """
        Create a new user
        return a user id or a token we don't know yet
        """
        if create_user(login,db):
            return create_login_access_token(login)
        else:
            raise JSONException(status_code=400, error={"message": "User already exists"})

    @app.post(prefix + "/info")
    def info(token:Annotated[str, Depends(decode_access_token)]) -> None:
        """
        Logout a user #TODO: decide what is this for.
        """
        return token

    @app.post(prefix + "/me")
    def info(token: Annotated[str, Depends(decode_user_token)]) -> None:
        """
        Logout a user
        """
        return token

    @app.post(prefix + "/games/")
    def get_games(token:Annotated[str, Depends(decode_user_token)],db:Session=Depends(get_db)) -> list[int]:
        """
        Get all games of a user
        """
        gw = db.query(Game).filter(Game.white_player == token['username']).all()
        gb = db.query(Game).filter(Game.black_player == token['username']).all()
        # to transofrm
        out = list(gw.extend(gb))
        return None

    @app.post(prefix + "/leaderboard/") 
    def leaderboard(db:Session=Depends(get_db)) -> list[LeaderBoardResponse]:
        """
        Get all games of a user
        """
        rating = db.query(User).order_by(User.rating.desc()).all()
        
        return list(map(lambda x: LeaderBoardResponse(
            avatar=x.profile_image_url,
            user=x.user,
            elo=x.rating
        ),rating))