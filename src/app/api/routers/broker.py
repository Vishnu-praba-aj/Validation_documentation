import time
from fastapi import APIRouter, Depends, HTTPException
from src.app.domain.exception import TableMissingException, BrokersNotFoundException, OracleQueryException, TableMissingException
from src.app.application.services.broker_service import BrokerService
from src.app.api.deps import get_broker_service
from utils.logging import setup_logger

logger = setup_logger()
router = APIRouter()

@router.get("/brokers/", operation_id="get-all-brokers")
def get_all_brokers(service: BrokerService = Depends(get_broker_service)):
    try:
        start=time.perf_counter()
        brokers= service.fetch_all_brokers()
        end=time.perf_counter()
        logger.info(f"All brokers extracted in {end-start:.2f} seconds")
        return {"broker": brokers}
    except BrokersNotFoundException as e:
        logger.error(f"Broker endpoint client error (BrokersNotFound): {str(e)}")
        raise HTTPException(status_code=404, detail=e.detail)
    except TableMissingException as e:
        logger.error(f"Broker endpoint client error (BrokerTableMissing): {str(e)}")
        raise HTTPException(status_code=500, detail=e.detail)
    except OracleQueryException as e:
        logger.error(f"Broker endpoint client error (OracleQuery): {str(e)}")
        raise HTTPException(status_code=502, detail=e.detail)
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server error")