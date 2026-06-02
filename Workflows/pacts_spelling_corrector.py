#!/usr/bin/env python3
"""
Pacts & Power — Transcript Spelling Corrector
===============================================
Reads raw session transcripts and applies canonical spelling corrections
based on the campaign spelling dictionary.

Usage:
    python pacts_spelling_corrector.py [--input-dir DIR] [--output-dir DIR] [--dry-run] [--file FILENAME]

Arguments:
    --input-dir   Path to raw transcripts (default: vault Raw_Unedited folder)
    --output-dir  Path for corrected output (default: vault Corrected folder)
    --dry-run     Preview corrections without writing files
    --file        Process a single file instead of the whole directory
    --report      Generate a CSV correction report alongside each file

The script applies corrections in priority order and tracks every change
for audit purposes.
"""

import re
import os
import sys
import csv
import argparse
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


# ─────────────────────────────────────────────
# CONFIGURATION — Edit these paths for your system
# ─────────────────────────────────────────────

DEFAULT_INPUT_DIR = r"C:\Users\theli\pacts_power_vault\Session_Sources\Transcripts\Raw_Unedited"
DEFAULT_OUTPUT_DIR = r"C:\Users\theli\pacts_power_vault\Session_Sources\Transcripts\Corrected"


# ─────────────────────────────────────────────
# CORRECTION DEFINITIONS
# ─────────────────────────────────────────────

@dataclass
class Correction:
    """A single spelling correction rule."""
    pattern: str            # Regex pattern to match
    replacement: str        # What to replace with
    category: str           # For reporting (e.g., "PC Names", "Guilds")
    label: str              # Human-readable label (e.g., "Santis→Sanis")
    flags: int = re.IGNORECASE  # Regex flags
    word_boundary: bool = True   # Auto-wrap in \b...\b
    context_check: Optional[str] = None  # Optional: only apply if this regex also matches nearby


