from enum import Enum


class ROAValidity(Enum):
    VALID = 0
    UNKNOWN = 1
    # Note that we cannot differentiate between invalid by length
    # or invalid by origin or invalid by both
    # That is because for the same prefix you can have multiple
    # max lengths or multiple origins
    # And you select the most valid roa. So is invalid by length
    # more valid than invalid by origin? No. So we just say invalid
    INVALID = 2


class ROARouted(Enum):
    ROUTED = 0
    UNKNOWN = 1
    # A ROA is Non Routed if it is for an origin of ASN 0
    # This means that the prefix for this ROA should never be announced
    NON_ROUTED = 2
