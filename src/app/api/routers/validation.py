import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Form
from src.app.domain.exception import InvalidJSONResponseException, RepoProcessingException
from src.app.api.deps import get_validation_service
from src.app.domain.models import ValidationLLMResponse
from utils.logging import setup_logger

router = APIRouter()
logger = setup_logger()

@router.post(
    "/analyze_repo/",
    response_model=ValidationLLMResponse,
    operation_id="analyze-repository"
)
async def analyze_repo(
    repo_url: str = Form(...),
    service=Depends(get_validation_service)
):
    try:
        start = time.perf_counter()
        result = service.analyze_repo(repo_url)
        end = time.perf_counter()
        logger.info(f"Repo analysis completed in {end - start:.2f} seconds")
        return result
    except RepoProcessingException as e:
        logger.error(f"Validation endpoint client error (RepoProcessing): {str(e)}")
        raise HTTPException(status_code=400, detail=e.detail)
    except InvalidJSONResponseException as e:
        logger.error(f"Validation endpoint client exception (InvalidJSONResponse): {str(e)}")
        raise HTTPException(status_code=502, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unexpected server error")
