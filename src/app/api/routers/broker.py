import time
from fastapi import APIRouter, Depends, Form, HTTPException
from src.app.domain.models import AllBrokers
from src.app.domain.exception import DBQueryException, ResourceNotFoundException, TableMissingException, UniqueIdExistsException
from src.app.application.services.broker_service import BrokerService
from src.app.api.deps import get_broker_service
from utils.logging import setup_logger

logger = setup_logger()
router = APIRouter()

@router.get(
    "/brokers/", 
    operation_id="get-all-brokers",
    response_model=AllBrokers
)
async def get_all_brokers(service: BrokerService = Depends(get_broker_service)):
    try:
        start=time.perf_counter()
        brokers=service.fetch_all_brokers()
        end=time.perf_counter()
        logger.info(f"All brokers extracted in {end-start:.2f} seconds")
        return brokers
    except ResourceNotFoundException as e:
        logger.error(f"Get all brokers endpoint client exception (BrokersNotFound): {str(e)}")
        raise HTTPException(status_code=404, detail=e.detail)
    except TableMissingException as e:
        logger.error(f"Get all brokers endpoint client exception (TableMissing): {str(e)}")
        raise HTTPException(status_code=500, detail=e.detail)
    except DBQueryException as e:
        logger.error(f"Get all brokers endpoint client exception (DBQuery): {str(e)}")
        raise HTTPException(status_code=502, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unexpected server error")
    
@router.post("/brokers/unique-id-exists/", operation_id="check-unique-id")
async def check_unique_id(
    broker_code: str = Form(...),
    unique_id: str = Form(...),
    service: BrokerService = Depends(get_broker_service)
):
    try:
        return service.is_unique_id_present(broker_code, unique_id)
    except UniqueIdExistsException as e:
        logger.error(f"Check unique ID endpoint client exception (UniqueIdExists): {str(e)}")
        raise HTTPException(status_code=409, detail=e.detail)
    except ResourceNotFoundException as e:
        logger.error(f"Check unique ID endpoint client exception (BrokerNotFound): {str(e)}")
        raise HTTPException(status_code=404, detail=e.detail)
    except TableMissingException as e:
        logger.error(f"Check unique ID endpoint client exception (TableMissing): {str(e)}")
        raise HTTPException(status_code=500, detail=e.detail)
    except DBQueryException as e:
        logger.error(f"Check unique ID endpoint client exception (DBQuery): {str(e)}")
        raise HTTPException(status_code=502, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unexpected server error")