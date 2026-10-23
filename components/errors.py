class RotorConfigError(Exception):
    def __init__(self, message: str) -> str:
        super().__init__(message)

class InvalidModeError(Exception):
    def __init__(self, message: str) -> str:
        super().__init__(message)

class MessageKeyError(Exception):
    def __init__(self, message: str) -> str:
        super().__init__(message)

class CodesheetKeyError(Exception):
    def __init__(self, message: str) -> str:
        super().__init__(message)