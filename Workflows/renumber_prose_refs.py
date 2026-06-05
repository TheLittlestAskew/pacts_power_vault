"""One-time (2026-06-05): shift date-anchored prose session refs in derived vault pages.

Only rewrites 'PP NN (MM/DD/YY)' style references where the adjacent date confirms
which session is meant — bare refs without dates are left for manual triage.
"""
import os
import re

VAULT = r"C:\Users\theli\pacts_power_vault"
ROOTS = ["00-Campaign-Hub", "03-Characters", "04-World-Lore", "05-Mechanics",
         "07-Flora_Fauna", "02-Character_Journal"]

# old_num -> (new_num, MM/DD/YY)
SESSIONS = {
    10: (9, "11/30/25"),
    11: (10, "12/14/25"),
    12: (11, "01/11/26"),
    13: (12, "01/25/26"),
    14: (13, "02/13/26"),
    15: (14, "02/22/26"),
    16: (15, "03/13/26"),
    17: (16, "04/02/26"),
    18: (17, "04/05/26"),
    19: (18, "04/19/26"),
    20: (19, "05/14/26"),
    21: (20, "05/31/26"),
}

rules = []
for old in sorted(SESSIONS):  # ascending so cascades are safe
    new, date = SESSIONS[old]
    d = re.escape(date)
    # also tolerate MM/DD (no year) immediately after
    short_d = re.escape(date[:5])
    for label in [r"PP[ _]", r"Session ", r"S", r"T", r"Transcript "]:
        pat = re.compile(
            r"(?<![|\[\w])(" + label + r")0?" + str(old) +
            r"((?:\]\])?[ ,:]*\(?(?:" + d + r"|" + short_d + r")\b)"
        )
        rules.append((pat, lambda m, n=new: m.group(1) + f"{n:02d}" + m.group(2)))

changed = {}
for root_name in ROOTS:
    rp = os.path.join(VAULT, root_name)
    for dp, dn, fns in os.walk(rp):
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            with open(p, "r", encoding="utf-8") as f:
                text = f.read()
            orig = text
            total = 0
            for pat, repl in rules:
                text, k = pat.subn(repl, text)
                total += k
            if text != orig:
                with open(p, "w", encoding="utf-8", newline="") as f:
                    f.write(text)
                changed[os.path.relpath(p, VAULT)] = total

print(f"Changed {len(changed)} files, {sum(changed.values())} date-anchored refs")
for k, v in sorted(changed.items()):
    print(f"  {v:3d}  {k}")
