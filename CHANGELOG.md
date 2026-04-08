# Changelog

All notable changes to this project will be documented in this file.

This project uses [Semantic Versioning](https://semver.org/).

---

## [1.7.1] - 2026-04-08

### Patch — MEMORY.md startup and reference fixes

- `AGENTS.md` Every Session: added `MEMORY.md` as step 1 (was missing — fresh bots would skip their own cheat sheet)
- `README.md` memory tree: removed `MEMORY.md` from confusing position inside `memory/` block
- `README.md` File Reference: added `MEMORY.md` to workspace root tree

---

## [1.7.0] - 2026-04-08

### Documentation fixes and consistency pass

**Stale `memory/task-board.md` references removed (7 locations)**
- `TOOLS.md` — board IDs pointer updated to `memory/boards/active/[board-name].md`
- `README.md` — 4 references updated (memory tree ×2, setup step, memory table row)
- `docs/setup-guide.md` — Step 2 item 4 and troubleshooting row updated

**README.md**
- Version badge updated to `1.6.0`
- Ingestion folder tree: added `raid-logs/`
- "What goes where" section: added `raid-logs/` entry with description
- File Reference tree: added `core/`, `processes/`, `tools/` sections; memory section now includes `naming-conventions.md`, `boards/active/`, `heartbeat-state.json`; removed `task-board.md`

**AGENTS.md**
- Memory structure diagram ingestion section: expanded from 3 to all 9 subfolders; removed non-existent `weekly-plans/`
- Memory structure diagram memory section: added `project-status.md`, `roles.md`, `heartbeat-state.json`, `personal/`, `extracted/`
- Credentials example: hardcoded workspace path replaced with generic placeholder + comment

**`.env.example`** — added `NOTION_TOKEN` and `PLANNER_*` credential blocks

**`docs/ingestion-guide.md`** — replaced 3-row "dump in root" table with proper 9-subfolder table matching actual structure

**`IDENTITY.md`** — added Visual Identity section pointing to `self-portrait/` folder

**`scripts/README.md`** (new) — explains extraction script lives at system level, not here; notes folder is available for custom deployment scripts

---

## [1.6.0] - 2026-04-08

### Cleanup, ingestion fixes, and integration docs

**Ingestion**
- Added `ingestion/raid-logs/` subfolder with README
- Removed `weekly-plans/` ingestion path — this is a deployment-specific workflow, not a core template pattern
- Updated `ingestion/README.md` folder table to include `raid-logs/`, removed `weekly-plans/`
- Removed "Weekly Plans / Status Reports" section from `core/ingestion.md` and `processes/ingestion.md`
- Deleted malformed `ingestion/{status-reports,...}` folder (bad glob expansion)

**HEARTBEAT.md**
- Replaced stub comment with a real working example using placeholder IDs
- Includes all check types: Monday Digest, Morning Brief, Midday Nudge, new overdue alerts, board activity feed, Done list archive
- Includes state file reference, placeholder table, and note on adapting for Notion/Planner

**docs/tool-integrations.md**
- Added three-tier approach intro (REST → MCP → CLI)
- Added Notion section with `tools/notion.sh` usage
- Added Microsoft Planner section with `tools/planner.py` usage, app registration steps, Premium warning
- Updated general notes: `memory/task-board.md` reference replaced with `memory/boards/active/`

**Memory cleanup**
- Deleted `memory/scrums.md`, `memory/sdlc-verbatim.md`, `memory/website.md` (stale/non-generic files)
- Fixed `MEMORY.md` Trello Configuration section → generic Board Configuration pointing to `memory/boards/active/`

---

## [1.5.0] - 2026-04-08

### Core/processes architecture refactor

**New: `core/` folder — untouchable process docs**
- All 8 process docs moved to `core/` with DO NOT EDIT headers
- `core/README.md` — explains the folder, links to processes/, notes for developers
- Files: `boards.md`, `boards.trello.md`, `boards.notion.md`, `boards.planner.md`, `boards.jira.md`, `ingestion.md`, `emails.md`, `raid.md`

**Refactored: `processes/` — thin pointer + customization layer**
- Each file now says "read core/X.md first" then provides a user customization section
- `boards.md` — active platform config + custom routing
- `boards.trello/notion/planner/jira.md` — workspace notes + adapter-specific config
- `ingestion.md` — meeting tool + custom sources
- `emails.md` — routing rules + delivery method
- `raid.md` — project-specific RAID rules
- `README.md` — updated to explain two-layer pattern + how to add custom processes

**Updated: `AGENTS.md`**
- Prominent `⛔ core/` off-limits notice added
- Board/task management section updated to reference new structure
- Off-limits section updated to include core/
- Memory structure diagram updated

**Memory folder cleanup**
- Removed `memory/task-board.md` (replaced by `memory/boards/active/`)
- Removed `memory/trello-boards.md` (platform-specific, outdated)
- Added `memory/boards/` folder with README
- Added `memory/boards/active/` with README + board config template
- Added `memory/boards/archived/.gitkeep`

---

## [1.4.0] - 2026-04-08

### Core process documentation

**New: `processes/` folder fully fleshed out**
- `processes/README.md` — folder index, "do not edit core files" guidance, separation of core vs. custom, how to extend
- `processes/ingestion.md` — full generic ingestion workflow: documents, meeting notes, calendar/schedule files, weekly plans/status reports, RAID log files; workspace-specific config (naming corrections, board IDs) referenced to `memory/`
- `processes/emails.md` — generic email drafting: when to draft, configurable routing rules, Trello proxy card format (internal + external/via-internal patterns), writing style reference, future direct-send migration path
- `processes/raid.md` — RAID log methodology: what belongs in a RAID log (filter guidance), pending workflow, identifying RAID items in meetings (signal patterns per type), processing actual log files, `memory/raid-logs.md` and `memory/raid-pending.md` structure
- `processes/boards.jira.md` — Jira stub: both MCP (mcporter) and REST API paths documented, placeholder sections ready to fill in

**New: `memory/naming-conventions.md`** — scaffold for transcription error corrections referenced by `ingestion.md`; workspace-specific, ships empty

**Design decisions**
- Core process files marked `<!-- core process | do not customize here -->` — convention-based separation, formal override mechanism deferred to future version
- Workspace-specific config stays in `memory/` (IDs, names, routing rules, naming corrections) — processes/ stays generic and upgradeable
- `emails.md` delivery method is configurable — Trello proxy is default, direct send is documented as an upgrade path
- RAID pulled out of ingestion into its own file — substantial enough to stand alone and be referenced independently

---

## [1.3.0] - 2026-04-08

### Board abstraction + Notion & Planner support

**New: `processes/` folder with platform-agnostic board adapter pattern**
- `processes/boards.md` — generic interface: when to create cards, card naming, routing, checklists, labels, two-way PM↔contact workflow, heartbeat checks
- `processes/boards.trello.md` — Trello adapter: full curl command reference for create/update/move/archive/query; includes board discovery and Stacy integration pattern
- `processes/boards.notion.md` — Notion adapter: REST API via integration token; create/update/archive/query; raw curl and script reference
- `processes/boards.planner.md` — Microsoft Planner adapter: Graph API via OAuth 2.0; ETag requirement documented; Premium Planner limitation called out

**New: `tools/` folder with runnable platform helper scripts**
- `tools/README.md` — setup instructions for both platforms; credential config; usage examples
- `tools/notion.sh` — shell script wrapping Notion REST API: `list-tasks`, `create-task`, `update-task`, `complete-task`, `archive-task`, `get-task`, `list-databases`
- `tools/planner.py` — Python 3 script for Microsoft Planner (Graph API): OAuth token fetch + caching, ETag handling, `list-plans`, `list-buckets`, `list-tasks`, `create-task`, `update-task`, `complete-task`, `list-members`

**Design decisions**
- `processes/boards.[platform].md` — adapter docs for agent reading; documents API patterns, auth, caveats
- `tools/` — runnable scripts the agent calls via `exec`; distinct from documentation
- Trello stays curl-only (no binary dependency); Notion uses curl via shell script; Planner uses Python for OAuth token management
- Token cache for Planner stored in `/tmp/.planner_token_cache` — avoids redundant auth calls within a session

---

## [1.0.0] - 2026-03-03

### Initial release

**Core workspace structure**
- `SOUL.md` — professional PM persona with "suggest but don't push" philosophy; adapts to user's workflow rather than enforcing methodology
- `AGENTS.md` — operating guide covering ingestion, memory, task management, tool access, and security
- `BOOTSTRAP.md` — conversational first-run onboarding script; short question-by-question flow, self-destructs after setup
- `IDENTITY.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md` — fill-in-the-blank identity and config files
- `.env.example` — credential template (`.env` is git-ignored)

**Ingestion system**
- `ingestion/` folder with 8 named subfolders: `meetings/`, `status-reports/`, `projects/`, `people/`, `clients/`, `processes/`, `reference/`, `calendar/`
- Each subfolder has a `README.md` explaining what belongs there with examples and tips
- Main `ingestion/README.md` with full folder reference table and onboarding instructions

**Memory system**
- `memory/company.md`, `clients.md`, `projects.md`, `people.md`, `processes.md`, `calendar.md`
- `memory/decisions.md` — key decisions tracked separately from RAID items
- `memory/task-board.md` — task management tool configuration
- `memory/raid-pending.md`, `open-questions.md`, `ingestion-log.md`

**Documentation**
- `docs/setup-guide.md` — step-by-step setup walkthrough
- `docs/ingestion-guide.md` — deep dive on the ingestion process and compounding effect
- `docs/pm-methodology.md` — crash course on RAID logs, task boards, sprints, meeting hygiene
- `docs/tool-integrations.md` — API setup for Trello, Jira, Azure DevOps, Linear, Asana, GitHub Issues
- `docs/plaud-sync-openclaw-general.md` — Plaud + Zapier + Dropbox automated pipeline guide
- `docs/rclone-dropbox-setup.md` — rclone + Dropbox reference for headless Linux servers
- `README.md` — comprehensive one-stop user guide with Quick Start, full feature walkthrough, FAQ

**Design decisions**
- Tool-agnostic: no assumptions about Trello, Plaud, or any specific stack
- No company-specific references (fully generic template)
- BOOTSTRAP is conversational and self-destructing — shapes setup without overwhelming new users
- Ingestion subfolders named for intuitive discovery — new users know what goes where on first look
- `decisions.md` added to memory structure — scope/direction/cost decisions tracked separately from RAID items
