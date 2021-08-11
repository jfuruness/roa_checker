from enum import Enum

class ROA(Enum):
    VALID = 0
    INVALID_LENGTH = 1
    INVALID_ORIGIN = 2
    INVALID_LENGTH_AND_ORGIN = 3
