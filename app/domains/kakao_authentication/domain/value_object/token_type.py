from enum import Enum


class TokenType(str, Enum):
    TEMP = "temp"
    SESSION = "session"
