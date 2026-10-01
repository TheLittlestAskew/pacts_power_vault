# HANDOFF — pacts_power_vault

> Obsidian D&D vault for the "Pacts & Power" campaign. Includes session HTML pages, 08-MCP_Workspace, Templates, Workflows.
> Handoff is **enabled** for this repo. Every change updates the DO NEXT block below and prepends a log entry.
> Note: this is a notes/content vault — most session-note edits won't have a "next dev step." Use the DO NEXT block for things like next-session prep if useful, or leave it as "—".

## ▶ DO NEXT

🛑 **NOTHING. THIS CAMPAIGN IS OVER AND THIS VAULT IS AN ARCHIVE.** Pacts & Power is no longer active; no updates are expected here and a long gap is correct, not a problem. **A ⚠️ stale flag for this repo in `Return Point` is the permanent, expected state — do not action it.**

🛑 **Do not ask Taylor to make changes to this vault.** Not tidy-ups, not format migrations, not bringing it in line with the newer vaults. The only two exceptions: **(1) a privacy or security issue** — this repo is **public**, so leaked personal detail, credentials, or account/game IDs must be acted on and raised; **(2) something she would genuinely regret not knowing.** "Could be neater" is never either one.

✅ **DO keep monitoring it when a change elsewhere could reach in here** — her words: *"I don't want it to break because I updated something else one day."* Check this vault whenever something shared moves: a renamed Supabase view/table/column, a renamed script or path, a change to the handoff / `septentrion-sync` / tool-inventory contracts (this repo is in **both** `REPOS` and `TOOLS_REPOS`), or anything altering how Rectrix Caedere serves P&P data. **Monitoring is read-only: report, do not fix here.**

📌 **Why it is kept:** this was the original guinea pig. The session pipeline, handoff motion, tool inventory and roll archive were invented and debugged here first, so it records how those processes came to exist. **Its data also stays in Rectrix Caedere — do not propose removing it from there either.**

📄 Full version in `CLAUDE.md` and `AGENTS.md` at this repo root.

---

## Log
<!-- newest first · one entry per logical task/session · timestamp · source · changed · commit · next -->

### 2026-10-01 12:40 ET · Claude Code — marked this vault an ARCHIVE, with the DO/DO NOT in three places

- **Changed:** Recorded Taylor's standing instruction that **this campaign is over and this vault is an archive**: new root `CLAUDE.md` (the file Claude Code auto-loads, so it cannot be missed), a banner at the top of `AGENTS.md` for Codex, and a rewritten `## ▶ DO NEXT` block — which also puts it on the vault dashboard through `septentrion-sync`, replacing a stale "no in-flight task" line.
  - 🛑 **The rule: do not ask her to make changes here.** Not tidy-ups, not format migrations, not bringing this vault in line with the newer ones. Two exceptions only — **a privacy or security issue** (this repo is public), or **something she would genuinely regret not knowing**. "Could be neater" is neither.
  - ✅ **The counterpart, which matters as much: keep monitoring it when a change elsewhere could reach in.** Her words: *"I don't want it to break because I updated something else one day."* Renamed Supabase views/tables/columns, renamed scripts or paths, or changes to the handoff / `septentrion-sync` / tool-inventory contracts — this repo sits in **both** `REPOS` and `TOOLS_REPOS`. **Monitoring is read-only: report, never fix here.**
  - 📌 **Why it is kept:** the original guinea pig. The session pipeline, handoff motion, tool inventory and roll archive were all invented and debugged here first. **Its data also stays in Rectrix Caedere** — do not propose removing it there either.
  - 📌 **A stale/cold flag for this repo in `Return Point` is now the permanent expected state**, not a defect to action.
  - ✅ Applied the `screencapture-*` / `*dash.cloudflare*` gitignore rule under the privacy exception above: this repo is **public** and had no such pattern while `skitl_vault` did. Verified nothing matching was already tracked, so it is preventative and no tracked file was silently dropped from the index.
