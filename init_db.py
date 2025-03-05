import json
import os
import uuid
import logging
from app.database import engine
from app.models.user import User
from app.services.user import create_user
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from sqlmodel import Session as SqlSession

# Liste des utilisateurs à créer
users_data = [
    {"email": "vic@staff.fr", "password": "password1234", "is_staff": True},
    {"email": "nico@staff.fr", "password": "password1234", "is_staff": True},
    {"email": "leo@staff.fr", "password": "password1234", "is_staff": True},
]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Encodeur personnalisé pour gérer UUID
def uuid_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)  # Convertit UUID en chaîne
    raise TypeError("Type non sérialisable")

def init_db():
    """Initialise la base de données avec des utilisateurs par défaut et enregistre les données dans un fichier JSON"""
    list_user_json = []
    
    try:
        with Session(engine) as session:  # Using SQLAlchemy Session for DB operations
            for user in users_data:
                user_create = UserCreate(email=user["email"], password=user["password"], is_staff=user["is_staff"])
                # Vérifier si l'utilisateur existe déjà
                existing_user = session.query(User).filter_by(email=user["email"]).first()
                if existing_user:
                    logger.info("L'utilisateur existe déjà")
                    continue
                created_user = create_user(db=session, user_create=user_create)
                list_user_json.append(created_user)
            logger.info("Utilisateurs staff importés avec succès")

        # Path handling with os.path to ensure cross-platform compatibility
        output_file = os.path.join(os.path.dirname(__file__), 'users_data.json')
        
        # Save the list of users into a JSON file
        with open(output_file, 'w') as f:
            json.dump([user.dict() for user in list_user_json], f, indent=4, default=uuid_serializer)
        
        logger.info(f"Les utilisateurs ont été enregistrés dans le fichier '{output_file}'")
    
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données : {e}")
        raise

# Exécuter la fonction si ce fichier est lancé directement
if __name__ == "__main__":
    init_db()
