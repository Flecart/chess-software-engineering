from fastapi import Request
from fastapi.responses import JSONResponse


class JSONException(Exception):
    def __init__(self,error:dict,status_code:int = 418 ):
        self.status_code = status_code
        self.error = error 



def install_exception_handler(app):
    @app.exception_handler(JSONException)
    async def exception_handler(r,exec):
        return JSONResponse(
            status_code=exec.status_code,
            content=exec.error,
        )