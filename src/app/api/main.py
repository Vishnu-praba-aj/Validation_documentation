from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.api.routers import validation, document

app = FastAPI(
    title="AI Repository Validation and Document Extraction",
    description="Backend for validation and document extraction using Gemini 1.5 Flash",
    version="1.0.0"
)

origins = [
    "http://localhost:4200"
    # Add your deployed frontend URL(s) here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(validation.router, prefix="/validation", tags=["validation"])
app.include_router(document.router, prefix="/document", tags=["document"])