- **Commit:** `dfec4e8`
- **Next:** Nothing, by design. This block is intentionally a "do not work here" notice rather than a task.
- **Watch out:** ⚠️ **21 modified `PP_*` session notes are sitting uncommitted in this working tree and are NOT from this change** — I scoped the commit to the four files I touched. ⚠️ **`wtff_vault/` is an embedded git repo inside this vault** with a divergent HEAD and its own dirty tree; flagged to Taylor, deliberately not touched. Its `.env` is safely ignored, so it is not a secrets exposure.

### 2026-09-02 22:20 ET · Claude Code (TOOLS.md tool inventory added)
- **Changed:** Added `TOOLS.md` (16 active rows) — Obsidian + its 5 plugins including chatgpt-md, AssemblyAI via `pp_transcribe.js`, Supabase, the shared ddb-roll-sync extension, and the rest. `AGENTS.md` gained a `### TOOLS.md` subsection so Codex maintains it too. One of 13 project tables that `septentrion-sync` v4 rolls into the vault's new `The Toolbox.md`.
- **Commit:** `0e26d6a`
- **Friction:** gen-fail — seeded Node.js here as `Node.js` while nine other projects used `Node.js + npm`, which split one tool into two rows in the master table. The sync's Problems section caught it, not me. Fixed here and in the dashboard table; verified on the next run when shared tools went 31 → 30. The Tool cell is a join key — normalize the name at write time.
- **Next:** Unchanged. See the block above this log.
- **Watch out:** ⚠️ This vault is **dormant** (last real commit 2026-07-29) and the table says so up front, so expect most of its rows in the master's 90-day stale section. The one `Paid` stale row is AssemblyAI — stale because the campaign is, not because a subscription is idling. Separately, `Ephemeris/pacts_power_vault.md` is still frozen at 2026-08-27 and pushing a stale row into SystemHorizon daily; that decision is still open.

### 2026-07-29 20:41 ET · Claude Code
- **Changed:** Removed the retired duplicate `ddb-roll-sync` extension from `Workflows/ddb-roll-sync/`, 6 files. Every copy across the vaults had drifted to a different version, so it is consolidated in one place and writes direct to Rectrix_Caedere. Found by a cross-repo handoff sweep; the deletions were already uncommitted in the working tree and Taylor confirmed they were deliberate. The same cleanup landed in `ashfall_vault` as `e0682ed`.
- **Commit:** `9f77b06`
- **Next:** Unchanged. See the block above this log.
- **Watch out:** ⚠️ A *deletion* commit banked on Taylor's confirmation, not on my own reading of the tree. If a copy is still needed here it is in git history at the parent of `9f77b06`.

### 2026-07-26 11:44 ET · Claude Code
- **Changed:** Added the Handoff Contract to `AGENTS.md` so Codex follows it. Codex reads `AGENTS.md`, never `~/.claude/skills/`, so it had no handoff instructions at all before this.
- **Commit:** `d8bc3ed`
- **Next:** Unchanged. See the block above this log.
- **Watch out:** Log entries must now carry a tool label (`Claude Code` / `Claude desktop` / `Codex` / `ChatGPT`). Do not restructure this file; the dashboard parses it.

### 2026-07-26 11:22 ET · Claude Code
- **Changed:** Backfilled the log for 2026-06-27 → 2026-06-29. Both commits in that window are automated `vault backup:` commits from Obsidian Git, so there is no human work narrative to record.
- **Commit:** `35f733f`, `dd726c6`
- **Next:** Nothing pending. The next real session sets this.
- **Watch out:** Automated backup commits say nothing about what changed in the notes. If you need the content history, read the diffs, not this log.

### 2026-06-23 09:37 ET · Claude chat
- **Changed:** Enabled repo handoff — added this `HANDOFF.md` at root.
- **Commit:** `docs: enable repo handoff`
- **Next:** Set by the next real change to the repo.
