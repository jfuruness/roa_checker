from ipaddress import ip_network

from roa_checker import ROAChecker, ROARouted, ROAValidity


def test_tree():
    # TODO: Break up into unit tests
    trie = ROAChecker()
    cidrs = [ip_network(x) for x in ["1.2.0.0/16", "1.2.3.0/24", "1.2.3.4"]]
    routed_origin = 1
    for cidr in cidrs:
        trie.insert(cidr, routed_origin, cidr.prefixlen)
    for cidr in cidrs:
        roa = trie.get_roa(cidr, routed_origin)
        assert roa and roa.prefix == cidr
        validity, routed = trie.get_validity(cidr, routed_origin)
        assert (validity, routed) == (
            ROAValidity.VALID,
            ROARouted.ROUTED,
        )
        assert ROAValidity.is_unknown(validity) is False
        assert ROAValidity.is_invalid(validity) is False
        assert ROAValidity.is_valid(validity) is True

    non_routed_cidrs = [ip_network(x) for x in ["2.2.0.0/16", "2.2.3.0/24", "2.2.3.4"]]
    non_routed_origin = 0
    for cidr in non_routed_cidrs:
        trie.insert(cidr, non_routed_origin, cidr.prefixlen)
    for cidr in non_routed_cidrs:
        roa = trie.get_roa(cidr, non_routed_origin)
        assert roa and roa.prefix == cidr
        assert trie.get_validity(cidr, routed_origin) == (
            ROAValidity.INVALID_ORIGIN,
            ROARouted.NON_ROUTED,
        )

    validity, routed = trie.get_validity(ip_network("1.0.0.0/8"), routed_origin)
    assert validity == ROAValidity.UNKNOWN
    assert routed == ROARouted.UNKNOWN
    validity, routed = trie.get_validity(ip_network("255.255.255.255"), routed_origin)
    assert validity == ROAValidity.UNKNOWN
    assert routed == ROARouted.UNKNOWN
    assert ROAValidity.is_unknown(validity) is True
    assert ROAValidity.is_invalid(validity) is False
    assert ROAValidity.is_valid(validity) is False
    validity, routed = trie.get_validity(ip_network("1.2.4.0/24"), routed_origin)
    assert validity == ROAValidity.INVALID_LENGTH
    assert routed == ROARouted.ROUTED
    assert ROAValidity.is_unknown(validity) is False
    assert ROAValidity.is_invalid(validity) is True
    assert ROAValidity.is_valid(validity) is False
    validity, routed = trie.get_validity(ip_network("1.2.3.0/24"), routed_origin + 1)
    assert validity == ROAValidity.INVALID_ORIGIN
    assert routed == ROARouted.ROUTED
    assert ROAValidity.is_unknown(validity) is False
    assert ROAValidity.is_invalid(validity) is True
    assert ROAValidity.is_valid(validity) is False
    validity, routed = trie.get_validity(ip_network("1.2.4.0/24"), routed_origin + 1)
    assert validity == ROAValidity.INVALID_LENGTH_AND_ORIGIN
    assert routed == ROARouted.ROUTED
    assert ROAValidity.is_unknown(validity) is False
    assert ROAValidity.is_invalid(validity) is True
    assert ROAValidity.is_valid(validity) is False
    validity, routed = trie.get_validity(ip_network("1.2.0.255"), routed_origin)
    assert validity == ROAValidity.INVALID_LENGTH
    assert routed == ROARouted.ROUTED
    validity, routed = trie.get_validity(ip_network("1.3.0.0/16"), routed_origin)
    assert validity == ROAValidity.UNKNOWN
    assert routed == ROARouted.UNKNOWN
    validity, routed = trie.get_validity(ip_network("1.2.0.255"), routed_origin)
    assert validity == ROAValidity.INVALID_LENGTH
    assert routed == ROARouted.ROUTED
