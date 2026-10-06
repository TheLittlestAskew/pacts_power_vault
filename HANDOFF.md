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

### 2026-10-06 11:30 ET · Claude Code (banked 21 session notes that had been dirty long enough to become the fleet's worst outlier)

- **Changed:** Banked work that was already finished on disk but had never been committed. **Nothing was authored here and no canon was edited.**
  - **21 files gained a `campaign:` frontmatter property** (`- Pacts & Power`), and three of them additionally had their YAML reformatted by Obsidian's property editor — inline arrays (`["Orphie", "Ogre", …]`) expanded into block lists and quoted scalars unquoted. That reformatting is lossless; the same keys, re-expressed.
  - ⭐ **The property and the untracked `01-Sessions/PP_Session_Base.base` are one unit of work, not two coincidences.** The Base filters on `campaign == ["Pacts & Power"]`, so without the backfill its table renders empty. Banked together.
  - 🛑 **Proved no prose was lost rather than inferring it from the diffstat.** Three files showed deletions, which on canon files is not something to wave through. Compared each note's **post-frontmatter body byte-for-byte against `HEAD`**, with line endings normalised: **21 of 21 identical, 0 bodies changed.** The deletions were entirely the reformatted YAML keys.
- **Commit:** `(this entry)`
- **Next:** Unchanged.
- **Follow-up, same session:** 🛑 **`Ogre.png` is now gitignored rather than committed, and the reason got stronger on a second look.** The Stop guard kept counting it as unbanked, so it needed resolving — and checking the fleet first changed the answer. The other four vaults **do** track images (`skitl_vault` 33, `wtff_vault` 47, `Dimension20` 11, `ashfall_vault` 2), so "repos here don't track images" was wrong as a general rule. ⚠️ **But this repo is PUBLIC, and its own `.gitignore` already documents why images are the exception here:** the privacy screen reads only `.md/.json/.txt/.canvas/.base/.html`, so **an image is invisible to it**, and a binary in a public repo cannot be un-published by a later commit. ✓ **Ignored, not deleted — the exact pattern this file already uses for `wtff_vault/`** ("its fate is still Taylor's call, and it is untracked data"). The file is untouched on disk. ▶ **To resolve: look at it, then either delete the ignore line and commit it into a proper media folder, or move it out of the repo.** 📌 It is very likely just a character portrait — Ogre is a party member and PP_18 is literally titled *"Hi_Im_Ogre"* — but *very likely* is not the standard for a public repo.
- **Watch out:** 🛑 **`Ogre.png` was deliberately NOT committed and is still untracked.** It is **1.9 MB**, dated **2026-06-09**, sits at the **vault root**, and **this repo tracks zero `.png` files** — so committing it would not be banking a loose end, it would be setting a new convention that this vault stores images in git. ▶ **Needs Taylor's call:** keep it out and move it somewhere, gitignore images here, or decide the repo does track art and commit it deliberately. ⚠️ **How this surfaced is worth noting:** nothing was watching. It took the 07:15 `mirror-freshness` run reporting `pacts_power_vault: uncommitted:23` — the dirtiest repo in the fleet by a wide margin — for anyone to look. The monitoring found it; no human did.

### 2026-10-01 15:30 ET · Claude Code — Taylor ruled on wtff_vault/: leave it. Recorded so it stops being re-raised.
- **Changed:** Added the ruling to `CLAUDE.md`'s DO NOT list, the file Claude Code auto-loads, which is where the 12:40 session correctly put the archive rule for the same reason. **Taylor's decision: leave `wtff_vault/` exactly as it is.** No deletion, no repairing its `.git`, no merging. It is already neutralised by the `473ba6b` gitignore, so there is no outstanding risk attached to the decision.
- **Commit:** `pending — this entry's own commit`
- **Next:** Unchanged. Still a "do not work here" notice.
- **Watch out:** 📌 **The reason this is written in `CLAUDE.md` rather than only here: two separate sessions have now independently flagged that folder and mis-diagnosed it the same way** (as an embedded repo with a divergent HEAD, which it does not have). A third would cost Taylor the same attention for the third time. The auto-loaded file is the only place that reliably prevents that, which is the same argument the 12:40 entry made about the archive rule itself.

### 2026-10-01 15:20 ET · Claude Code — closed a route by which this PUBLIC repo could have committed the wtff_vault/ copy
- **Changed:** `wtff_vault/` added to `.gitignore`. **Acted on under exception (1) in this vault's `CLAUDE.md` — a privacy/security issue in a public repo — and under the listed DO item about "a shared `.gitignore` pattern that other public vaults received and this one did not."** Same category as the `screencapture-*` rule in `dfec4e8`. 🛑 **The hazard, demonstrated before the fix, not assumed:** `git add --dry-run -- 'wtff_vault/HANDOFF.md'` **succeeded**. That folder's `.git` has **no `refs/` directory**, which makes it an invalid git dir, so git discovery walks up and every git command run from inside it silently operates on **this** repo. Its `HANDOFF.md` sat at **exactly 15 entries against the rotation cap of 15**, and `Handoff Log Rotate` scans **two levels deep** so it enrols that folder — one more entry and the task would have rewritten the file, staged it as `wtff_vault/HANDOFF.md`, and **self-banked it into this public repo as a routine-looking `chore: rotate HANDOFF.md log` commit.** ✅ After the ignore the same `git add` is refused with exit 1, and `audit-public` stops attributing that folder to this repo: scanned **377 → 370**, findings **48 → 46**.
- **Commit:** `473ba6b`
- **Next:** Unchanged, and deliberately so. The DO NEXT block above stays a "do not work here" notice; this was an exception, not a resumption of work.
- **Watch out:** ⚠️ **Correcting the 12:40 entry below:** it described `wtff_vault/` as *"an embedded git repo… with a divergent HEAD and its own dirty tree."* **There is no divergent HEAD.** The HEAD, origin and dirty tree git reported from inside that folder were **this repo's own**, because its `.git` is invalid and git walked up. I made the same mistake twice before checking `rev-parse --show-toplevel`; it is a genuinely easy one, and the tell is that `git -C <nested>` agreed exactly with the parent on every value. 🛑 **Ignored, NOT deleted — the folder still needs Taylor's ruling.** It is untracked data: 21 of its 24 top-level files are byte-identical to the real `wtff_vault`, and the 3 that differ (`HANDOFF.md`, `TOOLS.md`, `.gitignore`) are stale copies from 09-05, 09-02 and 08-24. 📌 The 21 modified `PP_*` session notes remain pre-existing and untouched; this commit was scoped to `.gitignore` alone.

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
