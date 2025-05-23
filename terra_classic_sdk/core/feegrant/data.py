"""feegrant module data objects."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional

import attr
from attr import converters
from dateutil import parser
from terra_proto.cosmos.feegrant.v1beta1 import (
    AllowedMsgAllowance as AllowedMsgAllowance_pb,
)
from terra_proto.cosmos.feegrant.v1beta1 import BasicAllowance as BasicAllowance_pb
from terra_proto.cosmos.feegrant.v1beta1 import (
    PeriodicAllowance as PeriodicAllowance_pb,
)

from terra_classic_sdk.core import Coins
from terra_classic_sdk.util.converter import to_isoformat
from terra_classic_sdk.util.json import JSONSerializable

__all__ = ["BasicAllowance", "PeriodicAllowance", "AllowedMsgAllowance", "Allowance"]


@attr.s
class BasicAllowance(JSONSerializable):
    """
    BasicAllowance implements Allowance with a one-time grant of tokens
    that optionally expires. The grantee can use up to SpendLimit to cover fees.
    """

    spend_limit: Optional[Coins] = attr.ib(converter=converters.optional(Coins))
    expiration: Optional[datetime] = attr.ib(
        converter=converters.optional(parser.parse)
    )

    type_amino = "feegrant/BasicAllowance"
    type_url = "/cosmos.feegrant.v1beta1.BasicAllowance"

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "spend_limit": self.spend_limit.to_amino()
                if self.spend_limit
                else None,
                "expiration": to_isoformat(self.expiration)
                if self.expiration
                else None,
            },
        }

    def to_data(self) -> dict:
        return {
            "spend_limit": self.spend_limit.to_data() if self.spend_limit else None,
            "expiration": to_isoformat(self.expiration) if self.expiration else None,
        }

    @classmethod
    def from_amino(cls, amino: dict) -> BasicAllowance:
        data = amino.get("value")
        sl = data.get("spend_limit") or None
        exp = data.get("expiration") or None
        return cls(
            spend_limit=Coins.from_amino(sl) if sl else None,
            expiration=exp if exp else None,
        )

    @classmethod
    def from_data(cls, data: dict) -> BasicAllowance:
        sl = data.get("spend_limit")
        exp = data.get("expiration")
        return cls(
            spend_limit=Coins.from_data(sl) if sl else None,
            expiration=exp if exp else None,
        )

    def to_proto(self) -> BasicAllowance_pb:
        return BasicAllowance_pb(
            spend_limit=self.spend_limit.to_proto() if self.spend_limit else [],
            expiration=self.expiration,
        )

    @classmethod
    def from_proto(cls, proto: BasicAllowance_pb) -> BasicAllowance:
        sl = proto.spend_limit
        exp = proto.expiration
        return cls(
            spend_limit=Coins.from_proto(sl) if sl else None,
            expiration=exp if exp else None,
        )


@attr.s
class PeriodicAllowance(JSONSerializable):
    """
    PeriodicAllowance extends Allowance to allow for both a maximum cap,
     as well as a limit per time period.
    """

    basic: BasicAllowance = attr.ib()
    period: int = attr.ib(converter=int)
    period_spend_limit: Coins = attr.ib(converter=Coins)
    period_can_spend: Coins = attr.ib(converter=Coins)
    period_reset: datetime = attr.ib(converter=parser.parse)

    type_amino = "feegrant/PeriodicAllowance"
    """"""
    type_url = "/cosmos.feegrant.v1beta1.PeriodicAllowance"
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "basic": self.basic.to_amino(),
                "period": str(self.period),
                "period_spend_limit": self.period_spend_limit.to_amino(),
                "period_can_spend": self.period_can_spend.to_amino(),
                "period_reset": to_isoformat(self.period_reset),
            },
        }

    @classmethod
    def from_amino(cls, amino: dict) -> PeriodicAllowance:
        data = amino.get("value")
        return cls(
            basic=BasicAllowance.from_amino(data.get("basic")),
            period=int(data.get("period")),
            period_spend_limit=Coins.from_amino(data.get("period_spend_limit")),
            period_can_spend=Coins.from_amino(data.get("period_can_spend")),
            period_reset=data.get("period_reset"),
        )

    @classmethod
    def from_data(cls, data: dict) -> PeriodicAllowance:
        return cls(
            basic=BasicAllowance.from_data(data["basic"]),
            period=data["period"],
            period_spend_limit=Coins.from_data(data["period_spend_limit"]),
            period_can_spend=Coins.from_data(data["period_can_spend"]),
            period_reset=data["period_reset"],
        )

    def to_proto(self) -> PeriodicAllowance_pb:
        return PeriodicAllowance_pb(
            basic=self.basic.to_proto(),
            period=timedelta(seconds=self.period),
            period_spend_limit=self.period_spend_limit.to_proto(),
            period_can_spend=self.period_can_spend.to_proto(),
            period_reset=self.period_reset,
        )

    @classmethod
    def from_proto(cls, proto: PeriodicAllowance_pb) -> PeriodicAllowance:
        return cls(
            basic=BasicAllowance.from_proto(proto.basic),
            period=proto.period.seconds(),
            period_spend_limit=proto.period_spend_limit,
            period_can_spend=proto.period_can_spend,
            period_reset=proto.period_reset,
        )


@attr.s
class AllowedMsgAllowance(JSONSerializable):
    """
    AllowedMsgAllowance creates allowance only for specified message types.
    """

    allowance: Allowance = attr.ib()
    allowed_messages: List[str] = attr.ib(converter=list)

    type_amino = "feegrant/AllowedMsgAllowance"
    """"""
    type_url = "/cosmos.feegrant.v1beta1.AllowedMsgAllowance"
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "allowance": self.allowance.to_amino(),
                "allowed_messages": self.allowed_messages,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> AllowedMsgAllowance:
        allowance = data["allowance"]
        return cls(
            allowance=Allowance.from_data(allowance),
            allowed_messages=data["allowed_messages"],
        )

    def to_proto(self) -> AllowedMsgAllowance_pb:
        return AllowedMsgAllowance_pb(
            allowance=self.allowance.to_proto(), allowed_messages=self.allowed_messages
        )


class Allowance(JSONSerializable, ABC):  # (BasicAllowance, PeriodicAllowance):
    @property
    @abstractmethod
    def type_url(self):
        pass

    @property
    @abstractmethod
    def type_amino(self):
        pass

    @abstractmethod
    def to_amino(self) -> dict:
        pass

    @abstractmethod
    def to_data(self) -> dict:
        pass

    @abstractmethod
    def to_proto(self) -> dict:
        pass

    @classmethod
    def from_data(cls, data: dict):
        if data.get("@type") == BasicAllowance.type_url:
            return BasicAllowance.from_data(data)
        elif data.get("@type") == AllowedMsgAllowance.type_url:
            return AllowedMsgAllowance.from_data(data)
        else:
            return PeriodicAllowance.from_data(data)

    @classmethod
    def from_amino(cls, data: dict):
        if data.get("type") == BasicAllowance.type_amino:
            return BasicAllowance.from_amino(data)
        else:
            return PeriodicAllowance.from_amino(data)

    @classmethod
    def from_proto(cls, data: any):
        if data.get("@type") == BasicAllowance.type_url:
            return BasicAllowance.from_proto(data)
        else:
            return PeriodicAllowance.from_proto(data)
