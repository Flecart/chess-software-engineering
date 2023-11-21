from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped

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
    profile_image_url = Column(String, default=f"https://api.dicebear.com/7.x/lorelei/png?seed=12")
    profile_image_type = Column(Enum("link", "blob", name="image_type"), default="link")
    auth = relationship("Auth", back_populates="user_instance")
    rating = Column(Integer, default=1500)

class Game(Base):
    __tablename__ = "game"
    game_id = Column(Integer, primary_key=True,autoincrement=True)
    white_player = Column(String)
    black_player = Column(String)
    fen = Column(String)
    moves = Column(String)
    is_finish = Column(Boolean)
    winner = Column(Enum('white', 'black',  name='winner'))

    def __repr__(self) -> str:
        return f"Game({self.game_id}, {self.white_player}, {self.black_player}, {self.fen}, {self.moves}, {self.is_finish}, {self.winner})"

Base.metadata.create_all(bind=engine)