# Vault Sync Status

This file tracks which sessions have been fully processed into vault wiki pages.

**Legend:**
- ✅ = Complete
- 🔶 = Partial (some data extracted)
- ❌ = Not started

## Phase 1: Core Pages (Non-Transcript)

| Category | Status | Notes |
|---|---|---|
| PC Pages (5) | ✅ | Orphie, Ogre, Rin, Sanis, Varis — populated from source files |
| Campaign Dashboard | ✅ | Full overview, quests, guild tracker, timeline |
| Guild Pages (10) | ✅ | All 10 guilds populated from source files |
| The Breakfast Club | ✅ | Party overview page created |
| The Second Sun | ✅ | Faction page created |

## Phase 2: Session-by-Session Extraction (Transcript-Dependent)

| Session | Source | Session File | NPCs | Locations | Loot | Quotes | Encounters |
|---|---|---|---|---|---|---|---|
| Sessions 1–16 | Early Sessions PDF | 🔶 (bullet notes exist) | ❌ | ❌ | ❌ | ❌ | ❌ |
| Transcript 01 (07/13/25) | 01_071325 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (no combat — puzzle session) |
| Transcript 02 (07/27/25) | 02_072725 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Transcript 03 (08/10/25) | 03_081025 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Transcript 04 (08/26/25) | 04_082625 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Transcript 05 (09/07/25) | 05_090725 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Transcript 06 (09/17/25) — [[PP_06_091725_Soul_Integrated_Soul_Storage_Get_It_Right\|Soul Integrated Soul Storage, Get It Right]] | 06_091725 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (RP/exposition — no combat) |
| Transcript 07 (10/05/25) | 07_100525 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Transcript 08 (10/19/25) | 08_101925 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Transcript 09 (11/30/25) | 09_113025 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Transcript 10 (12/14/25) | 10_121425 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Transcript 11 (01/11/26) | 11_011126 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Transcript 12 (01/25/26) | 12_012526 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Phase 3: Cross-Reference & Polish

| Task | Status |
|---|---|
| Backlink audit | ❌ |
| NPC pages from existing file stubs | 🔶 (T01: populated Borborygmos, Vraska, Salena; created Hikara, Benji, Nicol Bolas) |
| Location pages from existing file stubs | 🔶 (T01: created Fortress of Nivix) |
| Loot Tracker | 🔶 (T01 logged) |
| Quote Board Master | 🔶 (T01 logged) |
| Profanity Ledger | 🔶 (T01 logged) |
| House Rules & Rulings | 🔶 (T01 logged) |

## Processing Log

