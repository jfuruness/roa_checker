from lib_cidr_trie import CIDRTrie
from lib_cidr_trie.cidr_trie import PrefixType

from .roa import ROA
from .enums import ROARouted, ROAValidity


class ROATrie(CIDRTrie[PrefixType]):
    """Trie of CIDRs for ROAs"""

    # Just changing the defaults here to ROA instead of CIDRNode
    def __init__(self, *args, NodeCls: type[ROA] = ROA, **kwargs) -> None:
        # mypy doesn't understand that I can reset the default arg in this way
        super(ROATrie, self).__init__(*args, NodeCls=NodeCls, **kwargs)  # type: ignore

    def get_validity(
        self, prefix: PrefixType, origin: int
    ) -> tuple[ROAValidity, ROARouted]:
        """Gets the validity of a prefix-origin pair"""

        roa = self.get_most_specific_trie_supernet(prefix)
        assert roa is None or isinstance(roa, ROA), "mypy type check"
        if roa:
            return roa.get_validity(prefix, origin)
        else:
            return ROAValidity.UNKNOWN, ROARouted.UNKNOWN
