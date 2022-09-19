use anchor_lang::prelude::*;
use anchor_lang::solana_program;
use anchor_spl::associated_token;
use anchor_spl::token;
use std::convert::TryFrom;

declare_id!("Fo9d34XdUczXdNt9jkqrQseyUQys9bmTDC31utY3zt5x");

pub fn init_handler(mut ctx: Context<Init>, mut vote_account_bump: u8) -> Result<()> {
    let mut owner = &mut ctx.accounts.owner;
    let mut voter = &mut ctx.accounts.voter;
    let mut init_voter = voter;

    init_voter.owner = owner.key();

    init_voter.bump = vote_account_bump;

    Ok(())
}

pub fn vote_crunchy_handler(mut ctx: Context<VoteCrunchy>) -> Result<()> {
    let mut owner = &mut ctx.accounts.owner;
    let mut vote = &mut ctx.accounts.vote;

    require!(owner.key() == vote.owner, ProgramError::E000);

    vote.crunchy += 1;

    Ok(())
}

pub fn vote_smooth_handler(mut ctx: Context<VoteSmooth>) -> Result<()> {
    let mut owner = &mut ctx.accounts.owner;
    let mut vote = &mut ctx.accounts.vote;

    require!(owner.key() == vote.owner, ProgramError::E000);

    vote.smooth += 1;

    Ok(())
}

#[derive(Debug)]
#[account]
pub struct VoteAccount {
    owner: Pubkey,
    crunchy: u64,
    smooth: u64,
    bump: u8,
}

#[derive(Accounts)]
# [instruction (vote_account_bump : u8)]
pub struct Init<'info> {
    #[account(mut)]
    pub owner: Signer<'info>,
    #[account(
        init,
        payer = owner,
        seeds = ["Voter".as_bytes().as_ref(), owner.key().as_ref()],
        bump,
        space = 8 + std::mem::size_of::<VoteAccount>()
    )]
    pub voter: Box<Account<'info, VoteAccount>>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct VoteCrunchy<'info> {
    #[account(mut)]
    pub owner: Signer<'info>,
    #[account(mut)]
    pub vote: Box<Account<'info, VoteAccount>>,
}

#[derive(Accounts)]
pub struct VoteSmooth<'info> {
    #[account(mut)]
    pub owner: Signer<'info>,
    #[account(mut)]
    pub vote: Box<Account<'info, VoteAccount>>,
}

#[program]
pub mod crunchy_vs_smooth {
    use super::*;

    pub fn init(ctx: Context<Init>, vote_account_bump: u8) -> Result<()> {
        init_handler(ctx, vote_account_bump)
    }

    pub fn vote_crunchy(ctx: Context<VoteCrunchy>) -> Result<()> {
        vote_crunchy_handler(ctx)
    }

    pub fn vote_smooth(ctx: Context<VoteSmooth>) -> Result<()> {
        vote_smooth_handler(ctx)
    }
}

#[error_code]
pub enum ProgramError {
    #[msg("This is not your Vote account!")]
    E000,
}
