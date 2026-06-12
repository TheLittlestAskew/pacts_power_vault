# DDB Party Sheet Sync — Pacts & Power

A one-time archival pull of **The Breakfast Club's** D&D Beyond character sheets into the
vault. Ported from the SITL/Ashfall sync.

> **Pacts & Power is complete** (ended 2026-05-31). There is no pipeline watcher in this
> vault, so this runs **manually** — it captures the party's final sheets, it doesn't
> auto-refresh.

Uses DDB's character service (`character-service.dndbeyond.com/character/v5/...`). Anonymous
by default (Public sheets only); with a Cobalt token it also fetches **Campaign-Only** sheets.

## Roster & IDs

Character IDs come straight from the Campaign Dashboard (`00-Campaign-Hub/Campaign Dashboard.md`),
recorded in `ddb_party.json`. Output files are named after the **real character name** read from
each fetched sheet, so the registry only needs IDs.

| PC | Player | characterId | Anonymous fetch |
| --- | --- | --- | --- |
| Orphie Levistus | Taylor | 73462645 | ✅ Public |
| Ogre (Ur-Ogre-lan) | Chet | 78340271 | ✅ Public |
| Rin (Rinestra Genleth) | Rachel | 87915377 | ✅ Public |
| Varis Aestra | Vincent | 77072065 | ✅ Public |
| Braun | Clay | 102457478 | ✅ Public |
| Sanis Reylana | Gabe | 80474774 | 🔒 Campaign-Only (needs token) |
| Lance | Tenthebrutal | — | no ID on record |

So 5 of 7 fetch with no login; **Sanis** needs a Cobalt token, and **Lance** has no
characterId recorded.

## Run

```powershell
cd C:\Users\theli\pacts_power_vault\Workflows
node ddb_party_sync.js
```

Output (the hand-written `<Name> - Character Sheet.md` notes in that folder are **not** touched):

- `03-Characters/01 PCs/Party Character Sheets/_raw/<CharacterName>.json` — full raw JSON
- `03-Characters/01 PCs/Party Character Sheets/<CharacterName> (DDB).md` — readable sheet

## To also fetch Sanis (Campaign-Only)

1. Log in to D&D Beyond → **F12 → Application → Cookies → `https://www.dndbeyond.com`** → copy
   **`CobaltSession`**.
2. Put it in the vault `.env`:  `DDB_COBALT=<value>`  (commented placeholder already there).
   `.env` is gitignored — **keep it secret.** It's account-wide (same value as your other vaults).
3. Re-run. It mints a short-lived Bearer from your Cobalt cookie each run.

## Privacy — this repo is PUBLIC

The generated sheets (`_raw/*.json` + `<Name> (DDB).md`) are **gitignored** so other players'
sheets aren't republished to a public repo. They live in your local vault only. To publish them
anyway, remove those two lines from `.gitignore`.
