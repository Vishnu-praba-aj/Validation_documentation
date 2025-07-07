import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.app.domain.exception import RepoProcessingException
from src.app.api.deps import get_validation_service
from src.app.domain.models import ValidationLLMResponse
from utils.logging import setup_logger

router = APIRouter()
logger = setup_logger()

class ValidationRequest(BaseModel):
    repo_url: str

@router.post(
    "/analyze_repo/",
    response_model=ValidationLLMResponse,
    operation_id="analyzeRepository"
)
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
    except RepoProcessingException as e:
        logger.error(f"Validation endpoint client error (RepoProcessingException): {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Validation endpoint unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500,detail=str(e))