from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Récupérer la chaîne de connexion PostgreSQL depuis les variables d'environnement
DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
# DATABASE_URL = "sqlite:///./app/db.sqlite3"

# Create a database engine
engine = create_engine(DATABASE_URL, echo=True)

# Créer un sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction de dépendance FastAPI pour obtenir une session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
