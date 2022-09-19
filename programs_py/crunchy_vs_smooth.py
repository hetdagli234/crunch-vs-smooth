# crunchy_vs_smooth
# Built with Seahorse v0.1.6


from seahorse.prelude import *

# This will be updated once we do build the project, your program id can be found at crunchy_vs_smooth/target/idl/[your_project_name].json
declare_id("Fo9d34XdUczXdNt9jkqrQseyUQys9bmTDC31utY3zt5x")


# Here we define all our instructions, each of the method below as an RPC end point which can be invoked by clients.
@instruction
def init(owner: Signer, voter: Empty[VoteAccount], vote_account_bump: u8):
    # As a new user connects, we create a new voter PDA account for him and intialize the account.
    init_voter = voter.init(payer=owner, seeds=["Voter"])
    init_voter.owner = owner.key()
    init_voter.bump = vote_account_bump


# To vote crunchy
@instruction
def vote_crunchy(owner: Signer, vote: VoteAccount):
    assert owner.key() == vote.owner, "This is not your Vote account!"
    vote.crunchy += 1


# To vote smooth
@instruction
def vote_smooth(owner: Signer, vote: VoteAccount):
    assert owner.key() == vote.owner, "This is not your Vote account!"
    vote.smooth += 1


# Here we define the account required to be passed on to the instructions above.
class VoteAccount(Account):
    owner: Pubkey
    crunchy: u64
    smooth: u64
    bump: u8
