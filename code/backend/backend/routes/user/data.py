from pydantic import BaseModel

class LoginCredentials(BaseModel):
    username: str
    password: str


class LeaderBoardResponse(BaseModel):
    username: str
    elo: float
    avatar: str
    wins:int =0
    losses:int =0

class InfoUser(BaseModel):
    username: str
    elo: float
    avatar: str
    wins:int =0
    losses:int =0

class GameInfo(BaseModel):
    opponentName: str
    opponentElo: float
    opponentAvatar: str
    result: str
    eloGain:int 
    id: int
    
