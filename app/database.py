from sqlmodel import create_engine, Session
import sqlmodel

# Define the database URL
DATABASE_URL = "sqlite:///./app/db.sqlite3"

# Create a database engine
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_db():
    """
    Provides a database session for dependency injection.

    Yields:
        Session: A database session.
    """
    with Session(engine) as session:
        yield session
