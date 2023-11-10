from pydantic import BaseModel

class CreateGameRequest(BaseModel):
    against_bot: bool = True
    color: str = 'white'
    type: str = 'dark_chess'
    #time: (int,int) = (3,3) 
    #increment: (int,int) = (0,0) 

    
class GameStatusResponse(BaseModel):
    fen:str
    finish:bool
    possible_moves: list[str]|None = None
    best_move:str|None = None
    view:str