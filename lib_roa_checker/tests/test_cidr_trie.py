from ipaddress import ip_network

from ..cidr_tries import IPv4CIDRTrie


def test_tree():
    trie = IPv4CIDRTrie()
    cidrs = [ip_network(x) for x in ["1.2.0.0/16", "1.2.3.0/24", "1.2.3.4"]]
    for cidr in cidrs:
        trie.insert(cidr)
    for cidr in cidrs:
        assert cidr in trie
        assert trie.get_most_specific_trie_supernet(cidr).prefix == cidr

    invalid_cidrs = [ip_network(x) for x in ["1.0.0.0/8", "255.255.255.255"]]
    for invalid_cidr in invalid_cidrs:
        assert invalid_cidr not in trie
        assert trie.get_most_specific_trie_supernet(invalid_cidr) is None

    assert ip_network("1.2.4.0/24") in trie
    assert ip_network("1.2.0.255") in trie
    assert ip_network("1.3.0.0/16") not in trie
