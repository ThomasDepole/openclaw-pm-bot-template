# processes/

Your workspace-specific process customizations.

Files here extend the core process docs in `core/`. Each file:
1. Points to the relevant `core/` file (read that first)
2. Provides a section for your deployment-specific rules, overrides, and config

---

## How It Works

```
core/ingestion.md        ← generic, maintained by template (DO NOT EDIT)
processes/ingestion.md   ← your deployment: "read core first, then my rules"
```

The agent reads `processes/[file].md` when it needs to perform an operation.
That file tells it to load the core doc first, then applies your customizations on top.

---

## Files Here

### Generic interface
| File | Purpose |
|------|---------|
| `boards.md` | Active platform config + custom routing rules |
| `ingestion.md` | Meeting tool config + custom ingestion sources |
| `emails.md` | Routing rules + delivery method |
| `raid.md` | Project-specific RAID rules |

### Platform adapters
| File | Purpose |
|------|---------|
| `boards.trello.md` | Trello workspace notes |
| `boards.notion.md` | Notion workspace notes |
| `boards.planner.md` | Planner workspace notes |
| `boards.jira.md` | Jira configuration (fill in when setting up) |

---

## Adding Custom Processes

Need a process that isn't covered by a core file? Add it directly here.
Name it clearly: `processes/[topic].md`. No need to mirror it in `core/`.

Document it below:

### Custom Processes

<!-- Add your custom process files here as you create them. -->
