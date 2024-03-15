from enum import Enum


class ROAValidity(Enum):
    # NOTE: These values double as "scores" for validity,
    # so do NOT change the order
    # (used in the ROA class)
    VALID = 0
    UNKNOWN = 1
    # Note that we cannot differentiate between invalid by length
    # or invalid by origin or invalid by both
    # That is because for the same prefix you can have multiple
    # max lengths or multiple origins
    # And you select the most valid roa. So is invalid by length
    # more valid than invalid by origin? No. So we just say invalid

    # Nixing the comment above with the following methodology:
    # NOTE: There can be multiple ROAs for the same prefix
    # So if we say a ROA is invalid by length and origin
    # it could potentially be invalid by length for one ROA
    # and invalid by origin for another prefix
    # If we say non routed, it's violating at least one non routed ROA
    INVALID_LENGTH = 2
    INVALID_ORIGIN = 3
    INVALID_LENGTH_AND_ORIGIN = 4

    @staticmethod
    def is_valid(roa_validity: "ROAValidity") -> bool:
        return roa_validity == ROAValidity.VALID

    @staticmethod
    def is_unknown(roa_validity: "ROAValidity") -> bool:
        return roa_validity == ROAValidity.UNKNOWN

    @staticmethod
    def is_invalid(roa_validity: "ROAValidity") -> bool:
        return roa_validity in (
            ROAValidity.INVALID_LENGTH,
            ROAValidity.INVALID_ORIGIN,
            ROAValidity.INVALID_LENGTH_AND_ORIGIN,
        )


class ROARouted(Enum):
    ROUTED = 0
    UNKNOWN = 1
    # A ROA is Non Routed if it is for an origin of ASN 0
    # This means that the prefix for this ROA should never be announced
    NON_ROUTED = 2
