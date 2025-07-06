import time
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from src.app.api.deps import get_document_service
from src.app.domain.models import ExtractionLLMResponse
from utils.logging import setup_logger

router = APIRouter()
logger = setup_logger()

@router.post("/extract_fields/", response_model=ExtractionLLMResponse)
async def extract_fields(
    doc: UploadFile = File(...),
    custom_fields: UploadFile = File(...),
    user_prompt: str = Form(""),
    service=Depends(get_document_service)
):
    try:
        logger.info("Received request for extracting fields")
        start = time.perf_counter()
        doc_bytes = await doc.read()
        fields_bytes = await custom_fields.read()
        fields = [line.strip() for line in fields_bytes.decode("utf-8").splitlines() if line.strip()]
        result = service.extract_fields(doc_bytes, doc.filename, fields, user_prompt)
        logger.info("Successfully extracted fields")
        end = time.perf_counter()
        logger.info(f"Field extraction completed in {end - start:.2f} seconds")
        return result
    except Exception as e:
        logger.error(f"Extraction endpoint error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/continue_chat/")
async def continue_chat(
    session_id: str = Form(...),
    prompt: str = Form(...),
    service=Depends(get_document_service)
):
    try:
        start = time.perf_counter()
        result = service.continue_chat(session_id, prompt)
        end = time.perf_counter()
        logger.info(f"Chat continuation completed in {end - start:.2f} seconds")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))