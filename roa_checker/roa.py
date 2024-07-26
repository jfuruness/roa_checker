from dataclasses import dataclass
from functools import cached_property
from ipaddress import IPv4Network, IPv6Network
from typing import Optional

from .enums_and_dataclasses import ROAOutcome, ROARouted, ROAValidity


@dataclass(frozen=True, slots=True)
class ROA:
    prefix: IPv4Network | IPv6Network
    origin: int
    max_length: Optional[int] = None

    def __post_init__(self) -> None:
        if self.max_length is None:
            object.__setattr__(self, "max_length", self.prefix.prefixlen)

    @cached_property
    def roa_routed(self) -> ROARouted:
        return ROARouted.NON_ROUTED if self.origin == 0 else ROARouted.ROUTED

    def covers_prefix(self, prefix: IPv4Network | IPv6Network) -> bool:
        """Returns True if the ROA covers the prefix"""

        # NOTE: subnet_of includes the original prefix (I checked lol)
        return prefix.subnet_of(self.prefix)

    def get_validity(
        self, prefix: IPv4Network | IPv6Network, origin: int
    ) -> ROAValidity:
        """Returns validity of prefix origin pair"""

        if prefix.prefixlen > self.max_length and origin != self.origin:
            return ROAValidity.INVALID_LENGTH_AND_ORIGIN
        elif prefix.prefixlen > self.max_length and origin == self.origin:
            return ROAValidity.INVALID_LENGTH
        elif prefix.prefixlen <= self.max_length and origin != self.origin:
            return ROAValidity.INVALID_ORIGIN
        elif prefix.prefixlen <= self.max_length and origin == self.origin:
            return ROAValidity.VALID
        else:
            raise NotImplementedError("This should never happen")

    def get_outcome(self, prefix: IPv4Network | IPv6Network, origin: int) -> ROAOutcome:
        """Returns outcome of prefix origin pair"""

        validity = self.get_validity(prefix, origin)
        return ROAOutcome(validity=validity, routed=self.roa_routed)
