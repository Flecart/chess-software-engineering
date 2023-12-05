from dataclasses import dataclass

@dataclass
class MCSTPlayerConfig:
    roll_outs: int =1
    utc:int  = 25
    max_sim: int = 333