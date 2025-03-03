from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

def create_user(db: Session, user_create: UserCreate) -> UserRead:
    """
    Creates a new user with a hashed password and saves them to the database.

    Args:
        db (Session): The database session.
        user_create (UserCreate): The data for the new user.

    Returns:
        UserRead: The created user without the password.
    
    Raises:
        HTTPException: If the email is already used.
    """
    # Check if the email is already taken
    db_user = db.query(User).filter(User.email == user_create.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use",
        )
    print(user_create.password)
    
    # Hash the user's password
    hashed_password = User.hash_password(user_create.password)
    
    # Create a new user instance
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        is_staff=user_create.is_staff,
        first_name = user_create.first_name,
        last_name = user_create.last_name,
        advisor_id = user_create.advisor_id,
        phone_number = user_create.phone_number,
        is_active=True,
        first_connection=True,  # Default: user has not logged in yet
    )
    
    # Save user to the database     
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Return the created user without the password
    return UserRead(
        id=db_user.id,
        email=db_user.email,
        is_staff=db_user.is_staff,
        is_active=db_user.is_active,
        first_connection=db_user.first_connection,
        first_name = db_user.first_name,
        last_name = db_user.last_name,
        advisor_id = db_user.advisor_id,
        phone_number = db_user.phone_number,
        username = db_user.username,
    )

def get_user_by_id(db: Session, user_id: UUID) -> UserRead:
    """
    Retrieves a user by their unique ID.

    Args:
        db (Session): The database session.
        user_id (UUID): The ID of the user.

    Returns:
        UserRead: The user information.
    
    Raises:
        HTTPException: If the user is not found.
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
        first_name = db_user.first_name,
        last_name = db_user.last_name,
        advisor_id = db_user.advisor_id,
        phone_number = db_user.phone_number,
        username = db_user.username,
    )

def update_user(db: Session, user: User, updated_user: UserUpdate):
    """
    Update an existing user in the db.

    Args:
        db (Session): The database session.
        updated_user (User): The user that we have to update.
    """

    # Search the existing user
    db_user = user
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found")

    db_user.first_name = updated_user.first_name
    db_user.last_name = updated_user.last_name
    db_user.advisor_id = updated_user.advisor_id
    db_user.phone_number = updated_user.phone_number
    db_user.username = updated_user.username

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

def update_user_password(session: Session, user: User, new_password: str):
    user.hashed_password = User.hash_password(new_password)
    user.first_connection = False
    session.add(user)
    session.commit()
    session.refresh(user)


