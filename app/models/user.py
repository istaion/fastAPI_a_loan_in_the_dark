from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import uuid4, UUID
import bcrypt
from app.models.loan import Loan

class User(SQLModel, table=True):
    """
    Represents a user in the system.

    Attributes:
        id (UUID): Unique identifier for the user, automatically generated.
        email (str): User's email address. This must be unique.
        hashed_password (str): Hashed version of the user's password for authentication.
        is_staff (bool): Indicates whether the user has administrative privileges (staff).
        is_active (bool): Indicates if the user's account is currently active.
        first_connection (bool): Indicates whether the user is logging in for the first time.
        loans (List[Loan]): List of loans associated with the user (one-to-many relationship).
        first_name (Optional[str]): First name of the user (optional).
        last_name (Optional[str]): Last name of the user (optional).
        username (Optional[str]): The name of the user's company (optional, represents the client's company name).
        phone_number (Optional[str]): Phone number of the user (optional).
        advisor_id (Optional[UUID]): Foreign key linking the user to an advisor (optional).
        advisor (Optional[User]): The advisor associated with the user (self-referential relationship).
        users (List[User]): List of users assigned to an advisor (one-to-many relationship).
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_staff: bool = Field(default=False)
    is_active: bool = Field(default=False)
    first_connection: bool = Field(default=True)
    loans: List["Loan"] = Relationship(back_populates="user")
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)  # Represents the name of the user's company
    phone_number: Optional[str] = Field(default=None)

    # One-to-many relationship: An advisor can have multiple users to advise.
    advisor_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    advisor: Optional["User"] = Relationship(back_populates="users", sa_relationship_kwargs={"remote_side": "User.id"})

    # List of users associated with an advisor (one-to-many relationship).
    users: List["User"] = Relationship(back_populates="advisor")

    def verify_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the stored hashed password.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a given password using bcrypt to securely store it.

        Args:
            password (str): The plaintext password to hash.

        Returns:
            str: The hashed password as a string.
        """
        salt = bcrypt.gensalt()  # Generate a salt for hashing
        hashed = bcrypt.hashpw(password.encode(), salt)  # Hash the password with the salt
        return hashed.decode()  # Return the hashed password as a string
