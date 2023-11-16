from pydantic import BaseModel

class LoginCredentials(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user_id: int