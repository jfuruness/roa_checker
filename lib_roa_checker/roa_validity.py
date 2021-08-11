from enum import Enum

class ROAValidity(Enum):
    VALID = 0
    UNKNOWN = 1
    INVALID_LENGTH = 2
    INVALID_ORIGIN = 3
    INVALID_LENGTH_AND_ORIGIN = 4
