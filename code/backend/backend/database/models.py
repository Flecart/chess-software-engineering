from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped
from backend.database.utils_elo import get_point_difference

from backend.game.utils import Color

from .database import engine

from .database import Base

class Auth(Base):
    __tablename__ = "auth"
    id = Column(Integer, primary_key=True, index=True)
    user = mapped_column(String, ForeignKey('users.user'), index=True)
    is_active = Column(Boolean, default=True)
    salt = Column(String)
    hashed_password = Column(String)

    # see https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-uselist-false-for-non-annotated-configurations
    user_instance = relationship("User", back_populates="auth")

class User(Base):
    __tablename__ = "users"
    user = Column(String, primary_key=True, index=True)
    profile_image = Column(LargeBinary, default=None)
    profile_image_url = Column(String, default=lambda context: f"https://api.dicebear.com/7.x/lorelei/png?seed={context.get_current_parameters()['user']}")
    profile_image_type = Column(Enum("link", "blob", name="image_type"), default="link")
    auth = relationship("Auth", back_populates="user_instance")
    rating = Column(Integer, default=1500)
    wins: int = Column(Integer, default=0)
    losses: int = Column(Integer, default=0)

class Game(Base):
    __tablename__ = "game"
    game_id = Column(Integer, primary_key=True,autoincrement=True)
    white_player = Column(String)
    black_player = Column(String)
    fen = Column(String)
    moves = Column(String)
    is_finish = Column(Boolean)
    winner = Column(Enum('white', 'black',  name='winner'))
    white_points = Column(Integer)
    black_points = Column(Integer)

    def get_opponent(self, player: str) -> str:
        if self.white_player == player:
            return self.black_player
        else:
            return self.white_player
    
    def get_opponent_rating(self, player: str) -> int:
        if self.white_player == player:
            return self.black_points
        else:
            return self.white_points
    
    def get_color_player(self,player:str)->Color:
        if self.white_player == player:
            return Color.WHITE
        else:
            return Color.BLACK

    def get_point_difference(self, player: str) -> int:
        value={
            'win':1,
            'lose':0,
            'draw':0.5
        }
        state = self.get_state_game(player)
        if state not in value:
            return 0
        if self.get_color_player(player) == Color.WHITE:
            return get_point_difference(self.white_points, self.black_points, value[state])
        else:
            return get_point_difference(self.black_points, self.white_points, value[state])

    def get_state_game(self, player: str) -> str:
        if self.winner == None:
            return "playing"
        elif self.winner == self.get_color_player(player):
            return "win"
        elif self.winner == 'draw':
            return 'draw'
        else:
            return 'lose'


    def __repr__(self) -> str:
        return f"Game({self.game_id}, {self.white_player}, {self.black_player}, {self.fen}, {self.moves}, {self.is_finish}, {self.winner}, {self.white_points}, {self.black_points})"

Base.metadata.create_all(bind=engine)