- **Transcript 06 (09/17/25) — Soul Integrated Soul Storage, Get It Right — processed (Convo 2):** Session-notes file already in vault (`01-Sessions/Session Notes/Notes 2025/PP_06_091725_Soul_Integrated_Soul_Storage_Get_It_Right.md`, Convo 1); POV journal created (`PP_06_091725_Orphie_POV.md`, verbatim). Dashboard (3 timeline rows; Quest #1/#5 briefing + #9 resolution; **new Quest #10** Flameseekers/Simic; [[Liliana Vess|Liliana]] + [[Chandra Nalaar|Chandra]] planeswalker statuses; Party Assets: Aphonexa's Blessing + "Sis"/Nexus). All four hub trackers (Loot, Quote Board, Profanity w/ updated campaign totals, House Rules — 3 rulings). 8 DDB rolls (Roll_Statistics per-session row). NPC pages **created** ([[Aphonexa]], [[Liliana Vess]]) and **updated** ([[Salena]] → ascension, [[Onyx]] → Liliana reveal, [[Pippi]] → "Sis"/Nexus, [[Thal]] → revived/Thal Oram, Chandra + [[Isiah Ja-Faank]] → taken to [[Vitu-Ghazi]]). World-lore **created** ([[The Chain Veil]]) and **updated** ([[Bone Mine]] → Aphonexa's seat; [[Vitu-Ghazi]] → stinger). PC: [[Sanis Reylana|Sanis]] (sister's absolution + "seed of renewal"). Creature [[Myconids]] (revived; worship Aphonexa). **Minor deferred (low-value, captured in Dashboard/Loot/Aphonexa):** the shared "Aphonexa's blessing" line on the 4 non-Sanis PC pages, Spell_Usage T06, per-character roll column. **Open flags:** (1) Liliana's contract-break consequence unknown; (2) the Nexus/[[Implicit Maze]] location; (3) the Simic/Flameseekers rescue thread. **.docx skipped per Taylor.**
- **Transcript 05 (09/07/25) — Do You Smell That? It's Breakfast Time — processed (Convo 2):** Session notes file written (`01-Sessions/Session Notes/Notes 2025/PP_05_090725_Do_You_Smell_That_Its_Breakfast_Time.md`); POV journal (`PP_05_090725_Orphie_POV.md`, verbatim); corrected transcript already in vault (`Session_Sources/Transcripts/Corrected/05-090725-Pacts-Corrected.md`). **No spell-check pass (per Taylor).** Dashboard (4 timeline rows; Quest #9 **completed** — Selena rescued/ascended; Immortal Sun → Tezzeret recall; Tezzeret already in Planeswalkers table). All four hub trackers (Loot, Quote Board, Profanity w/ updated totals, House Rules — 11 new rulings). ~85 DDB rolls cross-referenced (Roll_Statistics: per-session + per-character T05 + Notable Rolls; Spell_Usage T05). NPC pages **created** (Tezzeret, Thal) and **updated** (Isiah, Chandra, Salena — major ascension update, Onyx). All 5 PC pages updated (3 enriched existing co-maintained T05 rows; Sanis & Rin added). World-lore **updated** (Bone Mine — major marrow-pits/essence detail; Immortal Sun) and creature **created** (Myconids); Eternals + Strixhaven touched. **Also corrected T04 page level 12→10** per Taylor's date-keying decision (party was level 10 at T04 and T05). **Open flags:** (1) Selena's new ascended nature (ethereal-figure stinger) unresolved; (2) Sanis's claim that Isiah caused Selena's death still not detailed in-source; (3) "the harvest is coming" thread; (4) Immortal Sun whereabouts now that Tezzeret is dead; (5) [[Dolora]] (Rin's deity) spelling unconfirmed. **Note:** layered into co-maintained pages (Orphie/Varis/Ogre already had stub T05 rows — enriched, not duplicated). **.docx skipped per Taylor.**
- **Transcript 04 (08/26/25) — The Spark and the Swarm — processed (Convo 2):** Session notes file written (`01-Sessions/Session Notes/Notes 2025/PP_04_082625_The_Spark_and_the_Swarm.md`); POV journal entry (`PP_04_082625_Orphie_POV.md`, Overview pasted verbatim); corrected transcript saved in Convo 1 (`Session_Sources/Transcripts/Corrected/04_082625_corrected.md`). Dashboard (4 timeline rows, Party Assets: Drawer→Clarissa / Scrappy→Izzet-Dalya / Dragon Spirit Box absorbed Niv essence / new Spark Harvester; Quests #1, #7, #9 updated). All four hub trackers (Loot, Quote Board, Profanity w/ updated campaign totals, House Rules). 16 DDB rolls cross-referenced (Roll_Statistics: per-session + per-character T04 + Notable Rolls; 15/16 matched). NPC pages **created/populated** (Isiah Ja-Faank — was an empty stub) and **updated** (Brula, Chandra, Nissa, Molly, Clarissa, Niv-Mizzet, Salena, Dalya Bara, Ral Zarek); all 5 PC pages updated; Eternals creature updated (painted-on metal); Spark-Harvester Trident (party acquisition); Bone Mine (en route); Spell_Usage T04. **Open flags:** (1) Sanis's claim that Isiah caused Salena's death (Early S4) not yet detailed in-source; (2) "Brula Galadora" surname (single occurrence) not canonized; (3) "Skarrg" (00:23:33) and "Oxon" (00:26:40) garbled; (4) stray 20:15:53 Ogre "Spell Attack" roll with no transcript context; (5) Selena/`Salena` filename spelling. **Resolved this pass:** "EMLA tanks/replicas" = canonical EMLA units (not an error); Scrappy drop-off = Izzet/Dalya (not Golgari). **Chandra (Bri)** logged as a recurring guest companion, kept off the core roster. **Note:** layered into co-maintained shared pages without overwriting later content. **.docx skipped per Taylor.**
- **Transcript 03 (08/10/25) — That's Why No One Will Remember Your Name — processed (Convo 2):** Session notes file written (`01-Sessions/Session Notes/Notes 2025/PP_03_081025_Thats_Why_No_One_Will_Remember_Your_Name.md`); POV journal entry (`PP_03_081025_Orphie_POV.md`); Dashboard (7 timeline rows, Party Assets, Guild Status, Planeswalkers, 3 new quests #7–9); all four hub trackers (Loot, Quote Board, Profanity w/ updated totals, House Rules); 61 DDB rolls cross-referenced (Roll_Statistics: per-session + per-character + Notable Rolls T03). NPC pages **created** (Brula, Onyx) and **updated** (Chandra — full rewrite, Niv-Mizzet — full rewrite, Nicol Bolas, Molly, Nissa, Samut, Steve, Salena; Oketra already T03-complete from parallel pass); all 5 PC pages updated. World-lore **created** (Bolas's Citadel, Strixhaven, Bone Mine, Vitu-Ghazi, Elder Spell, Spark-Harvester Trident, Flameseekers of Truth) and **updated** (Izzet League). Creatures (Eternals) updated; Plants/Fungi **created** (Ogre's Mushrooms, Purple Bone Mushrooms). **Open flags:** (1) "Witch" vs DDB "Duskblade" weapon name; (2) the unnamed fighting ally early in the battle is likely [[Samut]] but never named in-transcript; (3) "Murphy's mom" vs Orphie's mom (cookies); (4) "Onyx" identity gated behind a missed nat-20 (campaign-level: Professor Onyx = Liliana, NOT party knowledge in T03); (5) trident (T03) vs bident/"Biden" (earlier) terminology; (6) Scrappy drop-off destination (Izzet vs Golgari) TBD. **Note:** processed in parallel with the T02 pass into shared files — content layered without overwriting. **.docx skipped (vault uses markdown notes).**
- **Transcript 02 (07/27/25) — I Can't Rebuild You — processed (Convo 2):** Session notes file written (`01-Sessions/Session Notes/Notes 2025/PP_02_072725_I_Cant_Rebuild_You.md`); POV journal entry; Dashboard timeline rows + session link; all four hub trackers (Loot, Quote Board, Profanity, House Rules); 22 DDB rolls cross-referenced (Roll_Statistics updated). NPC pages **created** (Molly, Nissa, Samut, God-Eternal Oketra, Pippi) and **filled/updated** (Steve, Dalya Bara, Clarissa, Ral Zarek, Salena, Szadek); all 5 PC pages updated; Eternals creature updated. **Open flags:** (1) Gruul T02 betrayal vs. Dashboard "Allied" status — left to maintained canon, flagged; (2) Salena/"Selena" no-show at apartment (resolved T03 at Bone Mine); (3) DDB roll attributions: Varis History nat-1 vs "four," planeswalker Insight 19 (Ogre vs Varis), Varis Perception 17 vs DDB 4; (4) "bident" transcribed as "Biden." **Note:** vault Dashboard/House Rules were already T03-aware (co-maintained in parallel); T02 work was per-page extraction layered under existing content without overwriting. **.docx skipped per Taylor.**
- **Transcript 01 (07/13/25) — Into the Ghost Mind — processed (Convo 2):** Dashboard (timeline, planeswalkers, quests, party assets), all 5 PC pages, NPC pages (Kaya, Ral, Szadek, Tomik already done by prior pass; updated Salena; created/populated Borborygmos, Hikara, Benji, Nicol Bolas, Vraska), world-lore (Ghost Mind, Fortress of Nivix, Interplanar Beacon, Immortal Sun, Eternals, House Dimir, Izzet, Golgari, Gruul, Simic), mechanics (Roll_Statistics, Spell_Usage), and all four hub trackers seeded. POV journal verified present. **Open flags:** (1) Salena/"Selena" return mechanism; (2) Borborygmos overthrown (T01) vs. active ally (T07); (3) Ogre History 15 vs DDB 17.
