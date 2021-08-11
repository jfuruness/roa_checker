from ipaddress import ip_network

from lib_cidr_trie import CIDRNode

from .roa_validity import ROAValidity


class ROA(CIDRNode):
    def __init__(self, *args, **kwargs):
        """Initializes the ROA node"""

        super(ROA, self).__init__(*args, **kwargs)
        self.origin = None
        self.max_length = None

    def add_data(self, prefix: ip_network, origin: int, max_length: int):
        """Adds data to the node"""

        # Make sure node was not previously set before
        # If it was previously set, two ROAs conflict with each other
        assert not any([self.prefix, self.origin, self.max_length])
        self.prefix = prefix
        self.origin = origin
        self.max_length = max_length

    def get_validity(self, prefix: ip_network, origin: int) -> ROAValidity:
        """Gets the ROA validity of a prefix origin pair"""

        # Doing this for OO purposes even tho it should always be True
        if not prefix.subnet_of(self.prefix):
            return ROAValidity.UNKNOWN
        else:
            if prefix.prefixlen > self.max_length:
                if origin != self.origin:
                    return ROAValidity.INVALID_LENGTH_AND_ORIGIN
                else:
                    return ROAValidity.INVALID_LENGTH
            elif origin != self.origin:
                return ROAValidity.INVALID_ORIGIN
            else:
                return ROAValidity.VALID
