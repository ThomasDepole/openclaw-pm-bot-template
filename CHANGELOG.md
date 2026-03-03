# Changelog

All notable changes to this project will be documented in this file.

This project uses [Semantic Versioning](https://semver.org/).

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
