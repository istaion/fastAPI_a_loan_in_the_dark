from pydantic import BaseModel, model_validator, EmailStr
from uuid import UUID
from typing import Optional, List
from app.models.loan import StateEnum, NAICSEnum, BankEnum, StatusEnum

class LoanCreate(BaseModel):
    """
    Schema for creating a new loan.

    This schema defines the fields required to create a new loan entry in the system.
    It validates the input data before it is passed to the database.

    Attributes:
        user_email (EmailStr): The email address of the user requesting the loan.
        state (Optional[StateEnum]): The state where the loan is issued (optional).
        bank (Optional[BankEnum]): The bank providing the loan (optional).
        naics (Optional[NAICSEnum]): The NAICS code for the business associated with the loan (optional).
        rev_line_cr (Optional[int]): Revolving line of credit status (0, 1, or null).
        low_doc (Optional[int]): Low documentation requirement (0, 1, or null).
        new_exist (Optional[int]): New or existing business (0, 1, or null).
        create_job (Optional[int]): Job creation status (0 or 1).
        retained_job (Optional[int]): Retained job status (0 or 1).
        has_franchise (Optional[int]): Indicates if the business has a franchise (0 or 1).
        recession (Optional[int]): Indicates if the loan is affected by recession (0 or 1).
        urban_rural (Optional[int]): Urban or rural area (0 or 1).
        no_emp (Optional[int]): Number of employees (integer).
        term (int): The loan term in months.
        gr_appv (float): The gross approval amount for the loan.
    """

    user_email: EmailStr  # Email of the user applying for the loan

    state: Optional[StateEnum] = None  # Optional state where the loan is being issued
    bank: Optional[BankEnum] = None  # Optional bank providing the loan
    naics: Optional[NAICSEnum] = None  # Optional NAICS code for the business

    rev_line_cr: Optional[int] = None  # Revolving line of credit status (0, 1, or null)
    low_doc: Optional[int] = None  # Low documentation requirement (0, 1, or null)
    new_exist: Optional[int] = None  # New or existing business (0, 1, or null)
    create_job: Optional[int] = None  # Job creation status (0 or 1)
    retained_job: Optional[int] = None  # Retained job status (0 or 1)
    has_franchise: Optional[int] = None  # Indicates if the business has a franchise (0 or 1)
    recession: Optional[int] = None  # Indicates if the loan is affected by recession (0 or 1)
    urban_rural: Optional[int] = None  # Urban or rural area (0 or 1)
    no_emp: Optional[int] = None  # Number of employees (integer)

    term: int  # Loan term in months
    gr_appv: float  # Gross approval amount for the loan

    @model_validator(mode='before')
    def check_values(cls, values):
        """
        Validates the values of the fields before processing.

        This method ensures that:
        - Fields with values 0 or 1 (e.g., new_exist, has_franchise) are restricted to those values or null.
        - Numerical fields (e.g., term, gr_appv) are positive numbers.

        Args:
            cls (Type[BaseModel]): The class that is being validated.
            values (dict): The values being validated.

        Returns:
            dict: The validated values.
        
        Raises:
            ValueError: If any validation fails.
        """
        # Validate fields that must be either 0, 1, or null
        for field in ['new_exist', 'has_franchise', 'recession', 'urban_rural', 'rev_line_cr', 'low_doc']:
            val = values.get(field)
            if val is not None and val not in [0, 1]:
                raise ValueError(f"{field} must be either 0, 1, or null.")
        
        # Validate that numerical fields are positive
        for field in ['term', 'no_emp', 'gr_appv', 'retained_job', 'create_job']:
            val = values.get(field)
            if val is not None and val < 0:
                raise ValueError(f"{field} must be a positive number.")
        
        return values

class LoanRead(BaseModel):
    """
    Schema for reading loan details.

    This schema is used to return detailed information about a loan,
    including the prediction results and the model's explanation.

    Attributes:
        id (UUID): Unique identifier for the loan.
        prediction (int): Predicted loan approval (0 or 1).
        proba_yes (float): Probability of loan approval (between 0 and 1).
        proba_no (float): Probability of loan denial (between 0 and 1).
        shap_values (List[float]): SHAP values explaining the model’s decision.
        status (StatusEnum): Current status of the loan.
        user_email (EmailStr): Email address of the user associated with the loan.
        state (Optional[StateEnum]): The state where the loan is issued (optional).
        bank (Optional[BankEnum]): The bank providing the loan (optional).
        naics (Optional[NAICSEnum]): The NAICS code for the business (optional).
        rev_line_cr (Optional[int]): Revolving line of credit status (0, 1, or null).
        low_doc (Optional[int]): Low documentation requirement (0, 1, or null).
        new_exist (Optional[int]): New or existing business (0, 1, or null).
        create_job (Optional[int]): Job creation status (0 or 1).
        retained_job (Optional[int]): Retained job status (0 or 1).
        has_franchise (Optional[int]): Indicates if the business has a franchise (0 or 1).
        recession (Optional[int]): Indicates if the loan is affected by recession (0 or 1).
        urban_rural (Optional[int]): Urban or rural area (0 or 1).
        no_emp (Optional[int]): Number of employees (integer).
        term (int): Loan term in months.
        gr_appv (float): Gross approval amount for the loan.
    """

    id: UUID  # Unique identifier for the loan
    prediction: int  # Predicted loan approval outcome (0 or 1)
    proba_yes: float  # Probability of approval (between 0 and 1)
    proba_no: float  # Probability of denial (between 0 and 1)
    shap_values: List[float]  # SHAP values for explaining the model’s predictions
    status: StatusEnum  # Current status of the loan
    user_email: EmailStr  # Email of the user requesting the loan
    state: Optional[StateEnum] = None  # Optional state where the loan is issued
    bank: Optional[BankEnum] = None  # Optional bank providing the loan
    naics: Optional[NAICSEnum] = None  # Optional NAICS code for the business
    rev_line_cr: Optional[int] = None  # Revolving line of credit status
    low_doc: Optional[int] = None  # Low documentation requirement
    new_exist: Optional[int] = None  # New or existing business
    create_job: Optional[int] = None  # Job creation status
    retained_job: Optional[int] = None  # Retained job status
    has_franchise: Optional[int] = None  # Franchise status
    recession: Optional[int] = None  # Recession impact status
    urban_rural: Optional[int] = None  # Urban or rural area
    no_emp: Optional[int] = None  # Number of employees
    term: int  # Loan term in months
    gr_appv: float  # Gross approval amount

class AcceptOrRefuseLoan(BaseModel):
    """
    Schema for accepting or refusing a loan.

    This schema contains the new status of a loan (either accepted or refused).

    Attributes:
        new_status (StatusEnum): The new status of the loan (either ACCEPTED or REFUSED).
    """

    new_status: StatusEnum  # The new status of the loan (ACCEPTED or REFUSED)
