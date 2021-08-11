# lib\_roa\_checker
This package contains a trie of ROAs for fast prefix-origin pair lookups

* [Usage](#usage)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [Licence](#license)
* [TODO](#todo)

## Usage
* [lib\_roa\_checker](#lib_roa_checker)

```python
from ipaddress import ip_network

from lib_roa_checker import ROAChecker, ROAValidity


rpki = ROAChecker()
# prefix, origin, max_length
rpki.add_roa(ip_network("1.2.0.0/16", 1, 16)

validity: ROAValidity = rpki.get_validity(ip_network("1.2.0.0/16", 1))
```

## Installation
* [lib\_roa\_checker](#lib_roa_checker)

Install python and pip if you have not already. Then run:

```bash
pip3 install lib_roa_checker
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/jfuruness/lib_roa_checker.git
cd lib_roa_checker
python3 setup.py develop
```

To test the development package: [Testing](#testing)


## Testing
* [lib\_cidr_trie](#lib_roa_checker)

You can test the package if in development by moving/cd into the directory where setup.py is located and running:
(Note that you must have all dependencies installed first)
```python3 setup.py test```


## Development/Contributing
* [lib\_roa\_checker](#lib_roa_checker)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Email me at jfuruness@gmail.com because I don't check github messages

## History
* [lib\_roa\_checker](#lib_roa_checker)
* 0.0.1 First working version

## Credits
* [lib\_roa\_checker](#lib_roa_checker)


## License
* [lib\_roa\_checker](#lib_roa_checker)

BSD License (see license file)

## TODO
* [lib\_roa\_checker](#lib_roa_checker)
* Needs better testing
* Would be nice to have some traversal funcs
