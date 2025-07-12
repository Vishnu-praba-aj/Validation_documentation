import oracledb
from src.app.domain.models import BrokerConfig
from src.app.domain.exception import DBQueryException, ResourceNotFoundException, TableMissingException, UniqueIdExistsException, VersionConflictException

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
            raise DBQueryException(str(e))
        
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

    def insert_broker_config(self, broker_code: str, response: BrokerConfig):
        try:
            with self.pool.acquire() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("select no_format from tps2_brokers_dref where broker_cd=:1 for update",[broker_code])
                    row = cursor.fetchone()
                    if not row:
                        raise ResourceNotFoundException("Broker not found in Broker Reference table")
                    new_total_format=row[0]+1
                    cursor.execute("update tps2_brokers_dref set no_format=:1 where broker_cd=:2",(new_total_format,broker_code))

                    fields=response.rows[0].fields
                    unique_id = next((f.document_label for f in fields if f.custom_field == "unique_identifier"), None)
                    if not unique_id:
                        raise ResourceNotFoundException("Unique identifier not found in Response")
                    status = self.check_unique_id_exists(broker_code, unique_id)
                    if status == "UNIQUE_ID_EXISTS":
                        raise UniqueIdExistsException()
                    elif status == "BROKER_NOT_FOUND":
                        raise ResourceNotFoundException("Broker not found in Broker Reference table")
                    cursor.execute(
                        "insert into tps2_brokers_format_dref (broker_cd, broker_format_nm, version, unique_id) VALUES (:1, :2, 1, :3)",
                        (broker_code, new_total_format, unique_id)
                    )

                    for field in fields:
                        metadata = field.metadata or {}
                        metadata = metadata.model_dump()
                        param_nm = field.custom_field or ""
                        param_ref_txt = field.document_label or ""

                        cursor.execute("""
                            insert into tps2_mnt_brokers_conf_fldsmap (
                                broker_cd, broker_format_nm, version,
                                param_nm, param_ref_txt,
                                start_index_nbr, end_index_nbr,
                                row_adder_cnt, col_adder_cnt,
                                param_ref_delim_txt, param_value_pos_cd,
                                unit_price_pct_ind, param_nm_occur_ind,
                                date_format_cd, decimal_separator_cd,
                                param_def_value_txt, derivation_col,
                                operations_seq, param_val_fn_txt
                            ) 
                            values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17,:18, :19)
                        """, (
                            broker_code, new_total_format, 1,
                            param_nm, param_ref_txt,
                            metadata.get("start_index_nbr"),
                            metadata.get("end_index_nbr"),
                            metadata.get("row_adder_cnt"),
                            metadata.get("col_adder_cnt"),
                            metadata.get("param_ref_delim_txt"),
                            metadata.get("param_value_pos_cd"),
                            metadata.get("unit_price_pct_ind"),
                            metadata.get("param_nm_occur_ind"),
                            metadata.get("date_format_cd"),
                            metadata.get("decimal_separator_cd"),
                            metadata.get("param_def_value_txt"),
                            metadata.get("derivation_col"),
                            metadata.get("operations_seq"),
                            metadata.get("param_val_fn_txt")
                        ))
                conn.commit()
        except oracledb.IntegrityError as e:
            raise DBQueryException(f"Integrity error (FK/PK): {str(e)}")
        except oracledb.DatabaseError as e:
            if "ORA-00942" in str(e):
                raise TableMissingException()
            raise DBQueryException(str(e))
        
    def get_template_info(self, broker_code: str):
        query="select broker_cd,no_format from tps2_brokers_dref where broker_cd=:1"
        try:
            with self.pool.acquire() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query,(broker_code,))
                    row = cursor.fetchone()
                    if row:
                        return {"broker_code": row[0], "no_template": row[1]}
                    else:
                        return None
        except oracledb.DatabaseError as e:
            if "ORA-00942" in str(e):
                raise TableMissingException("Broker Reference table not found")
            raise DBQueryException(str(e))
        
    def get_broker_config(self, broker_code: str, broker_template_no: int):
        query = """
        select * from tps2_mnt_brokers_conf_fldsmap where broker_cd = :broker_code and broker_format_nm = :broker_template_no
        and version=(select max(version) from tps2_mnt_brokers_conf_fldsmap where broker_cd = :broker_code and broker_format_nm = :broker_template_no)
        order by param_nm
        """
        try:
            with self.pool.acquire() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, {"broker_code": broker_code, "broker_template_no": broker_template_no})
                    columns = [col[0].lower() for col in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except oracledb.DatabaseError as e:
            if "ORA-00942" in str(e):
                raise TableMissingException("Broker Configuration table not found")
            raise DBQueryException(str(e))

    def update_config(self, broker_code: str, broker_template_no: int, version: int, unique_id: str, rows: list):
        try:
            with self.pool.acquire() as conn:
                with conn.cursor() as cursor:
                    new_version=version+1
                    query = """
                        insert into tps2_brokers_format_dref(broker_cd, broker_format_nm, version, unique_id)
                        select :broker_code, :broker_template_no, :new_version, :unique_id FROM dual
                        where not exists(
                            select 1 from tps2_brokers_format_dref
                            where broker_cd=:broker_code and broker_format_nm=:broker_template_no AND version = :new_version
                        )
                    """
                    cursor.execute(query,{
                        "broker_code": broker_code, "broker_template_no": broker_template_no, "unique_id":unique_id,
                        "new_version":new_version
                    })

                    if cursor.rowcount == 0:
                        conn.rollback()
                        raise VersionConflictException("Version conflict: another user has already updated this template.")

                    query = """
                        insert into tps2_mnt_brokers_conf_fldsmap (
                                broker_cd, broker_format_nm, version,
                                param_nm, param_ref_txt,
                                start_index_nbr, end_index_nbr,
                                row_adder_cnt, col_adder_cnt,
                                param_ref_delim_txt, param_value_pos_cd,
                                unit_price_pct_ind, param_nm_occur_ind,
                                date_format_cd, decimal_separator_cd,
                                param_def_value_txt, derivation_col,
                                operations_seq, param_val_fn_txt
                            ) values (
                            :1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19
                        )
                    """

                    for row in rows:
                        for field in row.fields:
                            m = field.metadata or {}
                            m = m.model_dump()
                            cursor.execute(query, (
                                broker_code,
                                broker_template_no,
                                new_version,
                                field.custom_field,
                                field.document_label,
                                m.get("start_index_nbr"),
                                m.get("end_index_nbr"),
                                m.get("row_adder_cnt"),
                                m.get("col_adder_cnt"),
                                m.get("param_ref_delim_txt"),
                                m.get("param_value_pos_cd"),
                                m.get("unit_price_pct_ind"),
                                m.get("param_nm_occur_ind"),
                                m.get("date_format_cd"),
                                m.get("decimal_separator_cd"),
                                m.get("param_def_value_txt"),
                                m.get("derivation_col"),
                                m.get("operations_seq"),
                                m.get("param_val_fn_txt")
                            ))
                    conn.commit()
                    return {
                        "message": "Config updated successfully", 
                        "version": new_version
                    }
        except oracledb.IntegrityError as e:
            raise DBQueryException(f"Integrity error (FK/PK): {str(e)}")
        except oracledb.DatabaseError as e:
            if "ORA-00942" in str(e):
                raise TableMissingException()
            raise DBQueryException(str(e))