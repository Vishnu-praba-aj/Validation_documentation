import oracledb
from src.app.domain.exception import DBQueryException, ResourceNotFoundException, TableMissingException

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
                        raise ResourceNotFoundException("No brokers in broker reference table")
                    return [{"broker_code": code, "broker_name": name} for code, name in rows]
        except oracledb.DatabaseError as e:
            if "ORA-00942" in str(e):
                raise TableMissingException("Broker Reference table not found")
            raise DBQueryException()
        
    def check_unique_id_exists(self, broker_code: str, unique_id: str) -> str:
        query = """
        select 
            case 
                when not exists(select 1 from tps2_brokers_dref where broker_cd=:broker_code) then 'BROKER_NOT_FOUND'
                when exists(select 1 from tps2_brokers_format_dref where broker_cd=:broker_code and unique_id=:unique_id) then 'UNIQUE_ID_EXISTS'
                else 'OK'
            end as status
        from dual"""
        try:
            with self.pool.acquire() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query,{"broker_code": broker_code, "unique_id": unique_id})
                    return cursor.fetchone()[0]
        except oracledb.DatabaseError as e:
            if "ORA-00942" in str(e):
                raise TableMissingException("Broker or Broker Format Reference table not found")
            raise DBQueryException(str(e))
