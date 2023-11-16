import os
from dotenv import load_dotenv


defConfig = {
    'port': 8000,
    'host': "127.0.0.1",
    'db_local': 'True',
    'db_password': 'password',
    'db_user': 'root',
    'db_url': 'localhost'
}

class Config():
    config:dict
    __instance = None

    def __getitem__(self,name):
        if name in self.config:
            return self.config[name]
        return None


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__init()
        return cls.__instance

    def __init(self):
        load_dotenv()
        self.config = defConfig    
        for key in defConfig.keys():
            if key in os.environ:
                self.config[key] = os.environ[key]
            