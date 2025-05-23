"""Gov module data types."""

from __future__ import annotations

import json
from datetime import datetime
from typing import List
import attr
from dateutil import parser
from terra_proto.cosmos.gov.v1beta1 import Proposal as Proposal_pb, ProposalStatus
from terra_proto.cosmos.gov.v1beta1 import TallyResult as TallyResult_pb
from terra_proto.cosmos.gov.v1beta1 import Vote as Vote_pb
from terra_proto.cosmos.gov.v1beta1 import VoteOption
from terra_proto.cosmos.gov.v1beta1 import WeightedVoteOption as WeightedVoteOption_pb

from terra_classic_sdk.core import AccAddress, Coins
from terra_classic_sdk.util.json import JSONSerializable
from terra_classic_sdk.util.converter import to_isoformat
from terra_classic_sdk.util.parse_proposal_msg import ProposalMsg,parse_proposal_msg

__all__ = ["Proposal", "ProposalMsg", "VoteOption", "WeightedVoteOption", "ProposalStatus"]


@attr.s
class TallyResult(JSONSerializable):
    yes: str = attr.ib()
    abstain: str = attr.ib()
    no: str = attr.ib()
    no_with_veto: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "yes": self.yes,
            "abstain": self.abstain,
            "no": self.no,
            "no_with_veto": self.no_with_veto,
        }

    def to_data(self) -> dict:
        return {
            "yes": self.yes,
            "abstain": self.abstain,
            "no": self.no,
            "no_with_veto": self.no_with_veto,
        }

    @classmethod
    def from_data(cls, data: dict) -> TallyResult:
        return cls(
            yes=data["yes"],
            abstain=data["abstain"],
            no=data["no"],
            no_with_veto=data["no_with_veto"],
        )

    def to_proto(self) -> TallyResult_pb:
        return TallyResult_pb(
            yes=self.yes,
            abstain=self.abstain,
            no=self.no,
            no_with_veto=self.no_with_veto,
        )


@attr.s
class Proposal(JSONSerializable):
    """Contains information about a submitted proposal on the blockchain."""

    proposal_id: int = attr.ib(converter=int)
    """Proposal's ID."""

    proposal_msgs: list[ProposalMsg] = attr.ib()
    """Proposal contents."""

    status: str = attr.ib()
    """Status of proposal."""

    final_tally_result: TallyResult = attr.ib()
    """Final tallied result of the proposal (after vote)."""

    submit_time: datetime = attr.ib()
    """Timestamp at which proposal was submitted."""

    deposit_end_time: datetime = attr.ib()
    """Time at which the deposit period ended, or will end."""

    total_deposit: Coins = attr.ib(converter=Coins)
    """Total amount deposited for proposal"""

    voting_start_time: datetime = attr.ib()
    """Time at which voting period started, or will start."""

    voting_end_time: datetime = attr.ib()
    """Time at which voting period ended, or will end."""

    metadata: str = attr.ib()
    """metadata of proposal."""

    title: str = attr.ib()
    """title of proposal."""

    summary: str = attr.ib()
    """description of proposal."""

    proposer:AccAddress=attr.ib()
    """proposer of proposal."""

    def to_amino(self) -> dict:
        return {
            "proposal_id": str(self.proposal_id),
            "proposal_msgs": [x.to_amino() for x in self.proposal_msgs],
            "status": self.status,
            "final_tally_result": self.final_tally_result.to_amino(),
            "submit_time": to_isoformat(self.submit_time),
            "deposit_end_time": to_isoformat(self.deposit_end_time),
            "total_deposit": self.total_deposit.to_amino(),
            "voting_start_time": to_isoformat(self.voting_start_time),
            "voting_end_time": to_isoformat(self.voting_end_time),
            "metadata": self.metadata,
            "title": self.title,
            "summary": self.summary,
            "proposer": self.proposer
        }

    @classmethod
    def from_data(cls, data: dict) -> Proposal:
        if data["voting_start_time"] is None:
            voting_start_time = ""
        else:    
            voting_start_time = parser.parse(data["voting_start_time"])
        
        if data["voting_end_time"] is None:
            voting_end_time = ""
        else:
            voting_end_time = parser.parse(data["voting_end_time"])

        return cls(
            proposal_id=data["id"],
            proposal_msgs=[parse_proposal_msg(x) for x in data['messages']] if data['messages'] else [],
            status=data["status"],
            final_tally_result=data["final_tally_result"],
            submit_time=parser.parse(data["submit_time"]),
            deposit_end_time=parser.parse(data["deposit_end_time"]),
            total_deposit=Coins.from_data(data["total_deposit"]),
            voting_start_time=voting_start_time,
            voting_end_time=voting_end_time,
            metadata=data['metadata'],
            title=data['title'],
            summary=data['summary'],
            proposer=data['proposer']
        )

    def to_proto(self) -> Proposal_pb:
        return Proposal_pb(
            proposal_id=self.proposal_id,
            status=ProposalStatus.from_str(self.status),
            final_tally_result=self.final_tally_result.to_proto(),
            submit_time=self.submit_time,
            deposit_end_time=self.deposit_end_time,
            total_deposit=self.total_deposit.to_proto(),
            voting_start_time=self.voting_start_time,
            voting_end_time=self.voting_end_time,
        )


@attr.s
class WeightedVoteOption(JSONSerializable):
    weight: str = attr.ib()
    option: VoteOption = attr.ib()

    def to_amino(self) -> dict:
        return {"weight": self.weight, "option": self.option.name}

    def to_data(self) -> dict:
        return {"weight": self.weight, "option": self.option.name}

    @classmethod
    def from_data(cls, data: dict) -> WeightedVoteOption:
        return cls(option=data["option"], weight=data["weight"])

    def to_proto(self) -> WeightedVoteOption_pb:
        return WeightedVoteOption_pb(option=self.option, weight=self.weight)


@attr.s
class Vote(JSONSerializable):
    proposal_id: int = attr.ib(converter=int)
    voter: AccAddress = attr.ib()
    options: List[WeightedVoteOption] = attr.ib(converter=list)

    def to_amino(self) -> dict:
        return {
            "proposal_id": str(self.proposal_id),
            "voter": self.voter,
            "options": [opt.to_amino() for opt in self.options],
        }

    def to_data(self) -> dict:
        return {
            "proposal_id": str(self.proposal_id),
            "voter": self.voter,
            "options": [opt.to_data() for opt in self.options],
        }

    @classmethod
    def from_data(cls, data: dict) -> Vote:
        return cls(
            proposal_id=data["proposal_id"],
            voter=data["voter"],
            options=data["options"],
        )

    def to_proto(self) -> Vote_pb:
        return Vote_pb(
            proposal_id=self.proposal_id, voter=self.voter, options=self.options
        )
