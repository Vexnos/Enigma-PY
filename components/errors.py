class ConfigError(ValueError):
    def __init__(self, message: str) -> str:
        super().__init__(message)

class InvalidModeError(ValueError):
    def __init__(self, message: str) -> str:
        super().__init__(message)

class MessageKeyError(ValueError):
    def __init__(self, message: str) -> str:
        super().__init__(message)

class CodesheetKeyError(ValueError):
    def __init__(self, message: str) -> str:
        super().__init__(message)