def build_corrections() -> list[Correction]:
    """
    Build the full correction list in priority order.
    
    IMPORTANT: Order matters. More specific patterns come first to prevent
    partial matches from firing before full matches.
    """
    corrections = []

    # ── HELPER: shorthand for simple word-boundary replacements ──
    def add(pattern, replacement, category, label, case_sensitive=False, word_boundary=True):
        flags = 0 if case_sensitive else re.IGNORECASE
        corrections.append(Correction(
            pattern=pattern,
            replacement=replacement,
            category=category,
            label=label,
            flags=flags,
            word_boundary=word_boundary,
        ))

    # ══════════════════════════════════════════
    # MULTI-WORD PATTERNS (must come first)
    # ══════════════════════════════════════════

    # Campaign artifacts & concepts (multi-word)
    add(r"leather\s+daddy\s+bowl", "leather daddy ball", "Artifacts", "leather daddy bowl→leather daddy ball")
    add(r"Ghost\s+Mine(?!d|r|s)", "Ghost Mind", "Entities", "Ghost Mine→Ghost Mind")
    add(r"Ghost\s+Miner", "Ghost Mind", "Entities", "Ghost Miner→Ghost Mind")
    add(r"ghost\s+mine(?!d|r|s)", "Ghost Mind", "Entities", "ghost mine→Ghost Mind")
    add(r"Soul\s+Integrated\s+Storage", "Sole Integrated Storage", "Artifacts", "Soul Integrated Storage→Sole Integrated Storage")
    add(r"Blaze\s+Bringer", "Blazebringer", "Artifacts", "Blaze Bringer→Blazebringer")
    add(r"Hell\s+Smasher", "HellSmasher", "Artifacts", "Hell Smasher→HellSmasher")
    add(r"Hell's\s+Masher", "HellSmasher", "Artifacts", "Hell's Masher→HellSmasher")
    add(r"Dol\s+Ara(?!h)", "Dol Arrah", "Characters", "Dol Ara→Dol Arrah")
    add(r"Dol\s+Arah", "Dol Arrah", "Characters", "Dol Arah→Dol Arrah")
    add(r"Guild\s+Pact", "Guildpact", "Terms", "Guild Pact→Guildpact")
    add(r"Living\s+Guild\s+Pact", "Living Guildpact", "Terms", "Living Guild Pact→Living Guildpact")
    add(r"Gates\s+Watch", "Gatewatch", "Organizations", "Gates Watch→Gatewatch")
    add(r"Gate\s+Watch", "Gatewatch", "Organizations", "Gate Watch→Gatewatch")
    add(r"Plane\s+Walker", "Planeswalker", "Terms", "Plane Walker→Planeswalker")
    add(r"Plains\s+Walker", "Planeswalker", "Terms", "Plains Walker→Planeswalker")
    add(r"Planes\s+Walker", "Planeswalker", "Terms", "Planes Walker→Planeswalker")
    add(r"Immortal\s+Son", "Immortal Sun", "Artifacts", "Immortal Son→Immortal Sun")
    add(r"Eternal\s+Son", "Immortal Sun", "Artifacts", "Eternal Son→Immortal Sun")
    add(r"Eternal\s+Sun", "Immortal Sun", "Artifacts", "Eternal Sun→Immortal Sun")
    add(r"Second\s+Son", "Second Sun", "Factions", "Second Son→Second Sun")
    add(r"Sun\s+Home", "Sunhome", "Locations", "Sun Home→Sunhome")
    add(r"Under\s+City", "Undercity", "Locations", "Under City→Undercity")
    add(r"Way\s+Port", "Wayport", "Locations", "Way Port→Wayport")
    add(r"Strix\s+Haven", "Strixhaven", "Planes", "Strix Haven→Strixhaven")
    add(r"Dead\s+Bridge\s+Chasm", "Deadbridge Chasm", "Locations", "Dead Bridge Chasm→Deadbridge Chasm")
    add(r"Blister\s+Coils", "Blistercoils", "Locations", "Blister Coils→Blistercoils")
    add(r"Krawl\s+Hive", "Kraul Hive", "Locations", "Krawl Hive→Kraul Hive")
    add(r"Lay\s+Line", "Leyline", "Terms", "Lay Line→Leyline")
    add(r"Shock\s+land", "Shockland", "Terms", "Shock land→Shockland")
    add(r"Guild\s+gate", "Guildgate", "Terms", "Guild gate→Guildgate")

    # Multi-word character names (before single-word patterns)
    add(r"Barbara\s+Rigmos", "Borborygmos", "Characters", "Barbara Rigmos→Borborygmos")
    add(r"Raul\s+Zarek", "Ral Zarek", "Characters", "Raul Zarek→Ral Zarek")
    add(r"Rall\s+Zarek", "Ral Zarek", "Characters", "Rall Zarek→Ral Zarek")
    add(r"Jace\s+Beleran", "Jace Beleren", "Characters", "Jace Beleran→Jace Beleren")
    add(r"Jace\s+Belarin", "Jace Beleren", "Characters", "Jace Belarin→Jace Beleren")
    add(r"Chandra\s+Nalar", "Chandra Nalaar", "Characters", "Chandra Nalar→Chandra Nalaar")
    add(r"Dovin\s+Ban(?!e)", "Dovin Baan", "Characters", "Dovin Ban→Dovin Baan")
    add(r"Doven\s+Baan", "Dovin Baan", "Characters", "Doven Baan→Dovin Baan")
    add(r"Domri\s+Raid", "Domri Rade", "Characters", "Domri Raid→Domri Rade")
    add(r"Domry\s+Rade", "Domri Rade", "Characters", "Domry Rade→Domri Rade")
    add(r"Ajani\s+Goldmain", "Ajani Goldmane", "Characters", "Ajani Goldmain→Ajani Goldmane")
    add(r"Teresa\s+Karlov", "Teysa Karlov", "Characters", "Teresa Karlov→Teysa Karlov")
    add(r"Niv\s+Mizzet", "Niv-Mizzet", "Characters", "Niv Mizzet→Niv-Mizzet")
    add(r"Niv\s+Mizet", "Niv-Mizzet", "Characters", "Niv Mizet→Niv-Mizzet")
    add(r"Nico\s+Bolus", "Nicol Bolas", "Characters", "Nico Bolus→Nicol Bolas")
    add(r"New\s+Prav(?!h)", "New Prahv", "Locations", "New Prav→New Prahv")
    add(r"Vito\s+Ghazi", "Vitu-Ghazi", "Locations", "Vito Ghazi→Vitu-Ghazi")
    add(r"Vitu\s+Ghazee", "Vitu-Ghazi", "Locations", "Vitu Ghazee→Vitu-Ghazi")
    add(r"Zannis\s+Ugin", "Sanis, Ugin's", "Characters", "Zannis Ugin→Sanis, Ugin's")
    add(r"Izzy\s+Guild", "Izzet Guild", "Guilds", "Izzy Guild→Izzet Guild")
    add(r"IS\s+A\s+Guild", "Izzet Guild", "Guilds", "IS A Guild→Izzet Guild", case_sensitive=True)
    add(r"Gru\s+Guild", "Gruul Guild", "Guilds", "Gru Guild→Gruul Guild")
    add(r"Amara\s+Tangers", "Emmara Tandris", "NPCs", "Amara Tangers→Emmara Tandris")
    add(r"Railana\s+Estate", "Reylana Mansion", "Locations", "Railana Estate→Reylana Mansion")

    # Guild full-name corrections
    add(r"Celestian\s+Conclave", "Selesnya Conclave", "Guilds", "Celestian Conclave→Selesnya Conclave")
    add(r"Celestia\s+Conclave", "Selesnya Conclave", "Guilds", "Celestia Conclave→Selesnya Conclave")
    add(r"Sledging\s+Conclave", "Selesnya Conclave", "Guilds", "Sledging Conclave→Selesnya Conclave")
    add(r"Solicited\s+Conclave", "Selesnya Conclave", "Guilds", "Solicited Conclave→Selesnya Conclave")

    # ══════════════════════════════════════════
    # SINGLE-WORD PATTERNS
    # ══════════════════════════════════════════

    # PC Names
    add(r"Orphiea", "Orphea", "PC Names", "Orphiea→Orphea")
    add(r"Orphieus", "Orphea", "PC Names", "Orphieus→Orphea")
    add(r"Santis", "Sanis", "PC Names", "Santis→Sanis")
    add(r"Santus", "Sanis", "PC Names", "Santus→Sanis")
    add(r"Varus", "Varis", "PC Names", "Varus→Varis")

    # Planeswalkers & Major NPCs
    add(r"Nicobolus", "Nicol Bolas", "Characters", "Nicobolus→Nicol Bolas")
    add(r"Kaeya", "Kaya", "Characters", "Kaeya→Kaya")
    add(r"Kayakasir", "Kaya Cassir", "Characters", "Kayakasir→Kaya Cassir")
    add(r"Hugin(?!'s)", "Ugin", "Characters", "Hugin→Ugin")
    # Handle Hugin's → Ugin's separately
    add(r"Hugin's", "Ugin's", "Characters", "Hugin's→Ugin's")
    add(r"Borberigmos", "Borborygmos", "Characters", "Borberigmos→Borborygmos")
    add(r"Barbarigmos", "Borborygmos", "Characters", "Barbarigmos→Borborygmos")
    add(r"Taysa", "Teysa", "Characters", "Taysa→Teysa")
    add(r"Isperea", "Isperia", "Characters", "Isperea→Isperia")
    add(r"Esperia", "Isperia", "Characters", "Esperia→Isperia")
    add(r"Lazoff", "Lazav", "Characters", "Lazoff→Lazav")
    add(r"Lazov", "Lazav", "Characters", "Lazov→Lazav")
    add(r"Aurellia", "Aurelia", "Characters", "Aurellia→Aurelia")
    add(r"Narsett", "Narset", "Characters", "Narsett→Narset")
    add(r"Lilliana", "Liliana", "Characters", "Lilliana→Liliana")
    add(r"Tesserik", "Tezzeret", "Characters", "Tesserik→Tezzeret")
    add(r"Tezzerin", "Tezzeret", "Characters", "Tezzerin→Tezzeret")
    add(r"Tesserit", "Tezzeret", "Characters", "Tesserit→Tezzeret")

    # God-Eternals of Amonkhet (Bolas's army) — added after the finale (PP_20/21)
    # IMPORTANT: never map "Mardu"→Bontu; "Mardu" is a canonical Tarkir clan (Mardu Horde).
    add(r"Bantu", "Bontu", "Characters", "Bantu→Bontu")
    add(r"Bantou", "Bontu", "Characters", "Bantou→Bontu")
    add(r"Ronas", "Rhonas", "Characters", "Ronas→Rhonas")
    add(r"Khephnet", "Kefnet", "Characters", "Khephnet→Kefnet")
    add(r"Kevnit", "Kefnet", "Characters", "Kevnit→Kefnet")
    add(r"Kevnet", "Kefnet", "Characters", "Kevnet→Kefnet")
    add(r"Kefnut", "Kefnet", "Characters", "Kefnut→Kefnet")

    # Finale deities (campaign-original) — preserve intentional Ogre nicknames (Urogalan/Roguelin/Ogrelin/Oglin)
    add(r"Orogalan", "Ur-Ogre-lan", "Characters", "Orogalan→Ur-Ogre-lan")
    add(r"Ogorgalon", "Ur-Ogre-lan", "Characters", "Ogorgalon→Ur-Ogre-lan")
    add(r"Arogalin", "Ur-Ogre-lan", "Characters", "Arogalin→Ur-Ogre-lan")
    add(r"Arugalon", "Ur-Ogre-lan", "Characters", "Arugalon→Ur-Ogre-lan")
    add(r"Orogalon", "Ur-Ogre-lan", "Characters", "Orogalon→Ur-Ogre-lan")
    add(r"Rogalan", "Ur-Ogre-lan", "Characters", "Rogalan→Ur-Ogre-lan")
    # Aphonexa (goddess of rebirth) is canonical — correct the "Aphanexa" drift TO it
    add(r"Aphanexa", "Aphonexa", "Characters", "Aphanexa→Aphonexa")
    add(r"Aphenexa", "Aphonexa", "Characters", "Aphenexa→Aphonexa")
    add(r"Aphonexet", "Aphonexa", "Characters", "Aphonexet→Aphonexa")
    add(r"Aphanexus", "Aphonexa", "Characters", "Aphanexus→Aphonexa")
    add(r"Hellsmasher", "HellSmasher", "Artifacts", "Hellsmasher→HellSmasher")
    # Dol Arrah (Rin's deity; Eberron Sovereign Host) — long mis-transcribed "Dolora/Dolorah"
    add(r"Dolorah", "Dol Arrah", "Characters", "Dolorah→Dol Arrah")
    add(r"Dolora", "Dol Arrah", "Characters", "Dolora→Dol Arrah")
    add(r"Dolara", "Dol Arrah", "Characters", "Dolara→Dol Arrah")

    # Szadek variants (but NOT "Zaddy Daddy" — that's intentional)
    add(r"Zodix", "Szadek", "Characters", "Zodix→Szadek")
    add(r"Zadak", "Szadek", "Characters", "Zadak→Szadek")
    add(r"Zadix", "Szadek", "Characters", "Zadix→Szadek")
    add(r"Zadac", "Szadek", "Characters", "Zadac→Szadek")
    add(r"Zadig", "Szadek", "Characters", "Zadig→Szadek")
    add(r"Szadeko", "Szadek", "Characters", "Szadeko→Szadek")

    # Guilds (single-word errors)
    add(r"Azorious", "Azorius", "Guilds", "Azorious→Azorius")
    add(r"Selensya", "Selesnya", "Guilds", "Selensya→Selesnya")
    add(r"Selenya", "Selesnya", "Guilds", "Selenya→Selesnya")
    add(r"Orzov", "Orzhov", "Guilds", "Orzov→Orzhov")
    add(r"Orshov", "Orzhov", "Guilds", "Orshov→Orzhov")
    add(r"Golgory", "Golgari", "Guilds", "Golgory→Golgari")
    add(r"Golgori", "Golgari", "Guilds", "Golgori→Golgari")
    add(r"Borros", "Boros", "Guilds", "Borros→Boros")
    add(r"Simik", "Simic", "Guilds", "Simik→Simic")
    add(r"Simick", "Simic", "Guilds", "Simick→Simic")

    # Locations
    add(r"Ravnika", "Ravnica", "Locations", "Ravnika→Ravnica")
    add(r"Dravnica", "Ravnica", "Locations", "Dravnica→Ravnica")
    add(r"Ravinica", "Ravnica", "Locations", "Ravinica→Ravnica")
    add(r"Orzova", "Orzhova", "Locations", "Orzova→Orzhova")
    add(r"Niviks", "Nivix", "Locations", "Niviks→Nivix")
    add(r"Nybecks", "Nivix", "Locations", "Nybecks→Nivix")
    add(r"Ibidugazi", "Vitu-Ghazi", "Locations", "Ibidugazi→Vitu-Ghazi")
    add(r"Skarg", "Skaarg", "Locations", "Skarg→Skaarg")

    # Planes
    add(r"Exelon", "Ixalan", "Planes", "Exelon→Ixalan")
    add(r"Ixelan", "Ixalan", "Planes", "Ixelan→Ixalan")
    add(r"Exalan", "Ixalan", "Planes", "Exalan→Ixalan")
    add(r"Amikette", "Amonkhet", "Planes", "Amikette→Amonkhet")
    add(r"Amuket", "Amonkhet", "Planes", "Amuket→Amonkhet")
    add(r"Arcavius", "Arcavios", "Planes", "Arcavius→Arcavios")
    add(r"Dominiaria", "Dominaria", "Planes", "Dominiaria→Dominaria")
    add(r"Talbata", "Tolbata", "Planes", "Talbata→Tolbata")

    # Terms
    add(r"Layline", "Leyline", "Terms", "Layline→Leyline")
    add(r"Paroon", "Parun", "Terms", "Paroon→Parun")
    add(r"Ecuminopolis", "Ecumenopolis", "Terms", "Ecuminopolis→Ecumenopolis")
    add(r"Pippy", "Pippi", "Artifacts", "Pippy→Pippi")
    add(r"Scrapy", "Scrappy", "Artifacts", "Scrapy→Scrappy")
    add(r"Scrappi", "Scrappy", "Artifacts", "Scrappi→Scrappy")
    add(r"Clarisa", "Clarissa", "NPCs", "Clarisa→Clarissa")
    add(r"Crenko", "Krenko", "NPCs", "Crenko→Krenko")

    # NPC misspellings
    add(r"Hecara", "Hekara", "NPCs", "Hecara→Hekara")
    add(r"Hekera", "Hekara", "NPCs", "Hekera→Hekara")
    add(r"Lavina", "Lavinia", "NPCs", "Lavina→Lavinia")

    return corrections


