from ipaddress import ip_network
from lib_cidr_trie import CIDRTrie

from .roa import ROA
from .roa_validity import ROAValidity


class ROATrie(CIDRTrie):
    """Trie of CIDRs for ROAs"""

    node_class = ROA

    def get_validity(self, prefix: ip_network, origin: int) -> ROAValidity:
        """Gets the validity of a prefix-origin pair"""

        roa = self.get_most_specific_trie_supernet(prefix)
        if roa is None:
            return ROAValidity.UNKNOWN
        else:
            return roa.get_validity(prefix, origin)
