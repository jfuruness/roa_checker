from lib_cidr_trie import CIDRTrie
from lib_cidr_trie.cidr_trie import PrefixType

from .roas_node import ROAsNode
from .enums_and_dataclasses import ROARouted, ROAValidity, ROAOutcome
from .roa import ROA


class ROATrie(CIDRTrie[PrefixType]):
    """Trie of CIDRs for ROAs"""

    # Just changing the defaults here to ROA instead of CIDRNode
    def __init__(self, *args, NodeCls: type[ROAsNode] = ROAsNode, **kwargs) -> None:
        # mypy doesn't understand that I can reset the default arg in this way
        super(ROATrie, self).__init__(*args, NodeCls=NodeCls, **kwargs)  # type: ignore

    def get_relevant_roas(self, prefix: PrefixType) -> frozenset[ROA]:
        """Returns all relevant ROAs for a given prefix

        This is a bit non-intuitive, because you'd think that all ROAs relevant
        for a given prefix would be __at the prefix__. But this isn't the case.
        They could be higher up the trie, and simply have a __max length__ that
        is >= your prefix length. So you need to collect all ROAs all the way down,
        and for each ROA, determine if it's relevant, and then return them
        """

        self._validate_prefix(prefix)
        bits = self._get_binary_str_from_prefix(prefix)
        node = self.root
        roas: list[ROA] = list()
        for bit in bits[: prefix.prefixlen]:
            next_node = node.right if bool(int(bit)) else node.left
            if next_node is None:
                return frozenset(roas)
            elif next_node.prefix is not None:
                # Add ROAs if they are relevant
                assert isinstance(next_node, ROAsNode), "for mypy"
                for roa in next_node.roas:
                    if roa.covers_prefix(prefix):
                        roas.append(roa)
            node = next_node
        return frozenset(roas)

    def get_roa_outcome(self, prefix: PrefixType, origin: int) -> ROAOutcome:
        """Gets the validity and roa routed vs non rotued of a prefix-origin pair

        This can get fairly complicated, since there can be multiple ROAs
        for the same announcement, and each ROA can have a different validity.
        Essentially, we need to calculate the best validity for a given announcement
        and then that's the validity that should be used. I.e. the "most valid" roa
        is the one that should be used
        """

        relevant_roas = self.get_relevant_roas(prefix)

        if relevant_roas:
            # Return the best ROAOutcome
            rv = sorted([x.get_outcome(prefix, origin) for x in relevant_roas])[0]
            assert isinstance(rv, ROAOutcome), "for mypy"
            return rv
        else:
            return ROAOutcome(validity=ROAValidity.UNKNOWN, routed=ROARouted.UNKNOWN)
