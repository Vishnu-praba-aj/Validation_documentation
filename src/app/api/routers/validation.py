import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.app.api.deps import get_validation_service
from src.app.domain.models import ValidationLLMResponse
from utils.logging import setup_logger

router = APIRouter()
logger = setup_logger()

class ValidationRequest(BaseModel):
    repo_url: str

@router.post("/analyze_repo/", response_model=ValidationLLMResponse)
async def analyze_repo(
    req: ValidationRequest,
    service=Depends(get_validation_service)
):
    try:
        start = time.perf_counter()
        result = service.analyze_repo(req.repo_url)
        end = time.perf_counter()
        logger.info(f"Repo analysis completed in {end - start:.2f} seconds")
        return result
    except HTTPException as e:
        logger.error(f"Validation endpoint error: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")