# CLAUDE.md — Pacts & Power Campaign Archive

This is the orientation file for working on the **Pacts & Power** (PP) D&D 5E campaign archive in Claude Code. Read this first, then open the authoritative rule files it points to before doing real work.

---

## WHAT THIS PROJECT IS

A complete, accurate, verifiable archive of the "Pacts & Power" campaign (Ravnica / Magic: The Gathering setting), built and maintained by Taylor "Tayls" Ritchie. The archive lives in an Obsidian vault that doubles as the campaign wiki. The work is processing session transcripts and D&D Beyond roll data into structured session notes and vault pages.

**DM:** Chris (heavyhart). **Taylor's character:** Orphea "Orphie" Levistus, Tiefling Barbarian (Path of the Totem Warrior). Party ("The Breakfast Club"): Orphie, Ogre, Rin, Sanis, Varis. Current party level: 12.

---

## HOW TO WORK IN CLAUDE CODE (read this)

Claude Code works **directly against the local filesystem and the terminal**. This is the whole reason the project moved here, so behave accordingly:

- **Vault writes:** edit and create vault `.md` files directly on disk. Do **not** route vault writes through the Obsidian MCP or a Filesystem MCP. There is no size cap on direct disk writes, so large transcripts and long session notes are fine.
- **Scripts:** run the existing automation scripts in the terminal (see Scripts section). Do not reimplement what a script already does.
- **Supabase:** query the roll archive via the Supabase MCP configured for this project (see Roll Archive section).
- **KEEP IN CHAT, NOT HERE:** Orphie's in-character POV journal entries (`02-Character_Journal/`). That is voice-dependent creative writing Taylor does interactively in the Claude.ai chat with her voice skills. In Claude Code, you may paste the POV Overview verbatim into the journal during a vault update, but do **not** author new journal prose here.

---

## AUTHORITATIVE RULE FILES (do not duplicate, go read them)

These are the source of truth. This CLAUDE.md is only a pointer and a quick-reference. When anything here conflicts with these files, **the files win**.

| File | What it governs |
|---|---|
| `Workflows/PACTS___POWER_PROJECT_INSTRUCTIONS_051826.md` | Master ruleset: roles, constraints, source authority, roll archive docs, full file index. Highest authority among instruction files. |
| `Workflows/Pacts___Power_Convo_1_Instrucions.md` | Convo 1 process: session notes generation (spell check, transcript correction, roll queries, notes, title, `.docx` output, handoff block). |
| `Workflows/PACTS___POWER_CONVO_2_INSTRUCTIONS.md` | Convo 2 process: the full numbered vault-update checklist, character page maintenance, backlinks, file naming. |
| `Workflows/PP_SESSION_NOTES_SECTION_BREAKDOWN.md` | Section-by-section content expectations and required table/column formats for session notes. |
| `Workflows/PP_Session_Notes_v8_Style_Guide.md` | Color palette, fonts, heading styles, table shading, spacing for the `.docx`. Read before generating any `.docx`. |
| `Templates/PP_Session_Notes_Template_v8.docx` | Visual authority for `.docx` output. If the Style Guide is ambiguous, inspect this directly. |
| `DND_Sources/Pacts_Power_Spelling_Dictionary.md` | Canonical spellings for PCs, NPCs, guilds, locations, artifacts, MTG/Ravnica terms. |

---

## NON-NEGOTIABLE CONSTRAINTS (always apply)

These are small enough to keep in context at all times. Violating any of these corrupts the archive.

- **No invention.** Never create connective narrative, paraphrase quotes, or invent motives, events, characters, or rolls. Unknown or ambiguous data is tagged `[Unknown/Ambiguous]`. The **only** exception is Orphie's POV Overview, which is in-character interpretation.
- **Verbatim quotes only.** Dialogue is exact, word for word. Never paraphrase a quote.
- **No silent spelling fixes.** Spelling correction is **disabled by default**. Do not normalize names, terms, or rules language unless explicitly told to (e.g., "correct spelling in this transcript"). Even when authorized, raw transcript text is never rewritten unless explicitly asked; normalization applies to notes, trackers, and indexes. When applied, add the disclosure line: `Spelling normalized per user request using campaign reference files. Verbatim transcript text unchanged.`
- **No session contamination.** Sessions are delineated by real-world play date. Never pull from later sessions to rewrite earlier ones. Preserve discrepancies and flag them.
- **No metagaming.** Do not predict or reveal future plot points from published Ravnica/MTG lore. Log only what the transcript states or implies.
- **No DM override.** D&D rules and Ravnica/MTG lore are context only, never canon. Chris's rulings are indisputable.
- **Universal date keying.** Every data point is tagged with its originating real-world session date.
- **Attribution care.** If a DM line might belong to an NPC, flag it and ask. Do not guess the speaker.

