from sqlalchemy import Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config import Config

_config = Config()

DATABASE_URL = f"postgresql://{_config['db_user']}:{_config['db_password']}@{_config['db_url']}"

if _config['db_local'] == 'True':
    DATABASE_URL = 'sqlite:///./sql_app.db'

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
