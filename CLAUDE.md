# Pacts & Power — READ THIS FIRST

## 🛑 This campaign is OVER. This vault is an archive, not a workstream.

**Pacts & Power is no longer an active campaign.** Do not expect updates here.
Do not treat a long gap since the last commit as a problem to solve, and do not
read a ⚠️ stale flag in the vault's `Return Point` as something needing action —
**for this repo, cold is the correct and permanent state.**

## Why it is still here

This was Taylor's **original guinea pig**. The processes that now run every other
campaign — the session pipeline, the handoff motion, the tool inventory, the
roll archive — were invented and debugged here first. The repo holds a lot of
information about *how those processes came to exist*, which is why it is kept
rather than deleted.

Its data also **stays in Rectrix Caedere**. Do not propose removing P&P rows,
views, or dashboard entries from that project either.

## 🛑 DO NOT

- **Do not ask Taylor to make changes to this vault.** Not tidy-ups, not format
  migrations, not "while we're here" fixes, not bringing it in line with how the
  newer vaults do things. The answer is no and asking costs her attention.
- **Do not open items in `## ▶ DO NEXT`** expecting them to be worked. The block
  is deliberately empty.
- Do not delete its data from Rectrix Caedere.
- 🛑 **Do not raise `wtff_vault/` again. DECIDED 2026-10-01 by Taylor: leave it.**
  It is a near-duplicate copy of the WtFF vault from before that project was split
  out. 21 of its 24 top-level files are byte-identical to the real `wtff_vault`; the
  3 that differ are stale copies from 09-05, 09-02 and 08-24. Its `.git` has no
  `refs/` directory, so it is an **invalid git dir and git discovery walks up** —
  meaning any git command run from inside it reports *this* repo's state, which is
  why two separate sessions have mis-described it as "an embedded repo with a
  divergent HEAD". It has none. ✅ **It is already neutralised:** `wtff_vault/` is
  gitignored (`473ba6b`), so the one real hazard — `Handoff Log Rotate` scanning two
  levels deep and self-banking that folder's `HANDOFF.md` into this public repo — is
  closed, and `git add` on it now fails. **Nothing further is wanted. Do not propose
  deleting it, fixing its `.git`, or merging it.**

### The only two exceptions

1. **A privacy or security issue.** This repo is **public**. If something here
   leaks personal detail, credentials, account or game IDs, or third-party
   information, act on it and tell her — that is not an interruption, it is the
   one thing she wants raised.
2. **Something genuinely important** that she would regret not knowing. Judge
   this strictly: "could be neater" is never it.

## ✅ DO

**Keep monitoring it when a change somewhere else could reach in here.** The
explicit instruction: *"I don't want it to break because I updated something else
one day."*

So when work elsewhere touches anything shared, check whether this vault is
affected, and say so:

- a renamed Supabase view, table, or column the P&P pages read
- a renamed or moved script, skill, or path this vault depends on
- a change to the handoff / `septentrion-sync` / tool-inventory contracts, since
  this repo is in both `REPOS` and `TOOLS_REPOS`
- anything that alters how Rectrix Caedere serves P&P data
- a shared `.gitignore`, hook, or privacy-screen pattern that other public vaults
  received and this one did not

Monitoring is read-only. Report what you find; do not start fixing it here.

---

*Written 2026-10-01 at Taylor's instruction. Mirrored in `AGENTS.md` and in
`HANDOFF.md`'s DO NEXT block so it is unmissable from any surface.*
