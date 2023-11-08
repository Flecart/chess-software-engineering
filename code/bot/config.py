import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
backend = os.getenv("BACKEND_URL")+'/dev'
DEBUG = os.getenv("DEBUG") == "True"

