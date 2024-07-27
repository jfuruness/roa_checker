from ipaddress import ip_network

from roa_checker import ROAChecker, ROARouted, ROAValidity, ROAOutcome, ROA


def test_tree():
    # TODO: Break up into unit tests
    trie = ROAChecker()
    cidrs = [ip_network(x) for x in ["1.2.0.0/16", "1.2.3.0/24", "1.2.3.4"]]
    routed_origin = 1
    for cidr in cidrs:
        trie.insert(cidr, ROA(cidr, routed_origin, cidr.prefixlen))
    for cidr in cidrs:
        outcome = trie.get_roa_outcome(cidr, routed_origin)
        assert outcome == ROAOutcome(ROAValidity.VALID, ROARouted.ROUTED)
        assert ROAValidity.is_unknown(outcome.validity) is False
        assert ROAValidity.is_invalid(outcome.validity) is False
        assert ROAValidity.is_valid(outcome.validity) is True

    non_routed_cidrs = [ip_network(x) for x in ["2.2.0.0/16", "2.2.3.0/24", "2.2.3.4"]]
    non_routed_origin = 0
    for cidr in non_routed_cidrs:
        trie.insert(cidr, ROA(cidr, non_routed_origin, cidr.prefixlen))
    for cidr in non_routed_cidrs:
        outcome = trie.get_roa_outcome(cidr, routed_origin)
        assert outcome == ROAOutcome(ROAValidity.INVALID_ORIGIN, ROARouted.NON_ROUTED)

    outcome = trie.get_roa_outcome(ip_network("1.0.0.0/8"), routed_origin)
    assert outcome.validity == ROAValidity.UNKNOWN
    assert outcome.routed == ROARouted.UNKNOWN
    outcome = trie.get_roa_outcome(ip_network("255.255.255.255"), routed_origin)
    assert outcome.validity == ROAValidity.UNKNOWN
    assert outcome.routed == ROARouted.UNKNOWN
    assert ROAValidity.is_unknown(outcome.validity) is True
    assert ROAValidity.is_invalid(outcome.validity) is False
    assert ROAValidity.is_valid(outcome.validity) is False
    outcome = trie.get_roa_outcome(ip_network("1.2.4.0/24"), routed_origin)
    assert outcome.validity == ROAValidity.INVALID_LENGTH
    assert outcome.routed == ROARouted.ROUTED
    assert ROAValidity.is_unknown(outcome.validity) is False
    assert ROAValidity.is_invalid(outcome.validity) is True
    assert ROAValidity.is_valid(outcome.validity) is False
    outcome = trie.get_roa_outcome(ip_network("1.2.3.0/24"), routed_origin + 1)
    assert outcome.validity == ROAValidity.INVALID_ORIGIN
    assert outcome.routed == ROARouted.ROUTED
    assert ROAValidity.is_unknown(outcome.validity) is False
    assert ROAValidity.is_invalid(outcome.validity) is True
    assert ROAValidity.is_valid(outcome.validity) is False
    outcome = trie.get_roa_outcome(ip_network("1.2.4.0/24"), routed_origin + 1)
    assert outcome.validity == ROAValidity.INVALID_LENGTH_AND_ORIGIN
    assert outcome.routed == ROARouted.ROUTED
    assert ROAValidity.is_unknown(outcome.validity) is False
    assert ROAValidity.is_invalid(outcome.validity) is True
    assert ROAValidity.is_valid(outcome.validity) is False
    outcome = trie.get_roa_outcome(ip_network("1.2.0.255"), routed_origin)
    assert outcome.validity == ROAValidity.INVALID_LENGTH
    assert outcome.routed == ROARouted.ROUTED
    outcome = trie.get_roa_outcome(ip_network("1.3.0.0/16"), routed_origin)
    assert outcome.validity == ROAValidity.UNKNOWN
    assert outcome.routed == ROARouted.UNKNOWN
    outcome = trie.get_roa_outcome(ip_network("1.2.0.255"), routed_origin)
    assert outcome.validity == ROAValidity.INVALID_LENGTH
    assert outcome.routed == ROARouted.ROUTED


def test_multiple_differing_roas():
    """Testing that all ROAs are considered

    This test has one less specific ROA that is valid with a long max length
    and one more specific roa that is invalid

    This should result in a valid ROA
    """

    # TODO: Break up into unit tests
    trie = ROAChecker()
    valid_ip_addr = ip_network("1.2.0.0/16")
    invalid_ip_addr = ip_network("1.2.3.0/24")
    trie.insert(valid_ip_addr, ROA(valid_ip_addr, 1, 24))
    trie.insert(invalid_ip_addr, ROA(invalid_ip_addr, 2, 24))
    assert trie.get_roa_outcome(invalid_ip_addr, 1).validity == ROAValidity.VALID
