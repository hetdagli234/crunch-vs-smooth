import * as anchor from "@project-serum/anchor";
import { web3, Program } from "@project-serum/anchor";
import { assert } from "chai";
import { CrunchyVsSmooth } from "../target/types/crunchy_vs_smooth";

describe("crunchy_vs_smooth", () => {
  // Configure the client to use the local cluster.
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.CrunchyVsSmooth as Program<CrunchyVsSmooth>;

  const [voter, bump] = web3.PublicKey.findProgramAddressSync(
    [Buffer.from("Voter")],
    program.programId
  );

  console.log(bump);

  it("Initialized the voter!", async () => {
    await program.methods
      .init(bump)
      .accounts({
        owner: provider.wallet.publicKey,
        voter: voter,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .rpc();

    let currentVoteAccountState = await program.account.voteAccount.fetch(
      voter
    );
    assert.equal(0, currentVoteAccountState.crunchy.toNumber());
    assert.equal(0, currentVoteAccountState.smooth.toNumber());
  });

  it("Vote Smooth", async () => {
    const voteSmooth = await program.methods
      .voteSmooth()
      .accounts({ vote: voter })
      .rpc();

    let currentVoteAccountState = await program.account.voteAccount.fetch(
      voter
    );

    assert.equal(1, currentVoteAccountState.smooth.toNumber());
  });

  it("Vote Crunchy", async () => {
    const voteCrunchy = await program.methods
      .voteCrunchy()
      .accounts({ vote: voter })
      .rpc();

    let currentVoteAccountState = await program.account.voteAccount.fetch(
      voter
    );

    assert.equal(1, currentVoteAccountState.crunchy.toNumber());
  });
});
