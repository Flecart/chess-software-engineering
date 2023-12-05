import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
backend = os.getenv("BACKEND_URL")
DEBUG = os.getenv("DEBUG") == "True"
TIME_TO_VOTE_IN_SECONDS= int(os.getenv("TIME_TO_VOTE_IN_SECONDS"))

