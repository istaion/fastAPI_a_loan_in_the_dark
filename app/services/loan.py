from app.models.user import User
from app.models.loan import Loan, StatusEnum
from app.schemas.loan import LoanCreate, LoanRead, AcceptOrRefuseLoan
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

def create_loan(db: Session, loan_create: LoanCreate) -> None:
    user = db.query(User).filter(User.email == loan_create.user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not in the db",
        )
    # Check if loan already created
    db_loan = db.query(Loan).filter(Loan.user_id == user.id).first()
    if db_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan already created",
        )
    
    # Create a new loan
    db_loan = Loan(
        user_id = user.id,
        user = user,
        status = StatusEnum.STATUS_TO_TREAT,
        state = loan_create.state,
        bank = loan_create.bank,
        naics = loan_create.naics,
        rev_line_cr = loan_create.rev_line_cr,
        low_doc = loan_create.low_doc,
        new_exist = loan_create.new_exist,
        create_job = loan_create.create_job,
        has_franchise= loan_create.has_franchise,
        recession=loan_create.recession,
        urban_rural=loan_create.urban_rural,
        term = loan_create.term,
        no_emp= loan_create.no_emp,
        gr_appv=loan_create.gr_appv,
        retained_job=loan_create.retained_job
    )

    db_loan.make_prediction()
    
    # Save user to the database
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)

    return get_loan_by_id(db=db,loan_id=db_loan.id)


def get_loan_by_id(db:Session, loan_id:UUID):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    return LoanRead(
        id = db_loan.id,
        user_email= db_loan.user.email,
        prediction = db_loan.prediction,
        proba_yes = db_loan.proba_yes,
        proba_no = db_loan.proba_no,
        shap_values = db_loan.shap_values,
        status=db_loan.status,
        state = db_loan.state,
        bank = db_loan.bank,
        naics = db_loan.naics,
        rev_line_cr = db_loan.rev_line_cr,
        low_doc = db_loan.low_doc,
        new_exist = db_loan.new_exist,
        create_job = db_loan.create_job,
        has_franchise = db_loan.has_franchise,
        recession = db_loan.recession,
        urban_rural = db_loan.urban_rural,
        term = db_loan.term,
        no_emp = db_loan.no_emp,
        gr_appv = db_loan.gr_appv,
        retained_job = db_loan.retained_job
    )

def get_loan_by_user_id(db:Session, user_id:UUID):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_loan = db_user.loans[0]
    return LoanRead(
        id = db_loan.id,
        user_email= db_loan.user.email,
        prediction = db_loan.prediction,
        proba_yes = db_loan.proba_yes,
        proba_no = db_loan.proba_no,
        shap_values = db_loan.shap_values,
        status=db_loan.status,
        state = db_loan.state,
        bank = db_loan.bank,
        naics = db_loan.naics,
        rev_line_cr = db_loan.rev_line_cr,
        low_doc = db_loan.low_doc,
        new_exist = db_loan.new_exist,
        create_job = db_loan.create_job,
        has_franchise = db_loan.has_franchise,
        recession = db_loan.recession,
        urban_rural = db_loan.urban_rural,
        term = db_loan.term,
        no_emp = db_loan.no_emp,
        gr_appv = db_loan.gr_appv,
        retained_job = db_loan.retained_job
    )

def accept_or_refuse_loan(db: Session, loan_id: UUID, new_status: StatusEnum):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    loan.status = new_status
    db.add(loan)
    db.commit()
    db.refresh(loan)
    
    return {"message": f"Loan status updated to {new_status}"}

def update_loan_service(db: Session, loan_id: UUID, loan_update: LoanCreate) -> None:
    user = db.query(User).filter(User.email == loan_update.user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not in the db",
        )
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not db_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan not found",
        )

    db_loan.state = loan_update.state
    db_loan.bank = loan_update.bank
    db_loan.naics = loan_update.naics
    db_loan.rev_line_cr = loan_update.rev_line_cr
    db_loan.low_doc = loan_update.low_doc
    db_loan.new_exist = loan_update.new_exist
    db_loan.create_job = loan_update.create_job
    db_loan.has_franchise = loan_update.has_franchise
    db_loan.recession = loan_update.recession
    db_loan.urban_rural = loan_update.urban_rural
    db_loan.term = loan_update.term
    db_loan.no_emp = loan_update.no_emp
    db_loan.gr_appv = loan_update.gr_appv
    db_loan.retained_job = loan_update.retained_job

    db_loan.make_prediction()
    
    # Save user to the database
    db.commit()
    db.refresh(db_loan)

    return get_loan_by_id(db=db,loan_id=db_loan.id)