from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional, List, Dict
from enum import Enum
from sqlalchemy import JSON, Column

import cloudpickle
import pandas as pd
import shap
from static.enum import StateEnum, StatusEnum, NAICSEnum

def read_bank_file(file_path: str):
    """
    Reads a list of bank names from a file.

    Args:
        file_path (str): The path to the file containing bank names.

    Returns:
        List[str]: A list of bank names read from the file.
    """
    with open('static/banks_name.str', 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def create_bank_enum(file_path: str):
    """
    Creates an Enum for banks using a file containing bank names.

    Args:
        file_path (str): The path to the file containing bank names.

    Returns:
        Enum: A dynamically created Enum representing banks.
    """
    banks = read_bank_file(file_path)
    return Enum('BankEnum', {bank.replace(" ", "_").upper(): bank for bank in banks})

# Create the Enum for banks from the file
file_path = "banks.txt"
BankEnum = create_bank_enum(file_path)

class Loan(SQLModel, table=True):
    """
    Represents a loan associated with a user.

    Attributes:
        id (UUID): Unique identifier for the loan, generated automatically.
        user_id (UUID): Foreign key linking the loan to a user.
        user (Optional[User]): The user associated with the loan.
        status (StatusEnum): Current status of the loan.
        state (Optional[StateEnum]): The state where the loan is issued (optional).
        bank (Optional[BankEnum]): The bank providing the loan (optional).
        naics (Optional[NAICSEnum]): The NAICS code for the business associated with the loan (optional).
        rev_line_cr (Optional[int]): Revolving line of credit status (0, 1, or null).
        low_doc (Optional[int]): Low documentation requirement (0, 1, or null).
        new_exist (Optional[int]): Indicates if the loan is for a new or existing business (0, 1, or null).
        create_job (Optional[int]): Job creation status (0 or 1).
        has_franchise (Optional[int]): Indicates if the business has a franchise (0 or 1).
        recession (Optional[int]): Indicates if the loan is affected by recession (0 or 1).
        urban_rural (Optional[int]): Indicates whether the loan is from an urban or rural area (0 or 1).
        retained_job (Optional[int]): Retained job status (0 or 1).
        no_emp (Optional[int]): Number of employees (integer).
        term (int): The loan term in months.
        gr_appv (float): The gross approval amount for the loan.
        prediction (Optional[int]): The predicted loan approval outcome (0 or 1).
        proba_yes (Optional[float]): Probability of loan approval (between 0 and 1).
        proba_no (Optional[float]): Probability of loan denial (between 0 and 1).
        shap_values (Optional[List[float]]): SHAP values used to explain the model’s predictions.
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="loans")
    status: StatusEnum = Field(nullable=False, default=StatusEnum.STATUS_TO_TREAT)

    state: Optional[StateEnum] = Field(default=None)
    bank: Optional[BankEnum] = Field(default=None)  # Enum validated against predefined list of banks
    naics: Optional[NAICSEnum] = Field(default=None)

    rev_line_cr: Optional[int] = Field(default=None)  # 0, 1, or null
    low_doc: Optional[int] = Field(default=None)  # 0, 1, or null
    new_exist: Optional[int] = Field(default=None)  # 0, 1, or null
    create_job: Optional[int] = Field(default=None)
    has_franchise: Optional[int] = Field(default=None)
    recession: Optional[int] = Field(default=None)
    urban_rural: Optional[int] = Field(default=None)
    retained_job: Optional[int] = Field(default=None)
    no_emp: Optional[int] = Field(default=None)

    term: int = Field(nullable=False)
    gr_appv: float = Field(nullable=False)

    # Prediction-related Fields
    prediction: Optional[int] = Field(default=None)  # 0 (denied) or 1 (approved)
    proba_yes: Optional[float] = Field(default=None)  # Probability of approval (between 0 and 1)
    proba_no: Optional[float] = Field(default=None)  # Probability of denial (between 0 and 1)
    shap_values: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))

    def get_data(self) -> Dict:
        """
        Returns a dictionary of loan-related data to be used for making predictions.

        Returns:
            dict: A dictionary containing all loan attributes relevant for prediction.
        """
        # If an attribute is missing, it is set to "missing" for consistency.
        if not self.bank:
            bank = "missing"
        else:
            bank = self.bank.value
        if not self.state:
            state = "missing"
        else:
            state = self.state.value
        if not self.naics:
            naics = "missing"
        else:
            naics = self.naics.value
        return {
            "State": state,
            "Bank": bank,
            "NAICS": naics,
            "Term": self.term,
            "NoEmp": self.no_emp,
            "NewExist": self.new_exist,
            "CreateJob": self.create_job,
            "RetainedJob": self.retained_job,
            "UrbanRural": self.urban_rural,
            "RevLineCr": self.rev_line_cr,
            "LowDoc": self.low_doc,
            "GrAppv": self.gr_appv,
            "Recession": self.recession,
            "HasFranchise": self.has_franchise
        }
    
    def make_prediction(self):
        """
        Makes a loan prediction using a pre-trained model and updates the prediction fields.

        This method loads a pre-trained LightGBM model, makes a prediction based on the loan's data,
        and calculates the probabilities of approval and denial. It also computes SHAP values to explain 
        the prediction.

        Returns:
            None
        """
        # Load the pre-trained LightGBM model from a pickle file
        with open('static/lightGBM_model.pkl', "rb") as f:
            model = cloudpickle.load(f)

        # Prepare the loan data for prediction
        df = pd.DataFrame([self.get_data()])

        # Make a binary prediction (0 or 1) and calculate probabilities
        self.prediction = int(model.predict(df)[0])
        proba = model.predict_proba(df)[0]
        self.proba_no = proba[0]  # Probability of denial
        self.proba_yes = proba[1]  # Probability of approval

        # Apply the preprocessor to the data
        transformed_data = model.named_steps['preprocessor'].transform(df.iloc[[0]])

        # Compute SHAP values for model interpretation
        explainer = shap.TreeExplainer(model.named_steps['model'])
        self.shap_values = list(explainer.shap_values(transformed_data)[0])
