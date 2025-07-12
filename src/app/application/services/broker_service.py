from src.app.domain.exception import ResourceNotFoundException, UniqueIdExistsException
from src.app.domain.models import AllBrokers, BrokerConfigResponse, Field, FieldMetadata, Response, Row
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

    def insert_template(self, broker_code: str, response: Response):
        self.dao.insert_broker_config(broker_code, response)

    def get_broker_template_info(self, broker_code: str):
        result = self.dao.get_template_info(broker_code)
        if not result:
            raise ResourceNotFoundException("No broker found")
        return result

    def get_broker_config(self, broker_code: str, broker_template_no: int)->BrokerConfigResponse:
        rows = self.dao.get_broker_config(broker_code, broker_template_no)
        if not rows:
            raise ResourceNotFoundException("No config found for given broker and template")

        version = rows[0]["version"]
        response_rows = []

        for idx, row in enumerate(rows):
            metadata = FieldMetadata(
                start_index_nbr=row.get("start_index_nbr"),
                end_index_nbr=row.get("end_index_nbr"),
                row_adder_cnt=row.get("row_adder_cnt"),
                col_adder_cnt=row.get("col_adder_cnt"),
                param_ref_delim_txt=row.get("param_ref_delim_txt"),
                param_value_pos_cd=row.get("param_value_pos_cd"),
                unit_price_pct_ind=row.get("unit_price_pct_ind"),
                param_nm_occur_ind=row.get("param_nm_occur_ind"),
                date_format_cd=row.get("date_format_cd"),
                decimal_separator_cd=row.get("decimal_separator_cd"),
                param_def_value_txt=row.get("param_def_value_txt"),
                derivation_col=row.get("derivation_col"),
                operations_seq=row.get("operations_seq"),
                param_val_fn_txt=row.get("param_val_fn_txt"),
            )

            field = Field(
                custom_field=row.get("param_nm", ""),
                document_label=row.get("param_ref_txt", ""),
                value=None,
                metadata=metadata,
            )

            response_rows.append(Row(index=idx, fields=[field]))

        return BrokerConfigResponse(
            version=version,
            broker_code=broker_code,
            broker_template_no=broker_template_no,
            response=Response(rows=response_rows),
        )