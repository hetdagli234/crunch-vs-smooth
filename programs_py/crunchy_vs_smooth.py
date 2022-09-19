# crunchy_vs_smooth
# Built with Seahorse v0.1.6


from seahorse.prelude import *

# This will be updated once the project is build, your program id can be found at crunchy_vs_smooth/target/idl/[your_project_name].json
declare_id("Fo9d34XdUczXdNt9jkqrQseyUQys9bmTDC31utY3zt5x")


# Here we define all our instructions, each of the method below as an RPC end point which can be invoked by clients.
@instruction
def init(owner: Signer, voter: Empty[VoteAccount], vote_account_bump: u8):
    # As a new user connects, we create a new voter PDA account for him and intialize the account.
    init_voter = voter.init(payer=owner, seeds=["Voter", owner])
    # Assign the owner or the Signer of the one initialize the accouunt to the user's newly created VoteAccount owner.
    init_voter.owner = owner.key()
    # Assign the bump to the one initializing the accouunt to the user's newly created VoteAccount bump.
    init_voter.bump = vote_account_bump


# To vote crunchy
@instruction
def vote_crunchy(owner: Signer, vote: VoteAccount):
    # Check if the public key of the signer is the same as the owner in the vote account.
    assert owner.key() == vote.owner, "This is not your Vote account!"
    # Increment the crunchy variable in the user's VoteAccount
    vote.crunchy += 1


# To vote smooth
@instruction
def vote_smooth(owner: Signer, vote: VoteAccount):
    # Check if the public key of the signer is the same as the owner in the vote account.
    assert owner.key() == vote.owner, "This is not your Vote account!"
    # Increment the smooth variable in the user's VoteAccount
    vote.smooth += 1


# Defining the account which will be stored on-chain for every unique wallet interacting with our program.
class VoteAccount(Account):
    owner: Pubkey
    crunchy: u64
    smooth: u64
    bump: u8
