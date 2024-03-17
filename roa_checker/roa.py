from dataclasses import dataclass
from ipaddress import IPv4Network, IPv6Network
from typing import Optional

from lib_cidr_trie import CIDRNode

from .enums import ROARouted, ROAValidity


@dataclass(frozen=True, slots=True)
class ROAOutcome:
    validity: ROAValidity
    routed: ROARouted

    def __lt__(self, other) -> bool:
        if isinstance(other, ROAOutcome):
            return self.validity.value < other.validity.value
        else:
            return NotImplemented


class ROA(CIDRNode):
    def __init__(self, *args, **kwargs):
        """Initializes the ROA node"""

        super(ROA, self).__init__(*args, **kwargs)
        # Origin max length pairs
        self.origin_max_lengths: set[tuple[int, int]] = set()

    # Mypy doesn't understand *args in super class
    def add_data(  # type: ignore
        self,
        prefix: IPv4Network | IPv6Network,
        origin: int,
        max_length: Optional[int] = None,
    ):
        """Adds data to the node"""

        if max_length is None:
            max_length = prefix.prefixlen
        self.prefix = prefix
        self.origin_max_lengths.add((origin, max_length))

    def get_validity(
        self, prefix: IPv4Network | IPv6Network, origin: int
    ) -> tuple[ROAValidity, ROARouted]:
        """Gets the ROA validity of a prefix origin pair

        This gets pretty complicated because we need to calculate
        both validiate and routed, and there can be multiple ROAs
        for the same announcement.

        In other words, we need to calculate the best ROA for a given
        announcement, and then use the validity of that ROA. Ie
        the "most valid" ROA is the one that should be used.
        """

        assert isinstance(prefix, type(self.prefix))
        # Mypy isn't getting that these types are the same
        if not prefix.subnet_of(self.prefix):  # type: ignore
            return ROAValidity.UNKNOWN, ROARouted.UNKNOWN
        else:
            roa_validities = list()

            for self_origin, max_length in self.origin_max_lengths:
                routed = ROARouted.NON_ROUTED if self_origin == 0 else ROARouted.ROUTED
                if prefix.prefixlen > max_length and origin != self_origin:
                    roa_validities.append(
                        ROAOutcome(ROAValidity.INVALID_LENGTH_AND_ORIGIN, routed)
                    )
                elif prefix.prefixlen > max_length and origin == self_origin:
                    roa_validities.append(
                        ROAOutcome(ROAValidity.INVALID_LENGTH, routed)
                    )
                elif prefix.prefixlen <= max_length and origin != self_origin:
                    roa_validities.append(
                        ROAOutcome(ROAValidity.INVALID_ORIGIN, routed)
                    )
                elif prefix.prefixlen <= max_length and origin == self_origin:
                    roa_validities.append(ROAOutcome(ROAValidity.VALID, routed))
                else:
                    raise NotImplementedError("This should never happen")

            best_outcome = sorted(roa_validities)[0]
            return best_outcome.validity, best_outcome.routed
