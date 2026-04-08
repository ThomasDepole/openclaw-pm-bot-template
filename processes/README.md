# processes/

Core PM workflow documents. The agent reads these before performing specific operations.

---

## What's Here

### Generic interface
| File | Purpose |
|------|---------|
| `boards.md` | Platform-agnostic board concepts: card naming, routing, checklists, labels, two-way handoff |
| `ingestion.md` | All ingestion workflows: documents, meeting notes, calendar, RAID logs, weekly plans |
| `emails.md` | Email drafting, routing rules, proxy card format |
| `raid.md` | RAID log methodology, pending workflow, item identification |

### Platform adapters
| File | Purpose |
|------|---------|
| `boards.trello.md` | Trello curl command reference |
| `boards.notion.md` | Notion REST API adapter + `tools/notion.sh` reference |
| `boards.planner.md` | Microsoft Planner Graph API adapter + `tools/planner.py` reference |
| `boards.jira.md` | Jira stub — configure when ready |

---

## ⚠️ Do Not Edit Core Files

Files in this folder are **core process documents**. They ship with the template and will be updated in future template versions.

**Do not customize them directly.** If you edit them, your changes will be overwritten on the next template upgrade.

**Instead:**
- For workspace-specific config (board IDs, contact names, routing rules, naming corrections): use the `memory/` files
- For process overrides or additions specific to your deployment: use `memory/processes.md` to document exceptions and local rules

The clean separation is:
- `processes/` — **how** things work (generic, durable, upgradeable)
- `memory/` — **what** things are in your specific deployment (IDs, names, routing, decisions)

---

## Customizing Platform Adapters

`boards.trello.md`, `boards.notion.md`, and `boards.planner.md` document API patterns.
Board-specific IDs (board IDs, list IDs, label IDs) do **not** go in these files.
They go in `memory/boards/active/[board-name].md`.

`boards.jira.md` is a stub — fill it in when you configure Jira. Once configured,
treat it as yours and do not expect future template upgrades to overwrite it.

---

## Extending for Your Deployment

If you need a custom process that doesn't fit in `memory/`:

1. Create a new file in `processes/` with a name that makes its scope clear
2. Keep the `<!-- core process -->` comment off your custom files — helps distinguish them at a glance
3. Document it in this README under a "Custom Processes" section below

There is no enforced separation mechanism today — it's convention-based. A more formal
custom override pattern may be introduced in a future template version.
