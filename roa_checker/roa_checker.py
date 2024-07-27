from ipaddress import IPv4Network, IPv6Network

from .roa import ROA
from .roa_trie import ROATrie
from .roa_tries import IPv4ROATrie, IPv6ROATrie
from .enums_and_dataclasses import ROAOutcome


class ROAChecker:
    """Gets validity of prefix origin pairs against ROAs"""

    def __init__(self):
        """Initializes both ROA tries"""

        self.ipv4_trie = IPv4ROATrie()
        self.ipv6_trie = IPv6ROATrie()

    def insert(self, prefix: IPv4Network | IPv6Network, roa: ROA) -> None:
        """Inserts a prefix into the tries"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        # mypy struggling with this
        return trie.insert(prefix, roa)  # type: ignore

    def get_roas(self, prefix: IPv4Network | IPv6Network) -> frozenset[ROA]:
        """Gets the ROA covering prefix-origin pair"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        assert isinstance(trie, ROATrie)
        return trie.get_relevant_roas(prefix)

    def get_roa_outcome(
        self, prefix: IPv4Network | IPv6Network, origin: int
    ) -> ROAOutcome:
        """Gets the validity of a prefix origin pair"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        assert isinstance(trie, ROATrie), "for mypy"
        return trie.get_roa_outcome(prefix, origin)
