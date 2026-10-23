"""

=================================
   file: errors.py
project: Enigma Machine in Python
 author: Vexnos
   date: 2026-10-24
=================================

"""
# ------------------------------------------------------------------------
# Errors
# ------------------------------------------------------------------------
class ConfigError(ValueError):
    def __init__(self, message: str) -> str:
        super().__init__(message)

class InvalidModeError(ValueError):
    def __init__(self, message: str) -> str:
        super().__init__(message)

class CodesheetKeyError(ValueError):
    def __init__(self, message: str) -> str:
        super().__init__(message)