# ── CONTEXT-SENSITIVE CORRECTIONS ──
# These require special handling because the error word appears in normal English.

def apply_context_corrections(text: str, log: list) -> str:
    """
    Handle corrections that can't be done with simple word-boundary regex
    because the error term is a common English word or substring.
    """

    # Ren → Rin (only when standalone name, not inside aren't, children, etc.)
    # Match: start of line or after whitespace/punctuation, then "Ren", then comma/period/space/end
    def ren_replace(m):
        log.append(("PC Names", "Ren→Rin", m.group(0), m.start()))
        return m.group(1) + "Rin" + m.group(3)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Ren)([\s,.:;!?"\'\)\]]|$)', ren_replace, text, flags=re.MULTILINE)

    # Wren → Rin (when clearly a name)
    def wren_replace(m):
        log.append(("PC Names", "Wren→Rin", m.group(0), m.start()))
        return m.group(1) + "Rin" + m.group(3)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Wren)([\s,.:;!?"\'\)\]]|$)', wren_replace, text, flags=re.MULTILINE)

    # Ryn → Rin
    def ryn_replace(m):
        log.append(("PC Names", "Ryn→Rin", m.group(0), m.start()))
        return m.group(1) + "Rin" + m.group(3)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Ryn)([\s,.:;!?"\'\)\]]|$)', ryn_replace, text, flags=re.MULTILINE)

    # Selina → Selena (standalone)
    def selina_replace(m):
        log.append(("PC Names", "Selina→Selena", m.group(0), m.start()))
        return m.group(1) + "Selena" + m.group(3)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Selina)([\s,.:;!?"\'\)\]]|$)', selina_replace, text, flags=re.MULTILINE)

    # Raul → Ral (standalone, when not part of "Raul Zarek" which is handled above)
    # Only match standalone "Raul" that wasn't already caught by "Raul Zarek"
    def raul_replace(m):
        # Check if next word is "Zarek" — if so, skip (already handled)
        after = text[m.end():m.end()+10]
        if after.strip().startswith("Zarek"):
            return m.group(0)
        log.append(("Characters", "Raul→Ral", m.group(0), m.start()))
        return m.group(1) + "Ral" + m.group(3)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Raul)([\s,.:;!?"\'\)\]]|$)', raul_replace, text, flags=re.MULTILINE)

    # Raw → Ral (only when clearly a name — preceded by name-like context)
    # Match patterns like "Raw goes", "Raw,", "to Raw", line-starting "Raw "
    def raw_replace(m):
        log.append(("Characters", "Raw→Ral", m.group(0), m.start()))
        return m.group(1) + "Ral" + m.group(3)
    # Only replace when preceded by patterns that suggest it's a name:
    # After a comma/period + space, or at line start, followed by verb-like words or punctuation
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Raw)([\s,.:;!?"\'\)\]])', raw_replace, text, flags=re.MULTILINE)

    # Nicolas → Nicol Bolas (only when clearly referring to the villain, not a person named Nicolas)
    def nicolas_replace(m):
        # Check surrounding context for Bolas-related words
        start = max(0, m.start() - 50)
        end = min(len(text), m.end() + 50)
        context = text[start:end].lower()
        if any(w in context for w in ["bolas", "dragon", "villain", "evil", "planeswalker", "nicol"]):
            log.append(("Characters", "Nicolas→Nicol Bolas", m.group(0), m.start()))
            return m.group(1) + "Nicol Bolas" + m.group(3)
        return m.group(0)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Nicolas)([\s,.:;!?"\'\)\]]|$)', nicolas_replace, text, flags=re.MULTILINE)

    # Raska → Vraska (standalone)
    def raska_replace(m):
        log.append(("Characters", "Raska→Vraska", m.group(0), m.start()))
        return m.group(1) + "Vraska" + m.group(3)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Raska)([\s,.:;!?"\'\)\]]|$)', raska_replace, text, flags=re.MULTILINE)

    # Demir → Dimir (standalone, not inside "Demure")
    def demir_replace(m):
        log.append(("Guilds", "Demir→Dimir", m.group(0), m.start()))
        return m.group(1) + "Dimir" + m.group(3)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Demir)([\s,.:;!?"\'\)\]]|$)', demir_replace, text, flags=re.MULTILINE)

    # Demure → Dimir (when referring to the guild)
    def demure_replace(m):
        context_start = max(0, m.start() - 40)
        context_end = min(len(text), m.end() + 40)
        context = text[context_start:context_end].lower()
        if any(w in context for w in ["guild", "agent", "spy", "dimir", "espionage"]):
            log.append(("Guilds", "Demure→Dimir", m.group(0), m.start()))
            return m.group(1) + "Dimir" + m.group(3)
        return m.group(0)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Demure)([\s,.:;!?"\'\)\]]|$)', demure_replace, text, flags=re.MULTILINE)

    # Boris → Boros (only when referring to the guild)
    def boris_replace(m):
        context_start = max(0, m.start() - 40)
        context_end = min(len(text), m.end() + 40)
        context = text[context_start:context_end].lower()
        if any(w in context for w in ["guild", "legion", "headquarters", "district", "hq", "academy", "soldier"]):
            log.append(("Guilds", "Boris→Boros", m.group(0), m.start()))
            return m.group(1) + "Boros" + m.group(3)
        return m.group(0)
    text = re.sub(r'(^|[\s,.:;!?"\'\(\)])(Boris)([\s,.:;!?"\'\)\]]|$)', boris_replace, text, flags=re.MULTILINE)

    return text


# ─────────────────────────────────────────────
# MAIN PROCESSING
# ─────────────────────────────────────────────

def process_transcript(text: str, filename: str) -> tuple[str, list[tuple]]:
    """
    Apply all corrections to a transcript.
    Returns (corrected_text, correction_log).
    Log entries: (category, label, original_match, position)
    """
    corrections = build_corrections()
    log = []

    # Phase 1: Standard regex corrections
    for c in corrections:
        if c.word_boundary:
            pattern = rf'\b{c.pattern}\b'
        else:
            pattern = c.pattern

        def make_replacer(corr):
            def replacer(m):
                log.append((corr.category, corr.label, m.group(0), m.start()))
                # Preserve original case pattern for single-word replacements
                return corr.replacement
            return replacer

        text = re.sub(pattern, make_replacer(c), text, flags=c.flags)

    # Phase 2: Context-sensitive corrections
    text = apply_context_corrections(text, log)

    return text, log


def generate_header(filename: str, correction_count: int, categories: dict) -> str:
    """Generate the correction disclosure header."""
    date = datetime.now().strftime("%Y-%m-%d")
    
    cat_summary = ", ".join(f"{cat}: {count}" for cat, count in sorted(categories.items()))
    
    header = f"""---
source: {filename} (Raw)
corrected: true
correction_date: {date}
corrections_applied: {correction_count}
---

# {filename.replace('.md', '')} (Corrected)

> Spelling normalized per campaign spelling dictionary.
> Verbatim transcript text preserved except for proper noun corrections.
> Total corrections: {correction_count} ({cat_summary})

---

"""
    return header


def write_report(log: list, output_path: str):
    """Write a CSV correction report."""
    report_path = output_path.replace(".md", "_corrections.csv")
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Correction", "Original Text", "Position"])
        for category, label, original, pos in log:
            writer.writerow([category, label, original, pos])
    return report_path


def process_file(input_path: str, output_dir: str, dry_run: bool = False, write_csv: bool = False):
    """Process a single transcript file."""
    filename = os.path.basename(input_path)
    print(f"\n{'='*60}")
    print(f"Processing: {filename}")
    print(f"{'='*60}")

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    corrected, log = process_transcript(text, filename)

    # Count by category
    categories = {}
    for cat, label, orig, pos in log:
        categories[cat] = categories.get(cat, 0) + 1

    total = len(log)
    print(f"\nCorrections found: {total}")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    if total > 0:
        # Show sample corrections
        print(f"\nSample corrections (first 15):")
        for cat, label, orig, pos in log[:15]:
            print(f"  [{cat}] {label}")

    if dry_run:
        print(f"\n[DRY RUN] No files written.")
        return total

    # Write corrected file
    output_filename = filename.replace(".md", "-Corrected.md")
    output_path = os.path.join(output_dir, output_filename)

    header = generate_header(filename, total, categories)
    
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + corrected)

    print(f"\n✅ Written: {output_path}")

    # Optional CSV report
    if write_csv and total > 0:
        report_path = write_report(log, output_path)
        print(f"📊 Report: {report_path}")

    return total


def main():
    parser = argparse.ArgumentParser(
        description="Pacts & Power Transcript Spelling Corrector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pacts_spelling_corrector.py --dry-run
  python pacts_spelling_corrector.py --file 02-072725-Pacts.md
  python pacts_spelling_corrector.py --report
  python pacts_spelling_corrector.py --input-dir ./raw --output-dir ./corrected
        """
    )
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR, help="Path to raw transcripts")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Path for corrected output")
    parser.add_argument("--dry-run", action="store_true", help="Preview corrections without writing")
    parser.add_argument("--file", help="Process a single file")
    parser.add_argument("--report", action="store_true", help="Generate CSV correction reports")

    args = parser.parse_args()

    print("╔══════════════════════════════════════════════╗")
    print("║  Pacts & Power — Transcript Spelling Fixer   ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"\nInput:  {args.input_dir}")
    print(f"Output: {args.output_dir}")
    if args.dry_run:
        print("Mode:   DRY RUN (no files will be written)")

    grand_total = 0

    if args.file:
        # Single file mode
        input_path = os.path.join(args.input_dir, args.file)
        if not os.path.exists(input_path):
            print(f"\n❌ File not found: {input_path}")
            sys.exit(1)
        grand_total = process_file(input_path, args.output_dir, args.dry_run, args.report)
    else:
        # Batch mode — process all .md files
        files = sorted([f for f in os.listdir(args.input_dir) if f.endswith(".md")])
        if not files:
            print(f"\n❌ No .md files found in {args.input_dir}")
            sys.exit(1)

        print(f"\nFound {len(files)} transcript(s) to process.")

        for filename in files:
            input_path = os.path.join(args.input_dir, filename)
            count = process_file(input_path, args.output_dir, args.dry_run, args.report)
            grand_total += count

    print(f"\n{'='*60}")
    print(f"DONE. Total corrections across all files: {grand_total}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
