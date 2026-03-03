# Ingestion Drop Zone

Drop files here to be processed by the PM agent. Ask the agent to ingest when ready.

---

## Where to Drop Files

| File type | Drop here |
|-----------|-----------|
| Company docs, project status, client lists, HR docs, process docs | Root `ingestion/` folder |
| Meeting notes, call summaries, scrum notes | `ingestion/meetings/` |
| Calendar screenshots | `ingestion/calendar/` |

---

## Supported Formats

- `.md` / `.txt` — Plain text (read directly)
- `.pdf` — PDF documents
- `.docx` / `.doc` — Word documents
- `.xlsx` / `.xls` — Excel spreadsheets
- `.pptx` / `.ppt` — PowerPoint presentations
- `.csv` — CSV files
- `.png` / `.jpg` — Images (calendar screenshots, diagrams)

---

## How It Works

1. Drop file(s) here
2. Tell the agent: *"Can you ingest what's in the ingestion folder?"*
3. The agent reads, organizes, and writes structured notes to `memory/`
4. Source files are deleted after processing — `memory/` is the permanent record

---

## Automating Meeting Note Delivery

Instead of manually dropping meeting notes, you can automate delivery using:
- **Plaud + Zapier + Dropbox + rclone** — see `docs/plaud-sync-openclaw-general.md`
- **Other AI recorders** (Otter.ai, Fireflies, Grain, etc.) — same Dropbox pattern applies

---

## Notes

- Files are processed on demand, not automatically
- The ingestion folder is a drop zone — don't use it as long-term storage
- If you drop the same file twice, the agent will process it again — rename or version if needed
