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

from roa_checker import ROAChecker
from lib_roa_validity import ROAValidity


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
* 1.0.0 Updated package structure, typing, linters, etc
* 0.0.1 First working version


## License
* [roa\_checker](#roa_checker)

BSD License (see license file)
