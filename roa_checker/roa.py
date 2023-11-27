from ipaddress import IPv4Network, IPv6Network
from typing import Optional

from lib_cidr_trie import CIDRNode

from .enums import ROARouted, ROAValidity


class ROA(CIDRNode):
    def __init__(self, *args, **kwargs):
        """Initializes the ROA node"""

        super(ROA, self).__init__(*args, **kwargs)
        # Origin max length pairs
        self.origin_max_lengths: set[tuple[int, int]] = set()

    def add_data(
        self, prefix: IPv4Network | IPv6Network, origin: int, max_length: Optional[int]
    ):
        """Adds data to the node"""

        if max_length is None:
            max_length = prefix.prefixlen
        self.prefix = prefix
        self.origin_max_lengths.add((origin, max_length))

    def get_validity(
        self, prefix: IPv4Network | IPv6Network, origin: int
    ) -> tuple[ROAValidity, ROARouted]:
        """Gets the ROA validity of a prefix origin pair"""

        assert isinstance(prefix, type(self.prefix))
        # Mypy isn't getting that these types are the same
        if not prefix.subnet_of(self.prefix):  # type: ignore
            return ROAValidity.UNKNOWN, ROARouted.UNKNOWN
        else:
            valid_length = True
            valid_origin = True
            routed = ROARouted.ROUTED
            # NOTE: There can be multiple ROAs for the same prefix
            # So if we say a ROA is invalid by length and origin
            # it could potentially be invalid by length for one ROA
            # and invalid by origin for another prefix
            # If we say non routed, it's violating at least one non routed ROA
            for self_origin, max_length in self.origin_max_lengths:
                if prefix.prefixlen > max_length:
                    valid_length = False
                    if self_origin == 0:
                        routed = ROARouted.NON_ROUTED
                if origin != self_origin:
                    valid_origin = False
                    if self_origin == 0:
                        routed = ROARouted.NON_ROUTED
            if valid_length and valid_origin:
                return ROAValidity.VALID, routed
            elif valid_length and not valid_origin:
                return ROAValidity.INVALID_ORIGIN, routed
            elif not valid_length and valid_origin:
                return ROAValidity.INVALID_LENGTH, routed
            else:
                return ROAValidity.INVALID_LENGTH_AND_ORIGIN, routed
