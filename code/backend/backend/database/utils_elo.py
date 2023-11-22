
def get_estimate_outcome(elo1:int,elo2:int):
    return 1/(1+10**((elo2-elo1)/400))

def get_point_difference(elo1:int,elo2:int,win:int):
    return 32*((win)-get_estimate_outcome(elo1,elo2))