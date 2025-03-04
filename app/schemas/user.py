from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from app.models.user import User

class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    This schema defines the fields required for creating a new user account,
    including their email, password (to be hashed), and administrative status.

    Attributes:
        email (EmailStr): The email address of the user. It must be unique.
        password (str): The plain text password which will be hashed later.
        is_staff (bool): Indicates if the user has administrative privileges.
        username (Optional[str]): The username for the user (optional).
        first_name (Optional[str]): The user's first name (optional).
        last_name (Optional[str]): The user's last name (optional).
        phone_number (Optional[str]): The user's phone number (optional).
        advisor_id (Optional[UUID]): The advisor assigned to the user (optional).
    """
    email: EmailStr  # Email address of the user
    password: str  # Plain text password to be hashed
    is_staff: bool  # Whether the user has administrative privileges
    username: Optional[str] = None  # Username, used for the company name of the client
    first_name: Optional[str] = None  # First name of the user
    last_name: Optional[str] = None  # Last name of the user
    phone_number: Optional[str] = None  # Phone number of the user
    advisor_id: Optional[UUID] = None  # The ID of the advisor assigned to the user


class UserConnection(BaseModel):
    """
    Schema for user authentication (login).

    This schema is used when a user tries to log in by providing their email and password.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The plain text password for authentication.
    """
    email: EmailStr  # Email address of the user
    password: str  # Plain text password for login


class UserRead(BaseModel):
    """
    Schema for reading user information.

    This schema is used to return detailed information about a user, including their
    account status, privileges, and personal details.

    Attributes:
        id (UUID): The unique identifier of the user.
        email (EmailStr): The email address of the user.
        is_staff (bool): Indicates if the user has administrative privileges.
        is_active (bool): Indicates if the user's account is active.
        first_connection (bool): Indicates if it is the user's first login.
        first_name (Optional[str]): The user's first name (optional).
        last_name (Optional[str]): The user's last name (optional).
        phone_number (Optional[str]): The user's phone number (optional).
        username (Optional[str]): The username (optional).
        advisor_id (Optional[UUID]): The ID of the user's advisor (optional).
    """
    id: UUID  # Unique identifier for the user
    email: EmailStr  # Email address of the user
    is_staff: bool  # Whether the user has administrative privileges
    is_active: bool  # Whether the user's account is active
    first_connection: bool  # Whether it's the user's first login
    first_name: Optional[str] = None  # First name of the user
    last_name: Optional[str] = None  # Last name of the user
    phone_number: Optional[str] = None  # Phone number of the user
    username: Optional[str] = None  # Username of the user
    advisor_id: Optional[UUID] = None  # Advisor ID for the user (optional)


class UserPasswordUpdate(BaseModel):
    """
    Schema for updating the user's password.

    Attributes:
        new_password (str): The new password for the user.
    """
    new_password: str  # The new password for the user


class UserUpdate(BaseModel):
    """
    Schema for updating user information.

    This schema is used to update the personal details of a user. It allows modifying
    attributes like the first name, last name, phone number, username, and advisor.

    Attributes:
        first_name (Optional[str]): The user's first name (optional).
        last_name (Optional[str]): The user's last name (optional).
        phone_number (Optional[str]): The user's phone number (optional).
        username (Optional[str]): The username of the user (optional).
        advisor_id (Optional[UUID]): The ID of the advisor assigned to the user (optional).
    """
    first_name: Optional[str] = None  # First name of the user
    last_name: Optional[str] = None  # Last name of the user
    phone_number: Optional[str] = None  # Phone number of the user
    username: Optional[str] = None  # Username of the user
    advisor_id: Optional[UUID] = None  # Advisor ID for the user (optional)
