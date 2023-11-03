from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.routes.game import create_game_routes
from backend.routes.test import create_test_routes

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

# TODO(gio): initialize db connection

logging.getLogger('main').info('Creating routes')
""" adding routes  """
create_game_routes(app)
create_test_routes(app)
logging.getLogger('main').info('Create routes')

