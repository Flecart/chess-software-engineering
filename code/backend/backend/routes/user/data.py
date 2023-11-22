from pydantic import BaseModel

class LoginCredentials(BaseModel):
    username: str
    password: str


class LeaderBoardResponse(BaseModel):
    user: str
    elo: float
    avatar: str
