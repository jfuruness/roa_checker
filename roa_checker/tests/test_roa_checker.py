from ipaddress import ip_network

from ..roa_checker import ROAChecker
from ..roa_validity import ROAValidity

def test_tree():
    trie = ROAChecker()
    cidrs = [ip_network(x) for x in ["1.2.0.0/16", "1.2.3.0/24", "1.2.3.4"]]
    origin = 1
    for cidr in cidrs:
        trie.insert(cidr, origin, cidr.prefixlen)
    for cidr in cidrs:
        assert trie.get_roa(cidr, origin).prefix == cidr
        assert trie.get_validity(cidr, origin) == ROAValidity.VALID

    validity = trie.get_validity(ip_network("1.0.0.0/8"), origin)
    assert validity == ROAValidity.UNKNOWN
    validity = trie.get_validity(ip_network("255.255.255.255"), origin)
    assert validity == ROAValidity.UNKNOWN
    validity = trie.get_validity(ip_network("1.2.4.0/24"), origin)
    assert validity == ROAValidity.INVALID_LENGTH
    validity = trie.get_validity(ip_network("1.2.3.0/24"), origin + 1)
    assert validity == ROAValidity.INVALID_ORIGIN
    validity = trie.get_validity(ip_network("1.2.4.0/24"), origin + 1)
    assert validity == ROAValidity.INVALID_LENGTH_AND_ORIGIN
    validity = trie.get_validity(ip_network("1.2.0.255"), origin)
    assert validity == ROAValidity.INVALID_LENGTH
    validity = trie.get_validity(ip_network("1.3.0.0/16"), origin)
    assert validity == ROAValidity.UNKNOWN
