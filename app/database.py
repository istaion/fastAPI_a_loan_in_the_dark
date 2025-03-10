from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Chaîne de connexion MSSQL pour SQLModel
DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"

# Création du moteur SQLAlchemy compatible avec SQLModel
engine = create_engine(DATABASE_URL, echo=True)

# Fonction de dépendance FastAPI pour obtenir une session
def get_db():
    with Session(engine) as session:
        yield session