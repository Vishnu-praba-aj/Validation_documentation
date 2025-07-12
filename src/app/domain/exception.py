import oracledb


class FileTooLargeException(Exception):
    def __init__(self, detail="File is too large."):
        self.detail = detail

class InvalidFileTypeException(Exception):
    def __init__(self, detail="Invalid or unsupported file type."):
        self.detail = detail

class RepoProcessingException(Exception):
    def __init__(self, detail="Failed to process repository."):
        self.detail = detail

class InvalidJSONResponseException(Exception):
    def __init__(self, detail="Invalid JSON Response from LLM."):
        self.detail = detail

class JSONParsingException(Exception):
    def __init__(self, detail="Could not parse JSON Response."):
        self.detail = detail

class TableMissingException(Exception):
    def __init__(self, detail="Table does not exist in the database"):
        self.detail = detail

class DBQueryException(Exception):
    def __init__(self, detail="Failed to execute query on DB"):
        self.detail = detail

class UniqueIdExistsException(Exception):
    def __init__(self, detail="Unique identifier already exists"):
        self.detail = detail

class ResourceNotFoundException(Exception):
    def __init__(self, detail="Resource Not found"):
        self.detail = detail

class VersionConflictException(Exception):
    def __init__(self, detail="Version Conflict"):
        self.detail = detail
