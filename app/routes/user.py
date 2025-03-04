from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserRead, UserPasswordUpdate, UserUpdate
from sqlmodel import select
from app.services.user import create_user, get_user_by_id, update_user
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from app.services.auth import get_current_user
from app.models.user import User
from app.services.user import update_user_password

router = APIRouter()

@router.post("/create_user", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_create: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Creates a new user in the system, but only if the current user is staff.

    Args:
        user_create (UserCreate): The data for the user to be created.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        UserRead: The newly created user information.
    
    Raises:
        HTTPException: If the current user is not a staff member or if there is an error during user creation.
    """
    if not current_user.is_staff:
        raise HTTPException(status_code=403, detail="Access denied. You must be a staff user.")
    
    try:
        new_user = create_user(db=db, user_create=user_create)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("/user/{user_id}", response_model=UserRead)
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieves a user by their unique ID.

    Args:
        user_id (UUID): The ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserRead: The details of the retrieved user.
    
    Raises:
        HTTPException: If the user is not found.
    """
    return get_user_by_id(db=db, user_id=user_id)

@router.get("/list", response_model=list[UserRead])
async def list_users(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """
    Lists all users in the system, but only if the current user is a staff member.

    Args:
        current_user (User): The currently authenticated user.
        session (Session): The database session.

    Returns:
        list[UserRead]: A list of all users in the system.

    Raises:
        HTTPException: If the current user is not a staff member.
    """
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff members can list users."
        )
    
    users = session.exec(select(User)).all()
    return users

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Retrieves the currently authenticated user's information.

    Args:
        current_user (User): The authenticated user.
        db (Session): The database session.

    Returns:
        UserRead: The currently authenticated user's details.
    """
    return get_user_by_id(db=db, user_id=current_user.id)

@router.patch("/me/edit")
def update_user_me(
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Updates the details of the currently authenticated user.

    Args:
        user_update (UserUpdate): The updated user details.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        UserRead: The updated user details.
    
    Raises:
        HTTPException: If the update operation fails.
    """
    update_user(db, user=current_user, updated_user=user_update)

@router.put("/update-password", response_model=dict)
async def update_password(
    password_data: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """
    Updates the password for the currently authenticated user.

    Args:
        password_data (UserPasswordUpdate): The new password to set.
        current_user (User): The currently authenticated user.
        session (Session): The database session.

    Returns:
        dict: A success message indicating the password has been updated.
    
    Raises:
        HTTPException: If the user is not authenticated or the update operation fails.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    
    update_user_password(session, current_user, password_data.new_password)

    return {"message": "Password updated successfully"}
