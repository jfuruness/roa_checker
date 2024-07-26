from dataclasses import dataclass
from ipaddress import IPv4Network, IPv6Network
from typing import Optional

from lib_cidr_trie import CIDRNode

from .enums import ROARouted, ROAValidity


class ROAsNode(CIDRNode):
    def __init__(self, *args, **kwargs):
        """Initializes the ROA node"""

        super(ROA, self).__init__(*args, **kwargs)
        self.roas: set[ROA] = set()

    # Mypy doesn't understand *args in super class
    def add_data(self, prefix: IPv4Network | IPv6Network, roa: ROA) -> None:  # type: ignore
        """Adds ROA to the node for that prefix"""

        self.prefix: IPv4Network | IPv6Network = prefix
        self.roas.add(roa)
