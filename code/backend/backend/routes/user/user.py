from fastapi import FastAPI

from backend.routes.user.data import LoginCredentials, LoginResponse

def create_user_routes(app: FastAPI,prefix:str=''):
    prefix = f'{prefix}/user'

    @app.post(prefix + "/create")
    def create_user(login: LoginCredentials) -> LoginResponse:
        """
        Create a new user
        return a user id or a token we don't know yet
        """
        return None

    @app.post(prefix + "/login")
    def login(login: LoginCredentials) -> LoginResponse:
        """
        Login a user
        return a user id or a token we don't know yet
        """
        return None

    @app.post(prefix + "/logout")
    def logout() -> None:
        """
        Logout a user
        """
        return None

    @app.post(prefix + "/games/")
    def get_games() -> list[int]:
        """
        Get all games of a user
        """
        return None

    