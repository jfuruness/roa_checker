from dataclasses import dataclass
from functools import cached_property
from ipaddress import IPv4Network, IPv6Network

from .enums_and_dataclasses import ROAOutcome, ROARouted, ROAValidity


@dataclass(frozen=True)
class ROA:
    prefix: IPv4Network | IPv6Network
    origin: int
    max_length: int = None  # type: ignore
    # RIPE, ARIN, etc. Used by ROACollector, don't remove
    ta: str | None = None

    def __post_init__(self) -> None:
        if self.max_length is None:
            object.__setattr__(  # type: ignore
                self, "max_length", self.prefix.prefixlen
            )

    @cached_property
    def routed_status(self) -> ROARouted:
        return ROARouted.ROUTED if self.is_routed else ROARouted.NON_ROUTED

    @cached_property
    def is_routed(self) -> bool:
        return self.origin != 0

    @cached_property
    def is_non_routed(self) -> bool:
        return not self.is_routed

    def covers_prefix(self, prefix: IPv4Network | IPv6Network) -> bool:
        """Returns True if the ROA covers the prefix"""

        # NOTE: subnet_of includes the original prefix (I checked lol)
        # mypy wants this to be the same type of prefix but this doesn't matter
        return prefix.subnet_of(self.prefix)  # type: ignore

    def get_validity(
        self, prefix: IPv4Network | IPv6Network, origin: int
    ) -> ROAValidity:
        """Returns validity of prefix origin pair"""

        if self.covers_prefix(prefix):
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
        else:
            return ROAValidity.UNKNOWN

    def get_outcome(self, prefix: IPv4Network | IPv6Network, origin: int) -> ROAOutcome:
        """Returns outcome of prefix origin pair"""

        validity = self.get_validity(prefix, origin)
        return ROAOutcome(validity=validity, routed_status=self.routed_status)
