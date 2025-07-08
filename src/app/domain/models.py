from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any

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

class ExtractionField(BaseModel):
    custom_field: str
    document_label: Optional[str] = None
    value: Optional[str] = None

class ExtractionRow(BaseModel):
    index: int
    fields: List[ExtractionField]

class ExtractionResponseData(BaseModel):
    rows: Optional[List[ExtractionRow]] = None
    message: Optional[str] = None

class ExtractionLLMResponse(BaseModel):
    session_id: str
    type: str = "document_extraction"
    response: ExtractionResponseData