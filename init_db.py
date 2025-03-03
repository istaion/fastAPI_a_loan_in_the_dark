import json
from app.database import engine, Session
from app.models.user import User
from app.services.user import create_user
from app.schemas.user import UserCreate
import sqlmodel
import uuid

# Liste des utilisateurs à créer
users_data = [
    {"email": "vic@staff.fr", "password": "password1234", "is_staff": True},
    {"email": "nico@staff.fr", "password": "password1234", "is_staff": True},
    {"email": "leo@staff.fr", "password": "password1234", "is_staff": True},
]

# Encodeur personnalisé pour gérer UUID
def uuid_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)  # Convertit UUID en chaîne
    raise TypeError("Type non sérialisable")

def init_db():
    """Initialise la base de données avec des utilisateurs par défaut et enregistre les données dans un fichier JSON"""
    list_user_json = []
    with Session(engine) as session:
        for user in users_data:
            user_create = UserCreate(email=user["email"], password=user["password"], is_staff=user["is_staff"])
            created_user = create_user(db=session, user_create=user_create)
            list_user_json.append(created_user)
        print("Utilisateurs staff importés avec succès")
    
    # Sauvegarder la liste d'utilisateurs dans un fichier JSON
    with open('../djangoLoan/users_data.json', 'w') as f:
        json.dump([user.dict() for user in list_user_json], f, indent=4, default=uuid_serializer)  # Utilisation de l'encodeur personnalisé

    print("Les utilisateurs ont été enregistrés dans le fichier 'users_data.json'")
    

# Exécuter la fonction si ce fichier est lancé directement
if __name__ == "__main__":
    init_db()
