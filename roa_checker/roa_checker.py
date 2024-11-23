from functools import cache
from ipaddress import IPv4Network, IPv6Network, ip_network

from .enums_and_dataclasses import ROAOutcome
from .roa import ROA
from .roa_trie import ROATrie
from .roa_tries import IPv4ROATrie, IPv6ROATrie


class ROAChecker:
    """Gets validity of prefix origin pairs against ROAs"""

    def __init__(self):
        """Initializes both ROA tries"""

        self.ipv4_trie = IPv4ROATrie()
        self.ipv6_trie = IPv6ROATrie()
        self.get_roa_outcome_w_prefix_str_cached.cache_clear()

    def insert(self, prefix: IPv4Network | IPv6Network, roa: ROA) -> None:
        """Inserts a prefix into the tries"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        # mypy struggling with this
        return trie.insert(prefix, roa)  # type: ignore

    def get_relevant_roas(self, prefix: IPv4Network | IPv6Network) -> frozenset[ROA]:
        """Gets the ROA covering prefix-origin pair"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        assert isinstance(trie, ROATrie)
        # Mypy doesn't understand I match the proper trie with the prefix type
        return trie.get_relevant_roas(prefix)  # type: ignore

    def get_roa_outcome(
        self, prefix: IPv4Network | IPv6Network, origin: int
    ) -> ROAOutcome:
        """Gets the validity of a prefix origin pair"""

        trie = self.ipv4_trie if prefix.version == 4 else self.ipv6_trie
        assert isinstance(trie, ROATrie), "for mypy"
        # mypy doesn't understand I match the proper trie with the prefix type
        return trie.get_roa_outcome(prefix, origin)  # type: ignore

    # NOTE: since this is called so often, we leave it as cache
    # since it's significantly faster
    # It literally says cached in the name, this better not cause leaks
    @cache  # noqa: B019
    def get_roa_outcome_w_prefix_str_cached(
        self,
        prefix_str: str,
        origin: int,
    ) -> ROAOutcome:
        """Returns ROA outcome for a prefix (str) and origin, and caches the result"""

        return self.get_roa_outcome(ip_network(prefix_str), origin)

    def clear(self):
        self.__init__()  # type: ignore
