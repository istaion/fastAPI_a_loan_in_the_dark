from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.loan import LoanCreate, LoanRead, AcceptOrRefuseLoan, StatusEnum
from app.services.loan import create_loan, get_loan_by_id, get_loan_by_user_id, accept_or_refuse_loan, update_loan_service
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()

@router.post("/create_loan", response_model=LoanRead, status_code=status.HTTP_201_CREATED)
def create_new_loan(loan_create: LoanCreate, db: Session = Depends(get_db)):
    """
    Creates a new loan for a user.

    This function takes in the loan details, checks if the user exists, and creates a new loan entry in the database.

    Args:
        loan_create (LoanCreate): The loan details to create.
        db (Session): The database session, injected by FastAPI.

    Returns:
        LoanRead: The created loan's details.

    Raises:
        HTTPException: If the user doesn't exist or if a loan already exists for the user.
    """
    return create_loan(db=db, loan_create=loan_create)

@router.get("/get_loan/{loan_id}", response_model=LoanRead)
def get_loan(loan_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieves the loan details by loan ID.

    This function returns the details of a specific loan using its unique identifier.

    Args:
        loan_id (UUID): The ID of the loan to retrieve.
        db (Session): The database session, injected by FastAPI.

    Returns:
        LoanRead: The loan details.
    
    Raises:
        HTTPException: If the loan is not found.
    """
    return get_loan_by_id(db=db, loan_id=loan_id)

@router.get("/get_loan_by_user/{user_id}", response_model=LoanRead)
def get_loan(user_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieves the loan details by user ID.

    This function fetches the loan associated with a specific user using the user's unique identifier.

    Args:
        user_id (UUID): The ID of the user whose loan to retrieve.
        db (Session): The database session, injected by FastAPI.

    Returns:
        LoanRead: The loan details for the user.
    
    Raises:
        HTTPException: If the user does not have any loans.
    """
    return get_loan_by_user_id(db=db, user_id=user_id)

@router.patch("/update_loan/{loan_id}", response_model=LoanRead, status_code=status.HTTP_200_OK)
def update_loan(loan_create: LoanCreate, loan_id: UUID, db: Session = Depends(get_db)):
    """
    Updates an existing loan with new details.

    This function updates the details of an existing loan (e.g., bank, state, etc.) based on the loan ID.

    Args:
        loan_create (LoanCreate): The new loan details to update.
        loan_id (UUID): The ID of the loan to update.
        db (Session): The database session, injected by FastAPI.

    Returns:
        LoanRead: The updated loan details.
    
    Raises:
        HTTPException: If the loan does not exist.
    """
    return update_loan_service(db=db, loan_id=loan_id, loan_update=loan_create)

@router.put("/accept_or_refuse_loan/{loan_id}", response_model=dict)
async def put_status_loan(
    status: AcceptOrRefuseLoan,
    loan_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Accepts or refuses a loan based on the given status.

    This function allows a staff member to update the loan status, either accepting or refusing the loan.

    Args:
        status (AcceptOrRefuseLoan): The new loan status (accept or refuse).
        loan_id (UUID): The ID of the loan to update.
        db (Session): The database session, injected by FastAPI.

    Returns:
        dict: A message indicating the updated loan status.
    
    Raises:
        HTTPException: If the loan is not found.
    """
    return accept_or_refuse_loan(db=db, loan_id=loan_id, new_status=status.new_status)
