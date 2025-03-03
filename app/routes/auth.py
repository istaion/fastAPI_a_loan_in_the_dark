from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserConnection
from app.services.auth import create_access_token
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/login")
def login(user: UserConnection, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns an access token.
    """
    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # If the user does not exist
    if db_user is None:
        raise HTTPException(status_code=401, detail="This user is not registered")
    
    # If the password is incorrect
    elif not db_user.verify_password(user.password):  
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Generate an access token
    token = create_access_token({"sub": user.email})
    
    return {"access_token": token, "token_type": "bearer"}

@router.get("/verify_token")
async def verify_token(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Vérifie si le token est valide et retourne un statut HTTP 200 si OK.

    Args:
        current_user (dict): L'utilisateur authentifié grâce au token.
        db (Session): Session de base de données (Dépendance FastAPI).

    Returns:
        dict: Un message de confirmation si le token est valide.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    
    return {"message": "Token valide", "user_id": current_user.id}
