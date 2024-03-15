[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
![Tests](https://github.com/jfuruness/bgpy/actions/workflows/tests.yml/badge.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-2A6DBA.svg)](http://mypy-lang.org/)

# roa\_checker
This package contains a trie of ROAs for fast prefix-origin pair lookups

* [Usage](#usage)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Licence](#license)

## Usage
* [roa\_checker](#roa_checker)

```python
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
        assert trie.get_roa(cidr, routed_origin).prefix == cidr
        validity, routed = trie.get_validity(cidr, routed_origin)
        assert validity, routed == (ROAValidity.VALID, ROARouted.ROUTED,)
        assert ROAValidity.is_unknown(validity) is False
        assert ROAValidity.is_invalid(validity) is False
        assert ROAValidity.is_valid(validity) is True


    non_routed_cidrs = [ip_network(x) for x in ["2.2.0.0/16", "2.2.3.0/24", "2.2.3.4"]]
    non_routed_origin = 0
    for cidr in non_routed_cidrs:
        trie.insert(cidr, non_routed_origin, cidr.prefixlen)
    for cidr in non_routed_cidrs:
        assert trie.get_roa(cidr, non_routed_origin).prefix == cidr
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
```

## Installation
* [roa\_checker](#roa_checker)

Install python and pip if you have not already. Then run:

```bash
pip3 install roa_checker
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/jfuruness/roa_checker.git
cd roa_checker
pip3 install -e .[test]
pre-commit install
```

To test the development package: [Testing](#testing)


## Testing
* [roa\_checker](#roa_checker)

After installation for development:

```bash
cd roa_checker
python3 -m pytest roa_checker
```

To run all tests:

```bash
tox
```

## Development/Contributing
* [roa\_checker](#roa_checker)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Email me at jfuruness@gmail.com if I don't see it after a while

## History
* [roa\_checker](#roa_checker)
* 1.1.4 Bug fix for multiple ROA case where multiple ROAs would result in the least valid ROA being selected, rather than the most valid ROA being selected. Thanks for finding this Cameron Morris!
* 1.1.3 Dependency updates
* 1.1.2 Added ROA to top level import
* 1.1.1 mypy and linter fixes
* 1.1.0 Updated test deps
* 1.0.0 Updated package structure, typing, linters, etc, made ROAValidity contains multiple invalid types
* 0.0.1 First working version


## License
* [roa\_checker](#roa_checker)

BSD License (see license file)
