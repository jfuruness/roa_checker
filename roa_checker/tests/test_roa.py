from ipaddress import ip_network

from roa_checker import ROA, ROARouted, ROAValidity


def test_roa_outcome_valid():
    roa = ROA(ip_network("1.2.0.0/16"), 1)
    validity = roa.get_validity(ip_network("1.2.0.0/16"), 1)
    assert validity == ROAValidity.VALID
    outcome = roa.get_outcome(ip_network("1.2.0.0/16"), 1)
    assert outcome.validity == ROAValidity.VALID
    assert outcome.routed == ROARouted.ROUTED
    assert roa.routed == ROARouted.ROUTED


def test_roa_outcome_unknown():
    roa = ROA(ip_network("1.3.0.0/16"), 1)
    validity = roa.get_validity(ip_network("1.2.0.0/16"), 2)
    assert validity == ROAValidity.UNKNOWN
    outcome = roa.get_outcome(ip_network("1.2.0.0/16"), 2)
    assert outcome.validity == ROAValidity.UNKNOWN
    assert outcome.routed == ROARouted.ROUTED
    assert roa.routed == ROARouted.ROUTED


def test_roa_validity_invalid_length():
    roa = ROA(ip_network("1.2.0.0/16"), 1)
    validity = roa.get_validity(ip_network("1.2.3.0/24"), 1)
    assert validity == ROAValidity.INVALID_LENGTH
    outcome = roa.get_outcome(ip_network("1.2.3.0/24"), 1)
    assert outcome.validity == ROAValidity.INVALID_LENGTH
    assert outcome.routed == ROARouted.ROUTED
    assert roa.routed == ROARouted.ROUTED


def test_roa_validity_invalid_origin():
    roa = ROA(ip_network("1.2.0.0/16"), 1)
    validity = roa.get_validity(ip_network("1.2.0.0/16"), 0)
    assert validity == ROAValidity.INVALID_ORIGIN
    outcome = roa.get_outcome(ip_network("1.2.0.0/16"), 0)
    assert outcome.validity == ROAValidity.INVALID_ORIGIN
    assert outcome.routed == ROARouted.ROUTED
    assert roa.routed == ROARouted.ROUTED


def test_roa_validity_invalid_length_and_origin():
    roa = ROA(ip_network("1.2.0.0/16"), 1)
    validity = roa.get_validity(ip_network("1.2.3.0/24"), 2)
    assert validity == ROAValidity.INVALID_LENGTH_AND_ORIGIN
    outcome = roa.get_outcome(ip_network("1.2.3.0/24"), 2)
    assert outcome.validity == ROAValidity.INVALID_LENGTH_AND_ORIGIN
    assert outcome.routed == ROARouted.ROUTED
    assert roa.routed == ROARouted.ROUTED


def test_roa_non_routed():
    roa = ROA(ip_network("1.2.0.0/16"), 0)
    outcome = roa.get_outcome(ip_network("1.2.3.0/24"), 2)
    assert outcome.validity == ROAValidity.INVALID_LENGTH_AND_ORIGIN
    assert outcome.routed == ROARouted.NON_ROUTED
