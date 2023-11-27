from ipaddress import IPv4Network, IPv6Network

from lib_cidr_trie import CIDRNode

from .enums import ROARouted, ROAValidity


class ROA(CIDRNode):
    def __init__(self, *args, **kwargs):
        """Initializes the ROA node"""

        super(ROA, self).__init__(*args, **kwargs)
        # Origin max length pairs
        self.origin_max_lengths: set[tuple[int, int]] = set()

    def add_data(self, prefix: IPv4Network | IPv6Network, origin: int, max_length: int):
        """Adds data to the node"""

        if max_length is None:
            max_length = prefix.prefixlen
        self.prefix = prefix
        self.origin_max_lengths.add((origin, max_length))

    def get_validity(
        self, prefix: IPv4Network | IPv6Network, origin: int
    ) -> tuple[ROAValidity, ROARouted]:
        """Gets the ROA validity of a prefix origin pair"""

        if not prefix.subnet_of(self.prefix):
            return ROAValidity.UNKNOWN, ROARouted.UNKNOWN
        else:
            for self_origin, max_length in self.origin_max_lengths:
                if prefix.prefixlen > max_length or origin != self_origin:
                    if self_origin == 0:
                        return ROAValidity.INVALID, ROARouted.NON_ROUTED
                    else:
                        return ROAValidity.INVALID, ROARouted.Routed
            return ROAValidity.VALID, ROARouted.ROUTED
