from ipaddress import IPv4Network, IPv6Network

from .roa_trie import ROATrie


class IPv4ROATrie(ROATrie):
    """Trie of IPv4 CIDRs for ROAs"""

    prefix_class = IPv4Network


class IPv6ROATrie(ROATrie):
    """Trie of IPv6 CIDRs for ROAs"""

    prefix_class = IPv6Network
