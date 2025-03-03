from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from app.models.user import User

class UserCreate(BaseModel):
    """
    Schema for user creation.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The plain text password to be hashed later.
        is_staff (bool): Defines if the user has administrative privileges.
    """
    email: EmailStr
    password: str
    is_staff: bool
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    advisor_id: Optional[UUID] = None

class UserConnection(BaseModel):
    """
    Schema for user authentication (login).

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The plain text password for authentication.
    """
    email: EmailStr
    password: str

class UserRead(BaseModel):
    """
    Schema for reading user information.

    Attributes:
        id (UUID): The unique identifier of the user.
        email (EmailStr): The email address of the user.
        is_staff (bool): Indicates if the user has administrative privileges.
        is_active (bool): Indicates if the user's account is active.
        first_connection (bool): Specifies whether it is the user's first login.
    """
    id: UUID
    email: EmailStr
    is_staff: bool
    is_active: bool
    first_connection: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    username: Optional[str] = None
    advisor_id: Optional[UUID] = None


class UserPasswordUpdate(BaseModel):
    new_password: str

class UserUpdate(BaseModel):
    """
    Schema for reading user information.

    Attributes:
        id (UUID): The unique identifier of the user.
        email (EmailStr): The email address of the user.
        is_staff (bool): Indicates if the user has administrative privileges.
        is_active (bool): Indicates if the user's account is active.
        first_connection (bool): Specifies whether it is the user's first login.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    username: Optional[str] = None
    advisor_id: Optional[UUID] = None


