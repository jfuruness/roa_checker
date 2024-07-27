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


I can expand these if anyone actually uses this repo (lmk @ jfuruness@gmail.com)

```python
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
```

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
* 2.0.0
    * Previously the ROA checker would only look at the ROAs that were the most specific prefix (and then would check all of those ROAs)
        * This is a problem because if there were two ROAs, one that is less specific and valid, and one that is more specific and invalid, the announcements would be considered invalid incorrectly.
        * Fixing this unfortunately causes some of the public methods to change (they were wrong before anyways) like get_roa (you can't get a ROA for a prefix, you need to get all ROAs for that prefix)
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
