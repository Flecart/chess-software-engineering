import os


defConfig = {
    'port': 8000,
    'host': "127.0.0.1"
}

class Config():
    config:dict
    __instance = None

    def __getitem__(self,name):
        return self.config[name]


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__init()
        return cls.__instance

    def __init(self):
        self.config = defConfig    
        for key in defConfig.keys():
            if key in os.environ:
                if type(defConfig[key]) == int:
                    self.config[key] = int(os.environ[key])
                else:
                    self.config[key] = os.environ[key]
            