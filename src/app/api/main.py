from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.infrastructure.db import pool
from src.app.api.routers import validation, document, broker
from utils.logging import setup_logger

logger=setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App started")
    yield
    logger.info("Closing Oracle connection pool")
    pool.close()

app = FastAPI(
    title="Validation Report Generator and Broker Template Configuration",
    description="APIs for validation report generator and broker template configuration",
    version="1.0.0",
    lifespan=lifespan
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

app.include_router(validation.router, prefix="/api/validation", tags=["validation-report-generator"])
app.include_router(document.router, prefix="/api/broker", tags=["document-analyzer"])
app.include_router(broker.router, prefix="/api/config", tags=["broker-config"])