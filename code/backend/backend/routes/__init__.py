from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.routes.user.user import create_user_routes
from backend.routes.darkboard.darkboardgame import (
    create_game_routes as create_darkboard_routes,
)

from .game.game import create_game_routes
from .exception import install_exception_handler


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # nonostante con allow_origin sembri accessibile a tutti, non sarà un servizio esposto su internet,
    # quindi stiamo permettendo la comunicazione solamente con i servizi che si trovano come descritti dal docker compose.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.getLogger("main").info("Creating routes")
""" adding routes  """

install_exception_handler(app)

create_game_routes(app, prefix="/api/v1")
create_user_routes(app, prefix="/api/v1")
create_darkboard_routes(app, prefix="/api/v1")

logging.getLogger("main").info("Createe routes")
