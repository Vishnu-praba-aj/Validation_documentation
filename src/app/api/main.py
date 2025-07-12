from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import oracledb
from config.settings import ORACLE_DSN, ORACLE_PASSWORD, ORACLE_USER
from src.app.api.routers import validation, document, broker
from utils.logging import setup_logger

logger=setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating Oracle connection pool...")
    app.state.pool = oracledb.create_pool(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN,
        min=1,
        max=5,
        increment=1
    )
    logger.info("App started with Oracle pool.")
    yield
    logger.info("Closing Oracle connection pool...")
    app.state.pool.close()
    logger.info("Pool closed.")

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

app.include_router(validation.router, prefix="/api/validation", tags=["Validation Report Generator"])
app.include_router(broker.router, prefix="/api/broker/config", tags=["Broker Configuration"])
app.include_router(document.router, prefix="/api/broker/template", tags=["Broker Template Analyzer"])