**Source authority (highest to lowest):** Chris (DM) > recordings > transcripts > session notes > campaign reference files > D&D Beyond / Ravnica / MTG reference.

### POV Overview / journal hard limits
Orphie's POV is grounded in her perspective, in-world and in-character. **Never include:** OOC speech, above-table logistics, metagame knowledge (dice numbers, spell names as mechanics, stat blocks, HP, levels), player uncertainty or process, DM rulings as rulings, or real names / campaign / session references. The test: could Orphie know, feel, or observe this from inside the story? If no, leave it out.

---

## VAULT

**Local path:** `C:\Users\theli\pacts_power_vault`
**GitHub:** `TheLittlestAskew/pacts_power_vault` (private). The Obsidian Git plugin auto-commits and pushes every 10 minutes, so no manual backup is needed; just write to disk.

```
pacts_power_vault/
├── 00-Campaign-Hub/      Dashboard, House Rules, Loot Tracker, Quote Board,
│                         Profanity Ledger, Vault Sync Status
├── 01-Sessions/          One file per session (+ Early Sessions/)
├── 02-Character_Journal/ Orphie POV entries  (authored in chat, not here)
├── 03-Characters/        01 PCs/, 02 NPCs/, The Breakfast Club.md
├── 04-World-Lore/        Districts/, Factions/, Guilds/, Locations/, Planes/
├── 05-Mechanics/         Roll_Statistics.md, Spell_Usage.md
├── 06-Media/
├── 07-Flora_Fauna/       Creatures/, Plants_Fungi/
├── DND_Sources/          Spelling dicts, character list, Lore Dump.md
├── Session_Sources/
│   ├── Recordings/
│   └── Transcripts/      Raw_Unedited/, Corrected/
├── Templates/
└── Workflows/            Scripts + instruction files
```

---

## THE TWO WORKFLOWS

**Convo 1 — Session Notes Generation.** Turns a corrected transcript + roll data into the full `.docx` session notes, picks a title, and produces a handoff block. Mechanical and structured parts run well here in Claude Code (corrections, roll queries, encounter tables, roll logs, `.docx` build). Follow `Pacts___Power_Convo_1_Instrucions.md`.

**Convo 2 — Vault Update.** Takes the completed notes and writes/updates every relevant vault file. This is the best fit for Claude Code: direct disk writes, no MCP timeouts. Follow the numbered checklist in `PACTS___POWER_CONVO_2_INSTRUCTIONS.md`. Quick map of the 19 items:

- **Before writing:** read `DND_Sources/` (esp. `Lore Dump.md`), the Campaign Dashboard, and `Vault Sync Status.md` (start at the first ❌).
- **00-Campaign-Hub (1–9):** Dashboard sessions table, party assets, guild status, planeswalkers, active quests; then House Rules, Loot Tracker, Quote Board, Profanity Ledger (keep running campaign totals).
- **01-Sessions (10):** write `PP_##_MMDDYY_Title.md` with `[[backlinks]]` to characters, locations, guilds, items.
- **02-Character_Journal (11):** paste Orphie POV Overview exactly as in the notes, no edits.
- **03-Characters (12–13):** update each PC page; create/update NPC pages.
- **04-World-Lore (14–15):** locations/districts, guilds/factions/planes.
- **05-Mechanics (16):** new mechanics or first-time features.
- **07-Flora_Fauna (17–18):** non-PC-race creatures; plants/fungi.
- **Sync (19):** mark this session's columns ✅ in `Vault Sync Status.md`.

