from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User 
from app.database import get_db
from sqlalchemy.orm import Session
from typing import Dict
from fastapi import HTTPException, status, Depends
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Secret key and algorithm for JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Fallback for development only - In production, always use environment variable
    SECRET_KEY = "votre_cle_secrete_de_dev_123!@#"
    print("Warning: Using default SECRET_KEY. This is not secure in production.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# OAuth2 authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Generates a JWT access token.

    Args:
        data (dict): The payload data to encode in the token.
        expires_delta (timedelta, optional): The expiration duration.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Dict:
    """
    Decodes and verifies a JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        Dict: The decoded token payload.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Retrieves the current authenticated user from the JWT token.

    Args:
        token (str): The JWT token from the request header.
        db (Session): The database session.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    try:
        user_data = verify_token(token)  # Verify token and extract data
        user = db.query(User).filter(User.email == user_data['sub']).first()  # Find user in DB
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
