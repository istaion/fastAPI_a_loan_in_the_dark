from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.loan import LoanCreate, LoanRead, AcceptOrRefuseLoan, StatusEnum
from app.services.loan import create_loan, get_loan_by_id, get_loan_by_user_id, accept_or_refuse_loan, update_loan_service
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()

@router.post("/create_loan",response_model=LoanRead, status_code=status.HTTP_201_CREATED)
def create_new_loan(loan_create: LoanCreate, db: Session = Depends(get_db)):
    return create_loan(db=db, loan_create=loan_create)

@router.get("/get_loan/{loan_id}",response_model=LoanRead)
def get_loan(loan_id: UUID ,db: Session = Depends(get_db)):
    return get_loan_by_id(db=db, loan_id=loan_id)

@router.get("/get_loan_by_user/{user_id}",response_model=LoanRead)
def get_loan(user_id: UUID ,db: Session = Depends(get_db)):
    return get_loan_by_user_id(db=db, user_id=user_id)

@router.patch("/update_loan/{loan_id}",response_model=LoanRead, status_code=status.HTTP_200_OK)
def update_loan(loan_create: LoanCreate, loan_id: UUID , db: Session = Depends(get_db)):
    return update_loan_service(db=db, loan_id=loan_id ,loan_update=loan_create)

@router.put("/accept_or_refuse_loan/{loan_id}",response_model=dict)
async def put_status_loan(
    status: AcceptOrRefuseLoan,
    loan_id: UUID ,
    db: Session = Depends(get_db)):
    return accept_or_refuse_loan(db=db, loan_id=loan_id, new_status=status.new_status)

