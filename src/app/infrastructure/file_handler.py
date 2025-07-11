import os
import base64
import mimetypes
import pandas as pd
import io
from src.app.domain.models import ExtractionField, ExtractionFieldMetadata, ExtractionLLMResponse, ExtractionResponseData, ExtractionRow
from src.app.domain.exception import InvalidFileTypeException

EXTENSION_MIME_MAP = {
    ".csv": "text/csv",
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel"
}

def convert_excel_to_csv_bytes(file_bytes):
    df = pd.read_excel(io.BytesIO(file_bytes))
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")

def read_file_as_part(file_bytes, filename):
    ext = os.path.splitext(filename)[1].lower()
    mime_type = EXTENSION_MIME_MAP.get(ext)

    if not mime_type:
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            raise InvalidFileTypeException()

    if ext in [".xlsx", ".xls"]:
        file_bytes = convert_excel_to_csv_bytes(file_bytes)
        mime_type = "text/csv"
    
    return {
        "inline_data": {
            "data": base64.b64encode(file_bytes).decode('utf-8'),
            "mime_type": mime_type
        }
    }

def transform_llm_output(parsed, session_id, doc_type):
    user_fields = parsed.get("user_fields", [])
    doc_fields = parsed.get("document_fields", [])
    rows = parsed.get("rows", [])

    extracted_meta_keys = [
        "start_index_nbr", "end_index_nbr", "row_adder_cnt", "col_adder_cnt",
        "param_ref_delim_txt", "param_value_pos_cd"
    ]

    full_meta_keys = extracted_meta_keys + [
        "unit_price_pct_ind", "param_nm_occur_ind", "date_format_cd", "decimal_separator_cd",
        "param_def_value_txt", "derivation_col", "operations_seq", "param_val_fn_txt"
    ]

    extracted_rows = []

    for row in rows:
        row_values = row.get("values", [])
        meta_lists = {key: row.get(key, []) for key in extracted_meta_keys}

        fields = []
        for i, custom_field in enumerate(user_fields):
            value = row_values[i] if i < len(row_values) else ""
            document_label = doc_fields[i] if i < len(doc_fields) else ""

            metadata = {}
            for key in full_meta_keys:
                if doc_type == "excel":
                    if key == "col_adder_cnt":
                        metadata[key] = meta_lists.get(key, [None])[i] if i < len(meta_lists.get(key, [])) else None
                    else:
                        metadata[key] = None
                else:
                    if key in extracted_meta_keys:
                        metadata[key] = meta_lists.get(key, [None])[i] if i < len(meta_lists.get(key, [])) else None
                    else:
                        metadata[key] = None

            fields.append(ExtractionField(
                custom_field=custom_field,
                document_label=document_label,
                value=value,
                metadata=ExtractionFieldMetadata(**metadata)
            ))

        extracted_rows.append(ExtractionRow(
            index=row.get("index", 0),
            fields=fields
        ))

    return ExtractionLLMResponse(
        session_id=session_id,
        type="document_extraction",
        response=ExtractionResponseData(rows=extracted_rows)
    )
