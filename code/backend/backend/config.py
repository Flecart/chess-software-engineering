
from typing import ClassVar, Union
from fastapi.types import UnionType
import yaml
import os


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
        if os.path.exists('config.yaml'):
            with open('config.yaml', 'r') as file:
                self.config = yaml.safe_load(file)
        else:
            with open('default_config.yaml', 'r') as file:
                self.config = yaml.safe_load(file)
            