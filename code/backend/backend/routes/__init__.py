from fastapi import FastAPI
import logging

from backend.routes.game import create_game_routes
from backend.routes.test import create_test_routes


app = FastAPI()

# TODO(gio): initialize db connection

logging.getLogger('main').info('Creating routes')
""" adding routes  """
create_game_routes(app)
create_test_routes(app)
logging.getLogger('main').info('Create routes')

