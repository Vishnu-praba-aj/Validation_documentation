import oracledb
from src.app.domain.exception import BrokersNotFoundException, OracleQueryException, TableMissingException

class BrokerDAO:
    def __init__(self, pool: oracledb.ConnectionPool):
        self.pool = pool

    def get_all_brokers(self):
        query = "select broker_cd, broker_nm FROM tps2_brokers_dref"
        try:
            with self.pool.acquire() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    if not rows:
                        raise BrokersNotFoundException()
                    return [{"broker-code": code, "broker-name": name} for code, name in rows]
        except oracledb.DatabaseError as e:
            if "ORA-00942" in str(e):
                raise TableMissingException("Broker Reference table not found")
            raise OracleQueryException()
