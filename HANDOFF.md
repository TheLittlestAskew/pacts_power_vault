# HANDOFF — pacts_power_vault

> Obsidian D&D vault for the "Pacts & Power" campaign. Includes session HTML pages, 08-MCP_Workspace, Templates, Workflows.
> Handoff is **enabled** for this repo. Every change updates the DO NEXT block below and prepends a log entry.
> Note: this is a notes/content vault — most session-note edits won't have a "next dev step." Use the DO NEXT block for things like next-session prep if useful, or leave it as "—".

## ▶ DO NEXT
— No in-flight task. Everything committed here since enablement was an automated Obsidian Git backup, not deliberate work.

---

## Log
<!-- newest first · one entry per logical task/session · timestamp · source · changed · commit · next -->

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
