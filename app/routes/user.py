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
    print(f"Received create user request with data: {user_create}")
    print(f"Current user: {current_user.email}, is_staff: {current_user.is_staff}")
    
    # Vérification du staff
    if not current_user.is_staff:
        print("Access denied: User is not staff")
        raise HTTPException(status_code=403, detail="Access denied. You must be a staff user.")
    
    # Création de l'utilisateur
    try:
        new_user = create_user(db=db, user_create=user_create)
        print(f"User created successfully: {new_user.email}")
        return new_user
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=UserRead)
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieves a user by their ID.

    Args:
        user_id (UUID): The ID of the user.
        db (Session): The database session.

    Returns:
        UserRead: The retrieved user information.
    
    Raises:
        HTTPException: If the user is not found.
    """
    return get_user_by_id(db=db, user_id=user_id)

@router.get("/list", response_model=list[UserRead])
async def list_users(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
    ):
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only advisors can list users"
        )
    
    users = session.exec(select(User)).all()
    return users

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    """
    Returns the currently authenticated user's basic details.

    Args:
        current_user (User): The authenticated user.

    Returns:
        dict: The user's ID and email.
    """
    return get_user_by_id(db=db, user_id=current_user.id)

@router.patch("/me/edit")
def update_user_me(
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Update details about the current user.
    Args:
        user_update (User): The authentificated user with updated details
        db (Session): The database session.
        current_user (User): The currently authenticated user.
    """
    update_user(db, user=current_user,updated_user=user_update)

@router.put("/update-password", response_model=dict)
async def update_password(
    password_data: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    
    update_user_password(session, current_user, password_data.new_password)

    return {"message": "Password updated successfully"}

