from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database file definition
SQLALCHEMY_DB_URL = "sqlite:///./fastapi_todos_db/todos.db"

# Create DB Engine
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={'check_same_thread': False})

# Session Factory or Class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB Object
Base = declarative_base()