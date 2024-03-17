from ipaddress import ip_network

from roa_checker import ROA, ROARouted, ROAValidity


def test_roa_validity_valid():
    roa = ROA()
    roa.add_data(ip_network("1.2.0.0/16"), 1)
    validity, routed = roa.get_validity(ip_network("1.2.0.0/16"), 1)
    assert validity == ROAValidity.VALID
    assert routed == ROARouted.ROUTED


def test_roa_validity_unknown():
    roa = ROA()
    roa.add_data(ip_network("1.3.0.0/16"), 1)
    validity, routed = roa.get_validity(ip_network("1.2.0.0/16"), 2)
    assert validity == ROAValidity.UNKNOWN
    assert routed == ROARouted.UNKNOWN


def test_roa_validity_invalid_length():
    roa = ROA()
    roa.add_data(ip_network("1.2.0.0/16"), 1)
    validity, routed = roa.get_validity(ip_network("1.2.3.0/24"), 1)
    assert validity == ROAValidity.INVALID_LENGTH
    assert routed == ROARouted.ROUTED


def test_roa_validity_invalid_origin():
    roa = ROA()
    roa.add_data(ip_network("1.2.0.0/16"), 1)
    validity, routed = roa.get_validity(ip_network("1.2.0.0/16"), 0)
    assert validity == ROAValidity.INVALID_ORIGIN
    assert routed == ROARouted.ROUTED


def test_roa_validity_invalid_length_and_origin():
    roa = ROA()
    roa.add_data(ip_network("1.2.0.0/16"), 1)
    validity, routed = roa.get_validity(ip_network("1.2.3.0/24"), 2)
    assert validity == ROAValidity.INVALID_LENGTH_AND_ORIGIN
    assert routed == ROARouted.ROUTED


def test_roa_routed():
    roa = ROA()
    roa.add_data(ip_network("1.2.0.0/16"), 0)
    validity, routed = roa.get_validity(ip_network("1.2.3.0/24"), 2)
    assert validity == ROAValidity.INVALID_LENGTH_AND_ORIGIN
    assert routed == ROARouted.NON_ROUTED


def test_multiple_roa_valid():
    """If you have multiple ROAs, always choose the most valid"""
    roa = ROA()
    roa.add_data(ip_network("1.2.0.0/16"), 1)
    roa.add_data(ip_network("1.2.0.0/16"), 2)
    validity, routed = roa.get_validity(ip_network("1.2.0.0/16"), 1)
    assert validity == ROAValidity.VALID
    assert routed == ROARouted.ROUTED


def test_multiple_roa_invalid():
    """If you have multiple ROAs, always choose the most valid"""
    roa = ROA()
    roa.add_data(ip_network("1.2.0.0/16"), 1)
    roa.add_data(ip_network("1.2.0.0/16"), 2)
    validity, routed = roa.get_validity(ip_network("1.2.0.0/16"), 3)
    assert validity == ROAValidity.INVALID_ORIGIN
    assert routed == ROARouted.ROUTED
