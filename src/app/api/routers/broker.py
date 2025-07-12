import time
from fastapi import APIRouter, Depends, Form, HTTPException
from src.app.domain.models import AllBrokers, BrokerConfig, BrokerTemplateInfo, InsertConfigRequest
from src.app.domain.exception import DBQueryException, ResourceNotFoundException, TableMissingException, UniqueIdExistsException, VersionConflictException
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
    
@router.post(
    "/unique_id_exists/", 
    operation_id="check-unique-id"
)
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

@router.post(
    "/insert_config/",
    operation_id="insert-broker-config"
)
async def insert_config(
    request: InsertConfigRequest,
    service=Depends(get_broker_service)
):
    try:
        logger.info(f"Received request to insert config for broker: {request.broker_code}")
        start = time.perf_counter()
        service.insert_template(request.broker_code,request.response)
        end = time.perf_counter()
        logger.info(f"New config inserted in {end - start:.2f} seconds")
        return {"message": "Configuration inserted successfully"}
    except UniqueIdExistsException as e:
        logger.error(f"Insert New Config endpoint client exception (UniqueIdExists): {str(e)}")
        raise HTTPException(status_code=409, detail=e.detail)
    except ResourceNotFoundException as e:
        logger.error(f"Insert New Config endpoint client exception: {str(e)}")
        raise HTTPException(status_code=404, detail=e.detail)
    except TableMissingException as e:
        logger.error(f"Insert New Config endpoint client exception (TableMissing): {str(e)}")
        raise HTTPException(status_code=500, detail=e.detail)
    except DBQueryException as e:
        logger.error(f"Insert New Config endpoint client exception (DBQuery): {str(e)}")
        raise HTTPException(status_code=502, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unexpected server error")
    
@router.post(
    "/template_info/", 
    response_model=BrokerTemplateInfo,
    operation_id="get-template-info"
)
async def get_template_info(
    broker_code: str = Form(...),
    service: BrokerService = Depends(get_broker_service)
):
    try:
        result=service.get_broker_template_info(broker_code)
        return result
    except ResourceNotFoundException as e:
        logger.error(f"Template info error (BrokerNotFound): {str(e)}")
        raise HTTPException(status_code=404, detail=e.detail)
    except TableMissingException as e:
        logger.error(f"Template info error (TableMissing): {str(e)}")
        raise HTTPException(status_code=500, detail=e.detail)
    except DBQueryException as e:
        logger.error(f"Template info error (DBQuery): {str(e)}")
        raise HTTPException(status_code=502, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unexpected server error")
    
@router.get(
    "/get_config",
    response_model=BrokerConfig,
    operation_id="get-broker-config"
)
async def get_config(
    broker_code: str,
    broker_template_no: int,
    service: BrokerService = Depends(get_broker_service)
):
    try:
        return service.get_broker_config(broker_code, broker_template_no)
    except ResourceNotFoundException as e:
        logger.error(f"Broker config not found: {str(e)}")
        raise HTTPException(status_code=404, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unexpected server error")

@router.post(
    "/update-config",
    operation_id="update-broker-config"
)
async def update_config(
    request: BrokerConfig,
    service: BrokerService = Depends(get_broker_service)
):
    try:
        logger.info(f"Received request to update config for broker: {request.broker_code}")
        start = time.perf_counter()
        result = service.update_broker_config(request)
        end = time.perf_counter()
        logger.info(f"Config updated in {end - start:.2f} seconds")
        return result
    except ResourceNotFoundException as e:
        logger.error(f"Update config client endpoint error (UniqueIDNotFound): {str(e)}")
        raise HTTPException(status_code=404, detail=e.detail)
    except TableMissingException as e:
        logger.error(f"Update config client endpoint error (TableMissing): {str(e)}")
        raise HTTPException(status_code=500, detail=e.detail)
    except DBQueryException as e:
        logger.error(f"Update config client endpoint error (DBQuery): {str(e)}")
        raise HTTPException(status_code=502, detail=e.detail)
    except VersionConflictException as e:
        logger.error(f"Update config client endpoint error (VersionConflict): {str(e)}")
        raise HTTPException(status_code=409, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unexpected server error")