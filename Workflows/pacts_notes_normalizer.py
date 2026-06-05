#!/usr/bin/env python3
"""
pacts_notes_normalizer.py
-------------------------
Normalizes condensed Pacts & Power session notes (the `**Bold Label.**` format
used from Session 04 onward) into the full v8 template structure
(`## Section N — Title` + `### Subheading`), so they parse uniformly for the
Rectrix Caedere session page.

WHAT IT DOES (structure only — never invents or deletes content):
  * `## 5. Artifacts (Loot & Items)`            -> `## Section 5 — Artifacts (Loot & Items)`
  * `**Narrative Summary.** text...`            -> `### Narrative Summary` + paragraph
  * Only a WHITELIST of known v8 section labels is promoted to `###`.
    Lettered narrative beats (`**A. The battle...**`) and other inline bold
    are left exactly as-is, so narratives stay intact.

SAFETY:
  * Idempotent — re-running does nothing once a file is normalized.
  * Skips already-full-template files (Sessions 01-03) automatically.
  * --dry-run shows the plan and a table-row integrity check before writing.

USAGE:
  python pacts_notes_normalizer.py --dry-run
  python pacts_notes_normalizer.py                 # normalize all condensed notes in place
  python pacts_notes_normalizer.py --file "01-Sessions/Session Notes/Notes 2026/PP_13_012526_Fucking_Barbarians.md"

Run from the vault root (C:\\Users\\theli\\pacts_power_vault). Requires Python 3.
After it runs, let the Git plugin commit/push (or commit manually).
"""
import re, sys, argparse, glob, os

# --- whitelist: (test on cleaned-lowercased label) -> canonical v8 subheading ---
WHITELIST = [
    (lambda s: s.startswith('narrative summary'),            'Narrative Summary'),
    (lambda s: s.startswith('session setting'),              'Session Setting'),
    (lambda s: s.startswith('locations'),                    'Locations Visited'),
    (lambda s: s.startswith('quests'),                       'Quests / Objectives'),
    (lambda s: 'scene' in s and 'timeline' in s,             'Scene / Timeline Breakdown'),
    (lambda s: s.startswith('themes'),                       'Themes & Emotional Beats'),
    (lambda s: s.startswith('party structure'),              'Party Structure & Subgroups'),
    (lambda s: s.startswith('npcs') or s == 'npc',           'NPCs'),
    (lambda s: s.startswith('reputation'),                   'Reputation & Relationships'),
    (lambda s: s.startswith('encounter summary'),            'Encounter Summary'),
    (lambda s: s.startswith('encounter'),                    'Encounters'),
    (lambda s: s.startswith('initiative'),                   'Initiative'),
    (lambda s: s.startswith('full roll log') or s.startswith('roll log'), 'Full Roll Log'),
    (lambda s: s.startswith('quote board'),                  'Quote Board'),
    (lambda s: s.startswith('profanity'),                    'Profanity Record'),
    (lambda s: s.startswith('alternate'),                    'Alternate Names in Play'),
    (lambda s: s.startswith('loot') or s.startswith('artifacts'), 'Loot & Items'),
    (lambda s: s.startswith('patterns'),                     'Patterns, Progress & Future Implications'),
    (lambda s: s.startswith('continuity'),                   'Continuity Flags, Missing Info & Ambiguities'),
]

def match_label(label):
    s = label.strip().rstrip('.:').strip().lower()
    for test, canon in WHITELIST:
        if test(s):
            lead = None
            if canon == 'Encounters':
                d = re.sub(r'^encounter\s*[\u2014\-:]\s*', '', label.strip().rstrip('.:'), flags=re.I)
                if d and d.lower() != 'encounters':
                    lead = d
            return canon, lead
    return None, None

def is_condensed(md):
    """A note needs normalizing if it still has `## N.` section headers."""
    return re.search(r'^##\s+\d+\.\s', md, re.M) is not None

def normalize(md):
    out, promoted = [], 0
    for line in md.split('\n'):
        m = re.match(r'^##\s+(\d+)\.\s*(.+)$', line)
        if m:
            title = m.group(2).strip()
            if title.lower().startswith('orphie') and 'pov' in title.lower():
                title = "Orphie's POV Overview"
            out.append(f"## Section {m.group(1)} — {title}")
            continue
        m = re.match(r'^\*\*([^*]{1,70}?)\*\*[ \t]*(.*)$', line)
        if m:
            canon, lead = match_label(m.group(1))
            if canon:
                rest = m.group(2).strip()
                out.append(f"### {canon}")
                out.append("")
                if lead:
                    out.append(f"**{lead}**")
                if rest:
                    out.append(rest)
                promoted += 1
                continue
        out.append(line)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)), promoted

def process(path, dry):
    original = open(path, encoding='utf-8').read()
    if not is_condensed(original):
        print(f"  SKIP  {os.path.basename(path)}  (already full-template)")
        return
    new, promoted = normalize(original)
    tbl_o, tbl_n = original.count('\n|'), new.count('\n|')
    integrity = "OK" if tbl_o == tbl_n else f"!! TABLE MISMATCH {tbl_o}->{tbl_n}"
    action = "DRY-RUN" if dry else "WROTE  "
    if not dry:
        open(path, 'w', encoding='utf-8').write(new)
    print(f"  {action} {os.path.basename(path)}  | {promoted} headings promoted | tables {tbl_o}->{tbl_n} [{integrity}]")

def main():
    ap = argparse.ArgumentParser(description="Normalize condensed Pacts & Power notes to v8 structure.")
    ap.add_argument('--dry-run', action='store_true', help="Preview without writing.")
    ap.add_argument('--file', help="Normalize a single file (path relative to vault root).")
    args = ap.parse_args()
    if args.file:
        files = [args.file]
    else:
        files = glob.glob('01-Sessions/Session Notes/Notes */PP_*.md')
    files = sorted(files)
    if not files:
        print("No session notes found. Run from the vault root.")
        sys.exit(1)
    print(f"{'DRY-RUN — no files will change' if args.dry_run else 'NORMALIZING'} ({len(files)} candidate files)\n")
    for f in files:
        process(f, args.dry_run)
    print("\nDone." + ("" if args.dry_run else " Let the Git plugin commit/push, or commit manually."))

if __name__ == '__main__':
    main()
