# PM Agent Setup Guide

**Purpose:** Step-by-step guide for getting your PM agent up and running from scratch.

---

## Overview

This workspace is a template for a PM agent built on OpenClaw. The agent reads meeting notes, tracks projects, flags risks, and creates action items in your task management tool of choice. It learns about your company, clients, and team through an ingestion process — you drop files in, it reads and organizes them.

---

## Step 1: Personalize the Identity Files

Before anything else, update these files to reflect the actual PM and company:

### `IDENTITY.md`
- Fill in the PM's name, role, company, and emoji

### `USER.md`
- Fill in who the primary contact is (name, role, communication style)
- Fill in the company name and type

### `SOUL.md`
- The default is a generic professional PM persona — functional out of the box
- For a more authentic voice: share email samples, Slack messages, or writing from the actual PM and ask the agent to update `SOUL.md` to match their style
- The more specific, the better

---

## Step 2: Choose and Configure a Task Management Tool

The agent can create action items in any major task tool. Pick one and configure it:

1. **Identify your tool:** Trello, Jira, Azure DevOps, Linear, Asana, GitHub Issues, Monday.com, etc.
2. **Get API credentials:** See `docs/tool-integrations.md` for where to get keys for each tool
3. **Store credentials in `.env`:**
   ```
   # .env (at workspace root — git-ignored)
   TOOL_API_KEY=your_key_here
   TOOL_TOKEN=your_token_here
   ```
4. **Record board/project structure in `memory/boards/active/[board-name].md`** — use the template in `memory/boards/active/README.md` as a starting point
5. **Update `TOOLS.md`** with your tool name and credential env var names
6. **Update the "Creating Tasks" section in `AGENTS.md`** with your actual API commands

Until this is configured, the agent will describe action items in plain text and ask you to create them manually.

---

## Step 3: First Ingestion

Once identity and tool are configured, start feeding the agent context:

1. Drop your company overview doc (or a few key docs) into `ingestion/`
2. Ask the agent: *"Can you ingest what's in the ingestion folder?"*
3. The agent will read, organize, and write structured notes to `memory/`
4. Repeat with team rosters, project status reports, client documents, process docs, etc.

**Good starter docs to ingest:**
- Company overview / about page
- Team roster (spreadsheet or org chart)
- Active project list or status dashboard
- Client list
- Process documentation (how you run sprints, how you handle escalations, etc.)
- Any existing RAID logs

---

## Step 4: Set Up Meeting Notes Ingestion (Optional but Recommended)

Manually dropping meeting notes works, but automating it is better. Options:

### Manual
Drop meeting note files (`.txt`, `.md`, `.docx`, `.pdf`) into `ingestion/meetings/` and ask the agent to process them.

### Automated (Plaud + Zapier + Dropbox + rclone)
If you use a Plaud recording device:
- See `docs/plaud-sync-openclaw-general.md` for the full setup guide
- This routes recordings automatically from Plaud → Zapier → Dropbox → ingestion folder

### Automated (Other recording tools)
Most AI meeting recorders (Otter.ai, Fireflies, Grain, Read.ai, etc.) can export summaries to Zapier. The same Dropbox + rclone pattern applies — see the general setup guide.

---

## Step 5: Configure the Heartbeat (Optional)

The heartbeat is a periodic check the agent can run automatically. Once your task board is configured:

1. Open `HEARTBEAT.md`
2. Add checks that make sense for your workflow (overdue tasks, blocked items, upcoming deadlines)
3. The agent will run these checks periodically and flag anything that needs attention

Leave `HEARTBEAT.md` empty until your boards are set up — an empty file means the agent skips the check entirely.

---

## Step 6: Version Control (Optional but Recommended)

The workspace is git-ready. Set up a private repo to back up your agent's memory:

```bash
cd /path/to/workspace
git remote add origin https://github.com/your-org/your-repo.git
git push -u origin main
```

The `.gitignore` already excludes `.env` — credentials won't be committed.

---

## What to Expect

**Week 1:** The agent is in learning mode. Feed it documents, ask questions, and let it build context.

**Week 2+:** The agent starts to be genuinely useful — it knows your clients, projects, and team. Meeting notes get processed faster. Action items get created automatically.

**Over time:** The memory files become a living knowledge base. The agent's quality compounds as context grows.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Agent doesn't know about a client/project | Drop the relevant docs in `ingestion/` and ask it to ingest |
| Task creation failing | Check `.env` credentials and board IDs in `memory/boards/active/` |
| Agent lost context after restart | Normal — it reads from memory files on startup. Make sure important info is written to `memory/` |
| Binary file won't read | Use `python3 /home/node/.openclaw/scripts/extract-doc.py ingestion/<filename>` |
| extract-doc.py fails with import error | Run `pip3 install python-docx openpyxl python-pptx pdfplumber pandas --break-system-packages -q` |
