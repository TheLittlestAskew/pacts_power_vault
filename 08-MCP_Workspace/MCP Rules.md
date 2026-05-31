
# MCP Rules

## Default Behavior

Claude should treat the Obsidian MCP server as a surgical note editor, not as a full-vault research engine.

Claude should only use files listed in `Claude MCP Index.md` or exact paths provided by Taylor.

---

## Forbidden Unless Explicitly Requested

Claude must not:

- search the full vault
- list every file
- scan all tags
- open recordings
- open raw transcripts
- open every session note
- rewrite large tracker files wholesale
- infer campaign canon from DND sourcebooks before checking session notes
- update canon files without producing a patch summary first

---

## Preferred Workflow

1. Read `Claude MCP Index.md`.
2. Read only the specific working file or session file Taylor named.
3. Create proposed updates in `Tracker Patch Queue.md`.
4. Ask for approval if changes affect canon trackers.
5. Patch only the relevant sections.
6. Summarize exactly which files were changed.

---

## Editing Rules

- Preserve existing headings.
- Preserve existing table structures.
- Do not reorder trackers unless Taylor asks.
- Add uncertain information under `Needs Review`.
- Never silently delete existing notes.
- Never merge conflicting lore without flagging the conflict.