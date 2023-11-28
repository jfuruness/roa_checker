from ipaddress import IPv4Network, IPv6Network
from typing import Optional

from lib_cidr_trie import CIDRTrie

from .roa import ROA
from .roa_trie import ROATrie
from .roa_tries import IPv4ROATrie, IPv6ROATrie
from .enums import ROARouted, ROAValidity


class ROAChecker:
    """Gets validity of prefix origin pairs against ROAs"""

    def __init__(self):
        """Initializes both ROA tries"""

        self.ipv4_trie = IPv4ROATrie()
        self.ipv6_trie = IPv6ROATrie()

    def insert(
        self, prefix: IPv4Network | IPv6Network, origin: int, max_length: Optional[int]
    ) -> None:
        """Inserts a prefix into the tries"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        # mypy struggling with this
        return trie.insert(prefix, origin, max_length)  # type: ignore

    def get_roa(self, prefix: IPv4Network | IPv6Network, *args) -> Optional[ROA]:
        """Gets the ROA covering prefix-origin pair"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        assert isinstance(trie, CIDRTrie)
        roa = trie.get_most_specific_trie_supernet(prefix)
        assert roa is None or isinstance(roa, ROA), "for mypy"
        return roa

    def get_validity(
        self, prefix: IPv4Network | IPv6Network, origin: int
    ) -> tuple[ROAValidity, ROARouted]:
        """Gets the validity of a prefix origin pair"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        assert isinstance(trie, ROATrie), "for mypy"
        return trie.get_validity(prefix, origin)
