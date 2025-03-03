from fastapi import FastAPI
from app.routes import auth, user, loan
from app.database import engine
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Loan API", description="API de gestion des prêts bancaires", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],  # L'URL de votre Django
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
tags_metadata = [
    {"name": "Auth", "description": "Routes d'authentification"},
    {"name": "Users", "description": "Gestion des utilisateurs"},
    {"name": "Loans", "description": "Gestion des demandes de prêts"},
]

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="", tags=["Users"])
app.include_router(loan.router, prefix="/loans", tags=["Loans"])