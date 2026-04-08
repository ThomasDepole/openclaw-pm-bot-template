# memory/boards/

Board configuration files. One file per configured board.

Board configs store the IDs and operational details your agent needs
to work with a specific board — without loading the full process docs.

## Structure

```
memory/boards/
├── active/     ← boards currently in use
│   └── [board-name].md
└── archived/   ← boards that are no longer active
```

## What Goes in a Board Config File

Each `active/[board-name].md` should include:
- Platform (Trello, Notion, Planner, Jira)
- Board/database ID
- Lists/columns with IDs
- Labels/tags with IDs (if applicable)
- Routing rules specific to this board
- Completion/archive rules
- Any special notes about this board's workflow

See the platform adapter in `processes/boards.[platform].md` for the API commands
that use these IDs.
