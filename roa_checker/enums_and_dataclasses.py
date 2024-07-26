from dataclasses import dataclass
from enum import Enum


class ROAValidity(Enum):
    """ROAValidity values

    NOTE: it's possible that you could have two ROAs for
    the same prefix, each with different reasons why they are
    invalid. In that case, the ROAChecker returns the "best"
    validity (in the order below). It doesn't really matter,
    since they are both invalid anyways, and that's the only
    case where this conflict can occur
    """

    # NOTE: These values double as "scores" for validity,
    # so do NOT change the order
    # (used in the ROA class)
    VALID = 0
    UNKNOWN = 1
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


@dataclass(frozen=True, slots=True)
class ROAOutcome:
    validity: ROAValidity
    routed: ROARouted

    def __lt__(self, other) -> bool:
        if isinstance(other, ROAOutcome):
            return self.validity.value < other.validity.value
        else:
            return NotImplemented
