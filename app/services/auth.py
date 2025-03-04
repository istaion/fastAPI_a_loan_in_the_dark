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

    This function creates and encodes a JWT token with the specified payload
    and expiration time. If no expiration time is provided, the default expiration
    time will be used.

    Args:
        data (dict): The payload data to encode in the token.
        expires_delta (timedelta, optional): The expiration duration for the token.

    Returns:
        str: The encoded JWT token.
    """
    # Copy the provided data and add expiration time
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # Add expiration to the payload
    
    # Encode the payload into a JWT token using the secret key and algorithm
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Dict:
    """
    Decodes and verifies a JWT token.

    This function decodes the provided JWT token using the secret key and algorithm.
    If the token is expired or invalid, it raises an HTTPException with a relevant message.

    Args:
        token (str): The JWT token to decode and verify.

    Returns:
        Dict: The decoded token payload, if the token is valid.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Raise an exception if the token is expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        # Raise an exception if the token is invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Retrieves the current authenticated user from the JWT token.

    This function decodes the provided JWT token, verifies its validity, and extracts
    the user information from the database. If the user is not found or the token is invalid,
    an HTTPException is raised.

    Args:
        token (str): The JWT token from the request header.
        db (Session): The database session used to query the user.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the token is invalid, expired, or the user is not found in the database.
    """
    try:
        # Verify and decode the token, then extract user data from it
        user_data = verify_token(token)
        
        # Query the user from the database using the decoded email
        user = db.query(User).filter(User.email == user_data['sub']).first()
        
        if user is None:
            # Raise exception if the user is not found in the database
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception:
        # Raise a general exception if there is any error with the token or user lookup
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