**Backlink + naming conventions** live in the Convo 2 file. Sessions: `PP_##_MMDDYY_Title_With_Underscores.md` (zero-padded number, real play date MMDDYY, title matches the final chosen title exactly). PCs/NPCs/locations: by name (`Orphie.md`, `Vraska.md`, `New Prahv.md`).

---

## ROLL ARCHIVE (Supabase)

All D&D Beyond rolls live in Postgres on Supabase, queried via the Supabase MCP (`execute_sql`).

- **Project ID:** `vtrtyagltwdrbastpppl`
- **This campaign only:** `campaign_id = 2` (game_id `3661522`). Tables: `ddb_campaigns`, `ddb_rolls`.

**Standard session query (note the Eastern Time cast, this is required):**
```sql
SELECT * FROM ddb_rolls
WHERE campaign_id = (SELECT id FROM ddb_campaigns WHERE game_id = 3661522)
AND DATE(timestamp_iso AT TIME ZONE 'America/New_York') = 'YYYY-MM-DD';
```

**Must-know quirks:**
- **Date filtering must use `America/New_York`,** not UTC. Cast before `DATE()` or session-day filtering will be wrong.
- **Sanis and Rin roll outside D&D Beyond.** Zero or near-zero DDB roll counts for them are expected, not query errors. Their rolls come from the transcript; tag those `transcript-only`.
- **Physical dice** also won't appear in DDB. If the transcript confirms a result, include it and mark `physical dice roll`.
- **DM-controlled creatures** appear in the log and are not party members. `"custom"` actions are usually freeform DM-prompted rolls; use the transcript for context.
- **Sync gap check** before trusting completeness:
  ```sql
  SELECT MAX(timestamp_iso) FROM ddb_rolls WHERE campaign_id = 2;
  ```
  If the data Taylor is asking about looks missing, surface it and ask whether she has synced; do not fabricate.

**Cross-reference rule:** archive = exact roll values, timing, who rolled. Transcript = narrative context, DM rulings, in-fiction outcomes, dialogue.

---

## SCRIPTS (`Workflows/`)

Run these in the terminal; don't reimplement them.

```bash
# Transcribe a session recording (AssemblyAI). Output -> Session_Sources/Transcripts/Raw_Unedited/
cd C:\Users\theli\pacts_power_vault\Workflows\pp_transcribe
node pp_transcribe.js                 # interactive picker
node pp_transcribe.js session13.mp3   # specific file
node pp_transcribe.js --speakers 7 session13.mp3   # guest session

# Spelling corrector. Output -> Session_Sources/Transcripts/Corrected/  (-Corrected appended)
cd C:\Users\theli\pacts_power_vault\Workflows
python pacts_spelling_corrector.py --dry-run          # preview, writes nothing
python pacts_spelling_corrector.py --file 03-081025-Pacts.md
python pacts_spelling_corrector.py                    # batch all raw transcripts
python pacts_spelling_corrector.py --report           # batch + CSV audit reports
```

D&D Beyond roll sync is a **Chrome extension** (`ddb-roll-sync/`), not a terminal command. Taylor loads it unpacked, scrolls a DDB dice log to capture the token, then clicks **Sync All Campaigns** in the popup to upsert rolls into Supabase. Usage and troubleshooting live in `ddb-roll-sync/README.md`. She runs it manually after a session, so synced rolls may lag the session by a few hours. (The old browser-console script `ddb_sync_supabase.js` is superseded by this extension.)

---

## STYLE NOTES FOR TAYLOR

- Outputs may be humorous but never at the expense of accuracy, precision, or detail.
- Ignore real-life player chatter, bio-breaks, scheduling, and tech talk entirely.
- Avoid emdashes where a comma, semicolon, or colon works.
- Give clear, scannable structure and concrete next steps.

---

## ⚠️ VERIFY THESE PATHS

This file assumes the instruction `.md` files sit in `Workflows/` and the template/style guide split between `Workflows/` and `Templates/`. If the actual on-disk locations or filenames differ (note: `Pacts___Power_Convo_1_Instrucions.md` has a known spelling quirk), update the paths in the **Authoritative Rule Files** table above so they match your vault exactly.
