# TOOLS — pacts_power_vault

> What this project uses and what for. Maintained by the handoff motion: whenever
> a tool is used here, add or bump its row.
> Types: `Skill` · `MCP` · `CLI` · `App` · `Service` · `Site` · `Library` · `Data` · `Task`
> A `~` before a date means inferred, not observed. `—` means unknown.
>
> ⚠️ This vault is **dormant** — last real commit 2026-07-29, and everything since
> enablement has been automated Obsidian Git backups. Expect most rows below to
> age into the master table's 90-day stale section.

## Active

| Tool | Type | Used for | Access | Last used | Cost | Notes |
|---|---|---|---|---|---|---|
| **Obsidian** | App | The vault itself — Pacts & Power session notes, lore, session HTML pages | desktop | 2026-07-29 | Free | — |
| **obsidian-git** | Library | Auto-commit/backup of the vault | Obsidian plugin | 2026-07-29 | Free | The only thing still committing here |
| **templater-obsidian** | Library | Session/NPC/Item note templates | Obsidian plugin | ~2026-05-31 | Free | — |
| **smart-connections** | Library | Semantic search across the vault | Obsidian plugin | ~2026-05-31 | Free | — |
| **obsidian-5e-statblocks** | Library | Rendering monster/NPC statblocks | Obsidian plugin | ~2026-05-31 | Free | — |
| **chatgpt-md** | Library | In-vault chat against notes | Obsidian plugin | ~2026-06-05 | Free (own key) | Only vault with this plugin |
| **AssemblyAI** | Service | mp3 → session transcript | api.assemblyai.com | ~2026-05-31 | Paid | `Workflows/pp_transcribe.js` — this vault never got the watcher-based pipeline |
| **Supabase** | Service | `Rectrix_Caedere` — rolls and sessions for Pacts & Power | project `vtrtyagltwdrbastpppl` | ~2026-07-22 | Free tier | 437 rolls + 142 spells backfilled; wired per `PACTS_POWER_PROJECT_INSTRUCTIONS_TRIMMED.md` |
| **ddb-roll-sync** | App | Chrome extension feeding Pacts & Power rolls into Supabase | `Septentrion/Workflows/ddb-roll-sync` | ~2026-07-22 | Free | The vault-local copy is archived; the shared extension is the live one |
| **D&D Beyond** | Site | Source of roll and character data | dndbeyond.com | ~2026-07-22 | Paid | — |
| **08-MCP_Workspace** | Data | Scratch workspace for MCP-driven note operations | `08-MCP_Workspace/` | ~2026-07-29 | Free | No `.mcp.json` at this vault root — reached via global MCP config |
| **Node.js + npm** | CLI | Running `pp_transcribe.js` | local install | ~2026-05-31 | Free | — |
| **git** | CLI | Version control, handoff motion | `C:\Program Files\Git` | 2026-07-29 | Free | — |
| **GitHub** | Service | Remote host for `TheLittlestAskew/pacts_power_vault` | github.com | 2026-07-29 | Free | — |
| **Claude Code** | App | Session notes, backfills, handoffs | CLI / IDE extension | 2026-07-29 | Paid | — |
| **septentrion-sync** | Skill | Rolls this vault's tool table into the master | `~/.claude/skills/septentrion-sync` | 2026-09-02 | Free | ⚠️ In `TOOLS_REPOS` but **not** `REPOS` — and a stranded `Ephemeris/pacts_power_vault.md` from 2026-08-27 is still feeding stale data to SystemHorizon |

## Retired

| Tool | Type | Was used for | Retired | Why |
|---|---|---|---|---|
| ~~**Vault-local `ddb-roll-sync` copy**~~ | App | Per-vault copy of the roll-sync extension | 2026-06-15 | ✅ Archived to `Septentrion/Workflows/_archive/`; the shared extension replaced it |
