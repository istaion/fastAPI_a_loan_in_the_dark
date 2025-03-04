from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

def create_user(db: Session, user_create: UserCreate) -> UserRead:
    """
    Creates a new user with a hashed password and saves them to the database.

    This function checks if the email provided is already in use, hashes the user's password,
    creates a new user record, and saves the user to the database. 

    Args:
        db (Session): The database session.
        user_create (UserCreate): The data for the new user (email, password, etc.).

    Returns:
        UserRead: A representation of the created user without the password.

    Raises:
        HTTPException: If the email is already in use, a 400 Bad Request error is raised.
    """
    # Check if the email is already taken
    db_user = db.query(User).filter(User.email == user_create.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use",
        )

    # Hash the user's password
    hashed_password = User.hash_password(user_create.password)
    
    # Create a new user instance with provided data
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        is_staff=user_create.is_staff,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        advisor_id=user_create.advisor_id,
        phone_number=user_create.phone_number,
        is_active=True,  # User is active by default
        first_connection=True,  # Set to True because user hasn't logged in yet
    )
    
    # Save the user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Return the created user (excluding sensitive information like the password)
    return UserRead(
        id=db_user.id,
        email=db_user.email,
        is_staff=db_user.is_staff,
        is_active=db_user.is_active,
        first_connection=db_user.first_connection,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        advisor_id=db_user.advisor_id,
        phone_number=db_user.phone_number,
        username=db_user.username,
    )

def get_user_by_id(db: Session, user_id: UUID) -> UserRead:
    """
    Retrieves a user by their unique ID.

    This function queries the database to fetch a user by their ID. If the user is found, 
    their data is returned. If not, a 404 error is raised.

    Args:
        db (Session): The database session.
        user_id (UUID): The unique identifier of the user.

    Returns:
        UserRead: The user details (email, first name, last name, etc.).

    Raises:
        HTTPException: If the user is not found, a 404 Not Found error is raised.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return UserRead(
        id=db_user.id,
        email=db_user.email,
        is_staff=db_user.is_staff,
        is_active=db_user.is_active,
        first_connection=db_user.first_connection,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        advisor_id=db_user.advisor_id,
        phone_number=db_user.phone_number,
        username=db_user.username,
    )

def update_user(db: Session, user: User, updated_user: UserUpdate):
    """
    Updates an existing user's information in the database.

    This function updates the user details such as first name, last name, advisor ID, phone number, 
    and username based on the provided `updated_user` data.

    Args:
        db (Session): The database session.
        user (User): The user that is to be updated (must be fetched beforehand).
        updated_user (UserUpdate): The updated user data.

    Raises:
        HTTPException: If the user is not found, a 400 Bad Request error is raised.
    """
    # Check if the user exists in the database
    db_user = user
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )

    # Update user fields with new data
    db_user.first_name = updated_user.first_name
    db_user.last_name = updated_user.last_name
    db_user.advisor_id = updated_user.advisor_id
    db_user.phone_number = updated_user.phone_number
    db_user.username = updated_user.username

    # Commit the changes to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

def update_user_password(session: Session, user: User, new_password: str):
    """
    Updates the password for an existing user.

    This function hashes the new password, updates the user's `hashed_password`, and
    marks the user as having logged in for the first time.

    Args:
        session (Session): The database session.
        user (User): The user whose password is to be updated.
        new_password (str): The new password provided by the user.

    Returns:
        None
    """
    # Hash the new password and update the user's password
    user.hashed_password = User.hash_password(new_password)
    user.first_connection = False  # Mark as no longer first time connection
    session.add(user)
    session.commit()
    session.refresh(user)
