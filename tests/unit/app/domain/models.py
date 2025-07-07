import pytest
from src.app.domain.models import (
    ValidationField, ValidationEntityWithFields, ValidationEntityWithNote, ValidationLLMResponse,
    ExtractionField, ExtractionRow, ExtractionResponseData, ExtractionLLMResponse
)
from pydantic import ValidationError

def test_validation_field_valid():
    f = ValidationField(field="name", required=True, type="String")
    assert f.field == "name"
    assert f.required is True

def test_validation_field_invalid():
    with pytest.raises(ValidationError):
        ValidationField(field=None)

def test_validation_entity_with_fields():
    entity = ValidationEntityWithFields(
        name="User",
        fields=[ValidationField(field="name", required=True)]
    )
    assert entity.name == "User"
    assert isinstance(entity.fields[0], ValidationField)

def test_validation_entity_with_note():
    entity = ValidationEntityWithNote(name="User", note="No validation logic found")
    assert entity.note == "No validation logic found"

def test_llm_response_model():
    resp = ValidationLLMResponse(session_id="abc", type="validation", response={"entities": []})
    assert resp.type == "validation"

def test_extraction_llm_response_valid():
    resp = ExtractionLLMResponse(
        session_id="abc",
        type="document_extraction",
        response=ExtractionResponseData(rows=[ExtractionRow(index=0, fields=[ExtractionField(value="foo")])])
    )
    assert resp.type == "document_extraction"
    assert resp.response.rows[0].fields[0].value == "foo"