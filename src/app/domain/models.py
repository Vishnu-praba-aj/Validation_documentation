from pydantic import BaseModel
from typing import List, Optional, Union
    
class ValidationField(BaseModel):
    field: str
    required: Optional[bool] = None
    type: Optional[str] = None
    min: Optional[float] = None
    max: Optional[float] = None
    length: Optional[int] = None
    default: Optional[str] = None
    pattern: Optional[str] = None
    otherValidation: Optional[str] = None

class ValidationEntityWithFields(BaseModel):
    name: str
    fields: List[ValidationField]

class ValidationEntityWithNote(BaseModel):
    name: str
    note: str

ValidationEntity = Union[ValidationEntityWithFields, ValidationEntityWithNote]

class ValidationResponseData(BaseModel):
    entities: List[ValidationEntity]

class ValidationLLMResponse(BaseModel):
    session_id: str
    type: str = "validation"
    response: ValidationResponseData

class ExtractionFieldMetadata(BaseModel):
    start_index_nbr: Optional[int] = None
    end_index_nbr: Optional[int] = None
    row_adder_cnt: Optional[int] = None
    col_adder_cnt: Optional[int] = None
    param_ref_delim_txt: Optional[str] = None
    param_value_pos_cd: Optional[str] = None
    unit_price_pct_ind: Optional[str] = None
    param_nm_occur_ind: Optional[str] = None
    date_format_cd: Optional[str] = None
    decimal_separator_cd: Optional[str] = None
    param_def_value_txt: Optional[str] = None
    derivation_col: Optional[str] = None
    operations_seq: Optional[str] = None
    param_val_fn_txt: Optional[str] = None

class ExtractionField(BaseModel):
    custom_field: str
    document_label: Optional[str] = None
    value: Optional[str] = None
    metadata: ExtractionFieldMetadata

class ExtractionRow(BaseModel):
    index: int
    fields: List[ExtractionField]

class ExtractionResponseData(BaseModel):
    rows: List[ExtractionRow]

class ExtractionLLMResponse(BaseModel):
    session_id: str
    response: ExtractionResponseData

class BrokerOut(BaseModel):
    broker_code: str
    broker_name: str

class AllBrokers(BaseModel):
    broker: List[BrokerOut]

class ExtractUniqueIdRequest(BaseModel):
    session_id: str
    broker_code: str
    unique_id: str
    message: Optional[str] = None