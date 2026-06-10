# DDB Roll Sync — Usage Guide

A Chrome extension that pulls your D&D Beyond dice roll history and upserts it into
the Pacts & Power Supabase roll archive (`ddb_rolls`). It replaces the old
browser-console script (`ddb_sync_supabase.js`) with a one-click popup.

It does two things:

1. **`background.js`** quietly grabs the Bearer token D&D Beyond uses for its
   game-log API, every time your browser hits that service. You never paste a token.
2. **`popup.js`** uses that token to page through each campaign's game log, keeps only
   dice rolls, and upserts them to Supabase.

---

## One-time install

The extension is unpacked (not from the Chrome Web Store), so you load it from disk.

1. Open Chrome and go to `chrome://extensions`.
2. Turn on **Developer mode** (top-right toggle).
3. Click **Load unpacked**.
4. Select the folder:
   `C:\Users\theli\pacts_power_vault\Workflows\ddb-roll-sync`
5. The "DDB Roll Sync" 🎲 icon appears in the toolbar. Pin it (puzzle-piece menu → pin)
   so it's one click away.

You only do this once. After that the extension stays loaded across browser restarts.

> If you ever edit the extension files, return to `chrome://extensions` and click the
> **reload** ↻ icon on the DDB Roll Sync card to pick up the changes.

---

## Every-time sync (the actual workflow)

Do this after a session, once D&D Beyond has the rolls. (Sanis and Rin roll outside
DDB, so their rolls won't be here — that's expected, not a bug.)

### 1. Capture a fresh token

The token is short-lived, so refresh it right before syncing:

1. Log into **dndbeyond.com**.
2. Open any campaign or character sheet and **scroll the dice / game-log panel** so the
   roll history loads. That network request is what hands the extension a valid token.
3. Click the 🎲 **DDB Roll Sync** toolbar icon.
4. The status bar should read **✅ Token captured (Nm ago) — ready to sync** and the
   **Sync All Campaigns** button becomes active.

If it still says **⏳ No token yet**, the browser hasn't made a game-log request.
Scroll the dice log again (or open a different character) and reopen the popup.

### 2. Sync

1. Click **⚡ Sync All Campaigns**.
2. Watch the log panel. For each active campaign it shows pages fetched, new rolls
   found, and an upsert count (`+N`). Paused campaigns are skipped.
3. Wait for **🏁 Sync complete!**

That's it. The sync is incremental: it reads the newest `timestamp_unix` already in
Supabase for each campaign and only fetches rolls newer than that, so re-running is
safe and fast. Re-seeing an already-synced roll merges instead of duplicating.

---

## What gets synced

Campaigns are hard-coded in `popup.js`:

| Campaign | Supabase `campaign_id` | DDB `gameId` | Status |
|---|---|---|---|
| Sky Is The Limit | 1 | 6907990 | active |
| **Pacts & Power** | **2** | **3661522** | active |
| Ashfall Brittania | 3 | 7170962 | active |
| Where the Flowers Remember | 4 | — | paused (no gameId) |

Pacts & Power is `campaign_id = 2`. Each synced roll row carries: character, action,
roll type/kind, dice notation (rebuilt as e.g. `2d20+10`), modifier, total, and the
individual die values.

---

## Verifying a sync (optional)

After syncing, you can confirm the data landed via the Supabase MCP. The latest
timestamp for this campaign:

```sql
SELECT MAX(timestamp_iso) FROM ddb_rolls WHERE campaign_id = 2;
```

Pull a specific session's rolls (note the required Eastern-time cast):

```sql
SELECT * FROM ddb_rolls
WHERE campaign_id = (SELECT id FROM ddb_campaigns WHERE game_id = 3661522)
AND DATE(timestamp_iso AT TIME ZONE 'America/New_York') = 'YYYY-MM-DD';
```

If a session looks short, sync again before assuming rolls are missing — DDB's log can
lag the table by a few hours, and physical / off-DDB dice never appear here at all.

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| **⏳ No token yet** | No game-log request has happened. Open a DDB character and scroll the dice log, then reopen the popup. |
| Token shows but **DDB API error: 403** | Token expired or it's the wrong (website SSO) token. Re-scroll the dice log to re-capture a fresh game-log token, then sync again. |
| **Supabase ... 401 / 403** | The anon key in `popup.js` was rotated. Update `SUPABASE_KEY`. |
| Campaign says **no gameId** | That campaign has `gameId: 0` (e.g. *Where the Flowers Remember*). Add its real DDB game ID in `popup.js` and set status to `active`. |
| Counts look low for Sanis / Rin | Expected — they roll outside D&D Beyond. Their rolls come from the transcript. |
| Edited the code, nothing changed | Reload the extension on `chrome://extensions`. |

---

## How the token capture works (background)

The main dndbeyond.com site issues a website/SSO token (`aud=dndbeyond.com`) that the
game-log API gateway **rejects** with a 403. The game-log service uses a different,
service-scoped token. So `background.js` listens **only** on
`game-log-rest-live.dndbeyond.com` and stores the Bearer token from those requests —
a token DDB itself just used successfully. That's why "scroll the dice log" is the
capture step: it forces the browser to make exactly that request.

---

## Files

| File | Role |
|---|---|
| `manifest.json` | MV3 manifest, permissions, host access for DDB + Supabase. |
| `background.js` | Service worker that captures the game-log Bearer token. |
| `popup.html` | The toolbar popup UI. |
| `popup.js` | Sync logic: campaign config, DDB fetch/paginate, normalize, Supabase upsert. |
| `icon.png` | Toolbar icon. |
