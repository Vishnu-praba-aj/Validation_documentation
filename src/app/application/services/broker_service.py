from src.app.infrastructure.db.broker_dao import BrokerDAO

class BrokerService:
    def __init__(self, dao: BrokerDAO):
        self.dao = dao

    def fetch_all_brokers(self):
        return self.dao.get_all_brokers()
