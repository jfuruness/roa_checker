from ipaddress import ip_network, IPv4Network, IPv6Network

from lib_cidr_trie import CIDRNode

from .roa_validity import ROAValidity


class ROA(CIDRNode):
    def __init__(self, *args, **kwargs):
        """Initializes the ROA node"""

        super(ROA, self).__init__(*args, **kwargs)
        self.origin_max_lengths = set()

    def add_data(self, prefix: ip_network, origin: int, max_length: int):
        """Adds data to the node"""

        assert isinstance(prefix, (IPv4Network, IPv6Network))
        assert isinstance(origin, int)
        assert isinstance(max_length, (int, type(None)))
        if max_length is None:
            max_length = prefix.prefixlen
        self.prefix = prefix
        self.origin_max_lengths.add((origin, max_length))

    def get_validity(self, prefix: ip_network, origin: int) -> ROAValidity:
        """Gets the ROA validity of a prefix origin pair"""

        # Doing this for OO purposes even tho it should always be True
        if not prefix.subnet_of(self.prefix):
            return ROAValidity.UNKNOWN, None
        else:
            for self_origin, max_length in self.origin_max_lengths:
                if prefix.prefixlen > max_length or origin != self_origin:
                    return ROAValidity.INVALID, self_origin != 0
            return ROAValidity.VALID, True
