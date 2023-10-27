from fastapi import FastAPI
from typing import Union


def create_test_routes(app:FastAPI):

    @app.get("/test")
    def read_root():
        return {"Hello": "test"}


