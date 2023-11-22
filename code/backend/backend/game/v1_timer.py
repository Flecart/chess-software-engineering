

from datetime import datetime, timedelta


class Timer():

    def __init__(self,remaining_time:timedelta):
        self.remaining_time = remaining_time
        self.start_time = None
    
    def start(self):
        self.start_time = datetime.now()
    
    def stop(self) -> bool:
        if self.start_time is None:
            return False
        self.remaining_time -= datetime.now() - self.start_time
        self.start_time = None
        return self.is_finished()
    
    def is_finished(self) -> bool:
        return self.remaining_time <= timedelta(0)
    
