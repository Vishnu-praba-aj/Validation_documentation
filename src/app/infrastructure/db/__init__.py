import oracledb
from config.settings import ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN

pool = oracledb.create_pool(
    user=ORACLE_USER,
    password=ORACLE_PASSWORD,
    dsn=ORACLE_DSN,
    min=1,
    max=5,
    increment=1
)