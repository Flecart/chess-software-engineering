from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped

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
    profile_image_url = Column(String, default=f"https://api.dicebear.com/7.x/lorelei/png?seed={user}")
    profile_image_type = Column(Enum("link", "blob", name="image_type"), default="link")
    auth = relationship("Auth", back_populates="user_instance")

class Game(Base):
    __tablename__ = "game"
    
    game_id = Column(Integer, primary_key=True)
    white_player = Column(Integer)
    black_player = Column(Integer)
    moves = Column(String)
    state = Column(Enum('ENDED', 'STARTED', name='state'))
    winner = Column(Enum('white', 'black', 'not_ended', name='winner'))
