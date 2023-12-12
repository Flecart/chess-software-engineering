import os
from dotenv import load_dotenv


defConfig = {
    "port": 8000,
    "host": "127.0.0.1",
    "db_local": "False",
    "db_password": "password",
    "db_user": "root",
    "db_url": "localhost",
    "bot_username": "bot",
    "ssl_keyfile": "./privkey.pem",
    "ssl_certfile": "./cert.pem",
    "URL_KRIEGSPER": "http://app.t1-check-mates.mooo.com:8085/?",
    "bot": "check_mates_bot",
}


class Config:
    config_data: dict
    __instance = None

    def __getitem__(self, name):
        if name in self.config_data:
            return self.config_data[name]
        return None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__init()
        return cls.__instance

    def __init(self):
        load_dotenv()
        self.config_data = defConfig
        for key in defConfig.keys():
            if key in os.environ:
                self.config_data[key] = os.environ[key]
