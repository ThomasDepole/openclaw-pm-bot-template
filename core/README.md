# core/

⛔ **DO NOT EDIT FILES IN THIS FOLDER.**

These are core process documents maintained by the PM bot template.
Future template upgrades will overwrite the contents of this folder.

If you edit files here, your changes will be lost on the next upgrade.

---

## How to Customize

Add your workspace-specific rules, overrides, and customizations in the
corresponding file in `processes/`. Each file there starts with a pointer
to read the relevant `core/` file first, then surfaces your customizations below.

Pattern:
- `core/ingestion.md` — generic ingestion workflow (do not touch)
- `processes/ingestion.md` — read core first, then your deployment-specific rules

---

## What's Here

| File | Purpose |
|------|---------|
| `boards.md` | Generic board concepts: card naming, routing, checklists, labels |
| `boards.trello.md` | Trello API adapter |
| `boards.notion.md` | Notion API adapter |
| `boards.planner.md` | Microsoft Planner API adapter |
| `boards.jira.md` | Jira adapter stub |
| `ingestion.md` | All ingestion workflows: documents, meetings, calendar, RAID, weekly plans |
| `emails.md` | Email drafting workflow, proxy card format, routing pattern |
| `raid.md` | RAID methodology, pending workflow, item identification |

---

## For Developers

These files are part of the [openclaw-pm-bot-template](https://github.com/ThomasDepole/openclaw-pm-bot-template).
To propose changes to core process docs, open a PR against that repo.
The `processes/` user layer is yours to customize freely.
