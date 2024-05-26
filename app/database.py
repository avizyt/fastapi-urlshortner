from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

connect_args = {"check_same_thread": False}

# Create a database engine based on the database URL in the settings
engine = create_engine(get_settings().db_url, connect_args=connect_args)

# Create a session maker based on the engine
# The session maker will create a session that is bound to the engine, and will
# automatically commit and flush the session when a transaction is finished.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class, which is the base class for all ORM models
Base = declarative_base()
