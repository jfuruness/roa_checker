from ipaddress import IPv4Network, IPv6Network

from lib_cidr_trie import CIDRNode

from .roa import ROA


class ROAsNode(CIDRNode):
    def __init__(self, *args, **kwargs):
        """Initializes the ROA node"""

        super().__init__(*args, **kwargs)
        self.roas: set[ROA] = set()

    # Mypy doesn't understand *args in super class
    def add_data(  # type: ignore
        self, prefix: IPv4Network | IPv6Network, roa: ROA
    ) -> None:
        """Adds ROA to the node for that prefix"""

        self.prefix: IPv4Network | IPv6Network = prefix
        self.roas.add(roa)
