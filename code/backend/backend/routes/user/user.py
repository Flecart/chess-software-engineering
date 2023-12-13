from fastapi import Depends, FastAPI
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.database.models import Game, User
from backend.routes.exception import JSONException
from backend.routes.user.data import (
    GameInfo,
    LeaderBoardResponse,
    LoginCredentials,
    InfoUser,
)
from backend.database.database import get_db
from backend.database.utils import create_user, check_login
from backend.routes.auth import (
    create_guest_access_token,
    create_login_access_token,
)


def create_user_routes(app: FastAPI, prefix: str = ""):
    prefix = f"{prefix}/user"

    @app.post(prefix + "/guest")
    def guest(db: Session = Depends(get_db)) -> str:
        """
        Login a user
        return a user id or a token we don't know yet
        """
        import random

        return create_guest_access_token(random.randint(0, 100000))

    @app.post(prefix + "/login")
    def login_api(login: LoginCredentials, db: Session = Depends(get_db)) -> str:
        """
        Login a user
        return a user id or a token we don't know yet
        """
        if check_login(login, db):
            return create_login_access_token(login)
        else:
            raise JSONException(
                status_code=400, error={"message": "User or password wrong"}
            )

    @app.post(prefix + "/signup")
    def create_user_api(login: LoginCredentials, db: Session = Depends(get_db)) -> str:
        """
        Create a new user
        return a user id or a token we don't know yet
        """
        if create_user(login, db):
            return create_login_access_token(login)
        else:
            raise JSONException(
                status_code=400, error={"message": "User already exists"}
            )

    @app.get(prefix + "/info/{user}")
    def info(user: str, db: Session = Depends(get_db)) -> InfoUser:
        selected_user = db.query(User).filter(User.user == user).first()
        if selected_user is None:
            raise JSONException(
                status_code=400, error={"message": "User does not exist"}
            )
        return InfoUser(
            username=selected_user.user,
            avatar=selected_user.profile_image_url,
            elo=round(selected_user.rating),
            losses=selected_user.losses,
            wins=selected_user.wins,
        )

    @app.get(prefix + "/games/{user}")
    def get_games(user: str, db: Session = Depends(get_db)) -> list[GameInfo]:
        """
        Get all games of a user
        """
        games = (
            db.query(Game)
            .filter(
                or_(Game.white_player == user, Game.black_player == user),
                Game.white_player is not None,
                Game.black_player is not None,
                Game.winner is not None,

            )
            .all()
        )
        if games is None or len(games) == 0:
            return []
        
        games = list(filter(lambda x: x is not None, games))


        game_info_from_game = lambda x: GameInfo(
                id=x.game_id,
                opponentName=x.get_opponent(user),
                opponentAvatar=db.query(User)
                .filter(User.user == x.get_opponent(user))
                .first()
                .profile_image_url,
                eloGain=round(x.get_point_difference(user)),
                opponentElo=round(x.get_opponent_rating(user)),
                result=x.get_state_game(user),
            )

        def game_try_game_info(x):
            try:
                return game_info_from_game(x)
            except:
                return None


        gameinfo_list = map(
            game_try_game_info, 
            games,
        )


        games = list(filter(lambda x: x is not None, games))

        print(games)
        return list(reversed(list(gameinfo_list)))

    @app.get(prefix + "/leaderboard")
    def leaderboard(db: Session = Depends(get_db)) -> list[LeaderBoardResponse]:
        """
        Get all games of a user
        """
        rating = db.query(User).order_by(User.rating.desc()).all()
        if rating is None or len(rating) == 0:
            return []

        rating = list(filter(lambda x: x is not None, rating))

        return list(
            map(
                lambda x: LeaderBoardResponse(
                    avatar=x.profile_image_url,
                    username=x.user,
                    elo=round(x.rating),
                    losses=x.losses,
                    wins=x.wins,
                ),
                rating,
            )
        )
