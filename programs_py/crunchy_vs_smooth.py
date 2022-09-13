# crunchy_vs_smooth
# Built with Seahorse v0.1.6

from seahorse.prelude import *

declare_id("Fo9d34XdUczXdNt9jkqrQseyUQys9bmTDC31utY3zt5x")


class VoteAccount(Account):
    owner: Pubkey
    crunchy: u64
    smooth: u64
    bump: u8


@instruction
def init(owner: Signer, voter: Empty[VoteAccount], vote_account_bump: u8):
    init_voter = voter.init(payer=owner, seeds=["Voter"])
    init_voter.bump = vote_account_bump


@instruction
def vote_crunchy(vote: VoteAccount):
    vote.crunchy += 1


@instruction
def vote_smooth(vote: VoteAccount):
    vote.smooth += 1
