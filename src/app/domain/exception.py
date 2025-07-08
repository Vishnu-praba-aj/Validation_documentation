class FileTooLargeException(Exception):
    def __init__(self, detail="File is too large."):
        self.detail = detail

class SessionNotFoundException(Exception):
    def __init__(self, detail="Session not found."):
        self.detail = detail

class InvalidFileTypeException(Exception):
    def __init__(self, detail="Invalid or unsupported file type."):
        self.detail = detail

class RepoProcessingException(Exception):
    def __init__(self, detail="Failed to process repository."):
        self.detail = detail

class InvalidRepoURLException(Exception):
    def __init__(self, detail="Invalid Repo URL (no user or repo name)"):
        self.detail = detail

class InvalidJSONResponseException(Exception):
    def __init__(self, detail="Invalid JSON Response from LLM."):
        self.detail = detail

class JSONParsingException(Exception):
    def __init__(self, detail="Could not parse JSON Response."):
        self.detail = detail

class NoDefaultBranchException(Exception):
    def __init__(self, detail="Could not determine default branch."):
        self.detail = detail

class UnsupportedURLException(Exception):
    def __init__(self, detail="Not a github or bitbucket URL."):
        self.detail = detail