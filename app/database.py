from sqlmodel import create_engine, Session
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la chaîne de connexion PostgreSQL depuis les variables d'environnement
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db/{os.getenv('POSTGRES_DB')}"
# DATABASE_URL = "sqlite:///./app/db.sqlite3"

# Create a database engine
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

@contextmanager
def get_db():
    """
    Provides a database session for dependency injection.
    
    This function is used as a context manager to ensure the session is properly
    closed after use, even if an error occurs.
    
    Yields:
        Session: A database session.
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
