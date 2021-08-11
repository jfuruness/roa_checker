from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# https://stackoverflow.com/a/58534041/8903959
setup(
    name='lib_roa_checker',
    author="Justin Furuness",
    author_email="jfuruness@gmail.com",
    version="0.0.1",
    url='https://github.com/jfuruness/lib_roa_checker.git',
    license="BSD",
    description="Creates a trie of ROAs for fast lookups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["Furuness", "prefix", "cidr", "inet", "trie", "cidr-trie",
              "roas", "roas-trie", "ROA", "ROAs", "ROAs-trie"],
    include_package_data=True,
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "ip_address",
        "lib_cidr_trie",
        "pytest",
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'],
    entry_points={},
)
