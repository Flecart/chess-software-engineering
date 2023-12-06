import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEBUG = os.getenv("DEBUG") == "True"
TIME_TO_VOTE_IN_SECONDS = int(os.getenv("TIME_TO_VOTE_IN_SECONDS"))

http_protocol = os.getenv("PROTOCOL")
ws_protocol = os.getenv("WS_PROTOCOL")
host = os.getenv("HOST")

backend_url = f"{http_protocol}://{host}"
ws_url = f"{ws_protocol}://{host}"
api_base_url = "/api/v1"
