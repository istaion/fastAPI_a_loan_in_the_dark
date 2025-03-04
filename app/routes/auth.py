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

    This function verifies if the user's email exists in the database and if the provided password
    is correct. If both checks pass, it generates a JWT access token for the user.

    Args:
        user (UserConnection): The user login credentials containing email and password.
        db (Session): The database session, injected by FastAPI.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the user is not registered or the password is incorrect, a 401 error is raised.
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
    Verifies if the provided token is valid and returns a status message if successful.

    This function ensures that the provided JWT token is valid and corresponds to a registered user.
    If valid, a confirmation message with the user ID is returned.

    Args:
        current_user (dict): The current user retrieved from the validated JWT token.
        db (Session): The database session, injected by FastAPI.

    Returns:
        dict: A confirmation message indicating the token is valid along with the user ID.

    Raises:
        HTTPException: If the token is invalid or expired, a 401 error is raised.
    """
    # Ensure the current_user is valid
    if not current_user:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    
    return {"message": "Token valide", "user_id": current_user.id}
