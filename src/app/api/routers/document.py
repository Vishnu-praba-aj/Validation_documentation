import time
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from src.app.domain.exception import FileTooLargeException, InvalidFileTypeException, InvalidJSONResponseException, JSONParsingException, SessionNotFoundException
from src.app.api.deps import get_document_service
from src.app.domain.models import ExtractionLLMResponse
from utils.logging import setup_logger

router = APIRouter()
logger = setup_logger()

@router.post(
    "/extract_fields/", 
    response_model=ExtractionLLMResponse,
    operation_id="extractDocumentFields"
)
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
    except FileTooLargeException as e:
        logger.error(f"Extraction endpoint client exception (FileTooLarge): {str(e)}")
        raise HTTPException(status_code=413, detail=e.detail)
    except InvalidFileTypeException as e:
        logger.error(f"Extraction endpoint client exception (InvalidFileType): {str(e)}")
        raise HTTPException(status_code=415, detail=e.detail)
    except InvalidJSONResponseException as e:
        logger.error(f"Extraction endpoint client exception (InvalidJSONResponse): {str(e)}")
        raise HTTPException(status_code=502, detail=e.detail)
    except JSONParsingException as e:
        logger.error(f"Extraction endpoint client exception (JSONParsing): {str(e)}")
        raise HTTPException(status_code=400, detail=e.detail)
    except Exception as e:
        logger.error(f"Extraction endpoint unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.post(
    "/continue_chat/",
    response_model=ExtractionLLMResponse,
    operation_id="continueChat"
)
async def continue_chat(
    session_id: str = Form(...),
    prompt: str = Form(...),
    service=Depends(get_document_service)
):
    try:
        start = time.perf_counter()
        logger.info(f"Chat continuation initiated")
        result = service.continue_chat(session_id, prompt)
        end = time.perf_counter()
        logger.info(f"Chat continuation completed in {end - start:.2f} seconds")
        return result
    except SessionNotFoundException as e:
        logger.error(f"Chat continuation endpoint client exception (SessionNotFound): {str(e)}")
        raise HTTPException(status_code=404, detail=e.detail)
    except InvalidJSONResponseException as e:
        logger.error(f"Chat continuation endpoint client exception (InvalidJSONResponse): {str(e)}")
        raise HTTPException(status_code=502, detail=e.detail)
    except JSONParsingException as e:
        logger.error(f"Chat continuation endpoint client exception (JSONParsing): {str(e)}")
        raise HTTPException(status_code=400, detail=e.detail)
    except Exception as e:
        logger.error(f"Chat continuation unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")