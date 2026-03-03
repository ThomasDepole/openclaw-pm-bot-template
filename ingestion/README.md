# Ingestion Drop Zone

This folder is how you give your PM agent context. Drop files in the right subfolder, then tell the agent to process them.

**The agent starts with zero knowledge. The more you put in here, the smarter it gets.**

---

## Folder Structure

| Folder | What goes here |
|--------|----------------|
| `meetings/` | Meeting notes, call summaries, scrum notes, AI transcripts |
| `status-reports/` | Weekly/sprint status updates, project health reports |
| `projects/` | SOWs, project briefs, charters, RAID logs, change orders |
| `people/` | Team rosters, org charts, stakeholder lists |
| `clients/` | Client overviews, account context, key contacts |
| `processes/` | SOPs, workflows, policies, standards, methodologies |
| `reference/` | Company overview, general context, anything else |
| `calendar/` | Calendar screenshots or exports *(optional)* |

Each folder has a `README.md` inside with more detail on what belongs there.

---

## How It Works

1. Drop your files in the appropriate subfolder
2. Tell the agent: *"Can you ingest what's in the ingestion folder?"*
3. The agent reads, organizes, and writes structured notes to `memory/`
4. Source files are deleted after processing — `memory/` is the permanent record

---

## Where to Start

If this is your first time, drop these first:
1. A company overview doc → `reference/`
2. Your team roster → `people/`
3. Your active project list or a project brief → `projects/`

Everything else can follow. See `docs/ingestion-guide.md` for the full priority order and tips.

---

## Supported File Formats

`.md` `.txt` `.pdf` `.docx` `.xlsx` `.csv` `.pptx` `.png` `.jpg`

---

## Automating Meeting Note Delivery

Instead of manually dropping meeting notes, you can automate it:
- **Plaud, Otter.ai, Fireflies, or any AI recorder** → Zapier → Dropbox or Google Drive → syncs to `meetings/` automatically
- See `docs/plaud-sync-openclaw-general.md` and `docs/rclone-dropbox-setup.md` for setup guides
