from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.api.routers import validation, document

app = FastAPI(
    title="Validation Report Generator and Broker Document Analyzer",
    description="APIs for validation report generator and broker document analyzer",
    version="1.0.0"
)

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(validation.router, prefix="/validation", tags=["Validation Report Generator"])
app.include_router(document.router, prefix="/document", tags=["Broker Document Analyzer"])