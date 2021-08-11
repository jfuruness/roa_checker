from ipaddress import ip_network

from .roa_tries import IPv4ROATrie, IPv6ROATrie
from .roa_validity import ROAValidity


class ROAChecker:
    """Gets validity of prefix origin pairs against ROAs"""

    def __init__(self):
        """Initializes both ROA tries"""

        self.ipv4_trie = IPv4ROATrie()
        self.ipv6_trie = IPv6ROATrie()

    def insert(self, prefix: ip_network, origin: int, max_length: int):
        """Inserts a prefix into the tries"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        return trie.insert(prefix, origin, max_length)

    def get_roa(self, prefix: ip_network, origin: int):
        """Gets the ROA covering prefix-origin pair"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        return trie.get_most_specific_trie_supernet(prefix)

    def get_validity(self, prefix: ip_network, origin: int) -> ROAValidity:
        """Gets the validity of a prefix origin pair"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        return trie.get_validity(prefix, origin)
