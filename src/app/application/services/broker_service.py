from src.app.domain.exception import ResourceNotFoundException, UniqueIdExistsException
from src.app.domain.models import AllBrokers
from src.app.infrastructure.db.broker_dao import BrokerDAO

class BrokerService:
    def __init__(self, dao: BrokerDAO):
        self.dao=dao

    def fetch_all_brokers(self):
        brokers=self.dao.get_all_brokers()
        return AllBrokers(broker=brokers)
    
    def is_unique_id_present(self, broker_code: str, unique_id: str):
        status = self.dao.check_unique_id_exists(broker_code, unique_id)

        if status == "BROKER_NOT_FOUND":
            raise ResourceNotFoundException("Broker not found in Broker Reference table")
        elif status == "UNIQUE_ID_EXISTS":
            raise UniqueIdExistsException()
        return {"can_proceed":True}
