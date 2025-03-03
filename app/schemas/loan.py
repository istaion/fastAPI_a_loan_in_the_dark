from pydantic import BaseModel,  model_validator, EmailStr
from uuid import UUID
from typing import Optional, List
from app.models.loan import StateEnum, NAICSEnum, BankEnum, StatusEnum

class LoanCreate(BaseModel):
    user_email: EmailStr

    state: Optional[StateEnum] = None
    bank: Optional[BankEnum] = None
    naics: Optional[NAICSEnum] = None

    rev_line_cr: Optional[int] = None
    low_doc: Optional[int] = None
    new_exist: Optional[int] = None
    create_job: Optional[int] = None
    retained_job: Optional[int] = None
    has_franchise: Optional[int] = None
    recession: Optional[int] = None
    urban_rural: Optional[int] = None
    no_emp: Optional[int] = None

    term: int
    gr_appv: float

    @model_validator(mode='before')
    def check_values(cls, values):
        # Validation des champs 0, 1, ou null
        for field in ['new_exist', 'has_franchise', 'recession', 'urban_rural','rev_line_cr','low_doc']:
            val = values.get(field)
            if val is not None and val not in [0, 1]:
                raise ValueError(f"{field} must be either 0, 1, or null.")
        
        # Validation des valeurs numériques positives
        for field in ['term', 'no_emp', 'gr_appv', 'retained_job', 'create_job']:
            val = values.get(field)
            if val is not None and val < 0:
                raise ValueError(f"{field} must be a positive number.")
        
        return values

class LoanRead(BaseModel):
    id: UUID
    prediction: int
    proba_yes: float
    proba_no: float
    shap_values: List[float]
    status: StatusEnum
    user_email: EmailStr
    state: Optional[StateEnum] = None
    bank: Optional[BankEnum] = None
    naics: Optional[NAICSEnum] = None
    rev_line_cr: Optional[int] = None
    low_doc: Optional[int] = None
    new_exist: Optional[int] = None
    create_job: Optional[int] = None
    retained_job: Optional[int] = None
    has_franchise: Optional[int] = None
    recession: Optional[int] = None
    urban_rural: Optional[int] = None
    no_emp: Optional[int] = None
    term: int
    gr_appv: float

class AcceptOrRefuseLoan(BaseModel):
    new_status: StatusEnum