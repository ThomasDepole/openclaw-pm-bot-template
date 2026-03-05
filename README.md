# OpenClaw PM Bot — Workspace Template

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/ThomasDepole/openclaw-pm-bot-template/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/built%20on-OpenClaw-purple.svg)](https://docs.openclaw.ai)

**A ready-to-deploy project management assistant built on [OpenClaw](https://docs.openclaw.ai).**

This template gives you a PM bot that tracks projects, processes meeting notes, flags risks, creates action items, and maintains an organized knowledge base about your company, clients, team, and work — all through a simple drop-folder ingestion process. No integrations required to get started. Drop a document, ask it to read it, and it gets smarter.

> **This is a template, not a finished product.** Clone it, point an OpenClaw agent at it, answer a few setup questions, and you're running. The bot learns your context as you feed it documents.

---

## Table of Contents

1. [What This Bot Does](#what-this-bot-does)
2. [Quick Start](#quick-start)
3. [The Ingestion Process](#the-ingestion-process)
4. [Ingestion Folder Structure](#ingestion-folder-structure)
5. [The Memory System](#the-memory-system)
6. [Setting Up Task Management](#setting-up-task-management)
7. [Automating Meeting Notes](#automating-meeting-notes)
8. [PM Methodology & How the Bot Works](#pm-methodology--how-the-bot-works)
9. [Customizing the Bot](#customizing-the-bot)
10. [File Reference](#file-reference)
11. [Roadmap](#roadmap)
12. [FAQ](#faq)

---

## What This Bot Does

This is a project management assistant that:

- **Processes meeting notes** — reads raw notes or AI transcripts, distills them into concise summaries, extracts action items, and flags risks
- **Creates action items** — automatically creates tasks in your task management tool (Trello, Jira, Azure DevOps, Linear, Asana, GitHub Issues, and more)
- **Tracks risks and issues** — flags items for RAID logs, surfaces blockers, monitors what's at risk
- **Maintains a knowledge base** — builds and updates a structured memory of your company, clients, projects, team, and processes
- **Answers questions** — "What's the status of Project X?" / "Who owns the Y deliverable?" / "What did we decide about Z in last week's meeting?"

**What it is not:** a calendar assistant, a document editor, or a project management tool by itself. It's the intelligent layer *on top* of the tools you already use.

---

## Quick Start

### Already have an OpenClaw bot? Let it do the setup for you.

Copy the prompt below, fill in the tokens, and paste it into any active OpenClaw bot. It will clone the workspace, show you the config to add, and walk you through the rest.

```
I'd like to set up a new OpenClaw PM bot using the official template. Can you help me stand it up?

Bot name: {{BOT_NAME}}
Display name: {{DISPLAY_NAME}}
Channel: {{CHANNEL_DESCRIPTION}}

Please do the following:

1. Find where your current workspace lives and create a new sibling folder called workspace-{{BOT_NAME}} next to it

2. Clone the PM bot template into that new folder:
   git clone https://github.com/ThomasDepole/openclaw-pm-bot-template.git <full-path>/workspace-{{BOT_NAME}}

3. Show me the openclaw.json snippet I need to add — both the agents.list entry and the
   bindings entry — to create a new agent called {{BOT_NAME}} pointing at that workspace
   and bound to {{CHANNEL_DESCRIPTION}}

4. Let me know what to do after I've added the config and restarted the gateway

I'll handle the openclaw.json edit and gateway restart myself — just get the workspace
cloned and show me exactly what config to add.
```

**Tokens to fill in:**
- `{{BOT_NAME}}` — short name, no spaces (e.g. `pm-acme`, `ops-bot`)
- `{{DISPLAY_NAME}}` — human-readable name (e.g. `Acme PM Bot`)
- `{{CHANNEL_DESCRIPTION}}` — where it lives (e.g. `the #pm-bot Discord channel`)

After the bot clones the workspace and shows you the config snippet: add it to `openclaw.json`, restart the gateway, and send your first message to the new bot. It will introduce itself and walk you through setup.

> The full prompt (with token guide and next steps) is also in [`prompts/setup-new-bot.md`](prompts/setup-new-bot.md).

---

### Manual setup (no existing bot)

### 1. Clone this repo as your agent's workspace

```bash
git clone https://github.com/your-org/openclaw-pm-template.git workspace-yourname
```

### 2. Point an OpenClaw agent at the workspace

Add the agent to your `openclaw.json` config:

**`agents.list` entry:**
```json
{
  "id": "pm-bot",
  "name": "PM Bot",
  "workspace": "/home/node/.openclaw/workspace-yourname",
  "model": { "primary": "anthropic/claude-sonnet-4-6" },
  "tools": { "deny": ["gateway"] }
}
```

**`bindings` entry** (Discord channel example):
```json
{
  "agentId": "pm-bot",
  "match": {
    "channel": "discord",
    "peer": {
      "kind": "channel",
      "id": "YOUR_DISCORD_CHANNEL_ID"
    },
    "guildId": "YOUR_DISCORD_GUILD_ID"
  }
}
```

Both go into the top-level `openclaw.json` — `agents.list` is an array of agent definitions, `bindings` is a separate top-level array that routes messages to agents. Restart the gateway after saving. See [OpenClaw docs](https://docs.openclaw.ai) for full config reference and other channel types (Telegram, Slack, etc.).

### 3. Have your first conversation

When the bot starts for the first time, it will:
- Introduce itself briefly
- Ask you a few setup questions (your name, company, what tools you use)
- Explain the ingestion process
- Ask you to drop your first document

This is driven by `BOOTSTRAP.md` — it only runs once and self-destructs after setup is complete.

### 4. Drop your first documents

Put a company overview or project brief in the appropriate `ingestion/` subfolder and tell the bot to process it. That's it — you're running.

---

## The Ingestion Process

**This is the most important concept to understand.**

The bot starts with zero knowledge about you, your company, your clients, or your projects. Ingestion is how it learns. Think of it like onboarding a new employee — smart and capable on day one, but they need to be briefed. The more thoroughly you brief them, the faster they become genuinely useful.

### How it works

1. **You drop a file** into the appropriate subfolder inside `ingestion/`
2. **You tell the bot** to process it: *"Can you ingest what's in the ingestion folder?"*
3. **The bot reads, organizes, and writes** structured notes to the `memory/` files
4. **The source file is deleted** — the ingestion folder is a drop zone, not an archive
5. **The bot surfaces findings** — it tells you what it found, what stood out, and any open questions

### What to drop first

Start with the documents that give the most context fastest:

**Tier 1 — Foundation (start here)**
| Document | Where to drop | What the bot learns |
|----------|--------------|---------------------|
| Company overview / about doc | `reference/` | What the company does, who it serves |
| Team roster | `people/` | Names, roles, who owns what |
| Client list | `clients/` | Active clients, account context |

**Tier 2 — Work context (once Tier 1 is done)**
| Document | Where to drop | What the bot learns |
|----------|--------------|---------------------|
| Active project list or status report | `status-reports/` or `projects/` | What's in flight, current state |
| SOWs and project briefs | `projects/` | Scope, timeline, stakeholders |
| Existing RAID logs | `projects/` | Risks, issues, decisions already tracked |

**Tier 3 — Depth (ongoing)**
| Document | Where to drop | What the bot learns |
|----------|--------------|---------------------|
| Process docs, SOPs, policies | `processes/` | How things work here |
| Meeting notes | `meetings/` | What happened, what was decided |
| Calendar screenshots | `calendar/` | Meeting context and attendees |

### The compounding effect

The bot gets exponentially more useful over time. In week one it asks a lot of questions. By week four it knows your clients well enough to connect a risk in one meeting to a pattern it saw three meetings ago. That only happens with consistent ingestion — especially meeting notes.

### Supported file formats

| Format | Notes |
|--------|-------|
| `.md`, `.txt` | Read directly — preferred format for meeting notes |
| `.pdf` | Extracted automatically |
| `.docx` | Extracted automatically |
| `.xlsx`, `.csv` | Extracted as markdown tables |
| `.pptx` | Extracted slide-by-slide |
| `.png`, `.jpg` | Read directly (calendar screenshots, diagrams) |

---

## Ingestion Folder Structure

The `ingestion/` folder is organized so it's obvious what goes where. Each subfolder has its own `README.md` with details.

```
ingestion/
├── README.md               ← Start here
├── meetings/               ← Meeting notes, stand-ups, call summaries
├── status-reports/         ← Weekly/sprint status updates, dashboards
├── projects/               ← SOWs, briefs, RAID logs, change orders
├── people/                 ← Team rosters, org charts, stakeholder lists
├── clients/                ← Client overviews, account context
├── processes/              ← SOPs, workflows, policies, standards
├── reference/              ← Company overview, general context, catch-all
└── calendar/               ← Calendar exports/screenshots (optional)
```

### What goes where — quick reference

**`meetings/`** — Any written record of a conversation that had decisions or action items. Raw AI transcripts, rough bullet notes, formal minutes — all fine. The bot distills it.

**`status-reports/`** — Weekly updates, sprint reviews, project health snapshots, burn-down reports. Tells the bot where things stand right now.

**`projects/`** — The "what are we building and why" docs. SOWs, project charters, change orders, RAID logs. Drop these early — they're the foundation for everything project-related.

**`people/`** — Anyone who appears in your meetings, projects, or clients. A simple Name / Role / Email spreadsheet is enough to start. The bot builds on it as names appear in other docs.

**`clients/`** — One section per client: who they are, what you're doing for them, key contacts. If you're not a consultancy, use this for internal stakeholders and business units.

**`processes/`** — How things work here. Sprint process, escalation paths, approval chains, HR policies, QA standards. Helps the bot understand the *why* behind decisions.

**`reference/`** — Anything that doesn't fit elsewhere. Company history, industry context, glossaries, general background. If you're not sure where it goes, put it here.

**`calendar/`** — Optional. Screenshots or exports of your calendar help the bot match informal meeting references ("the Monday sync") to real events with attendees and times. Skip this if you're not comfortable sharing calendar data.

---

## The Memory System

Everything the bot learns lives in the `memory/` folder. These files are the permanent record — source files are deleted after ingestion. Understanding what goes where helps you know where to look when you want to verify what the bot knows.

```
memory/
├── MEMORY.md           ← (at workspace root) Fast-load reference: active projects, key IDs, standing rules
├── company.md          ← What the company does, structure, services, revenue
├── clients.md          ← One section per client — status, open items, key contacts
├── projects.md         ← Project tracking + naming conventions / lookup table
├── project-status.md   ← Running status snapshot across all active projects
├── people.md           ← External contacts, stakeholders, client-side people
├── roles.md            ← Formal role definitions and reporting structure
├── processes.md        ← How things work — workflows, standards, methodologies
├── calendar.md         ← Meeting schedule built from calendar inputs
├── decisions.md        ← Key decisions that affected scope, cost, or timeline
├── task-board.md       ← Task management tool configuration (board/list/label IDs)
├── raid-pending.md     ← RAID items flagged from meetings, pending your review
├── raid-logs.md        ← Snapshot of actual RAID log state per project
├── open-questions.md   ← Things that are unclear or need follow-up
├── ingestion-log.md    ← Log of every file processed — what, when, what was in it
├── team/               ← One file per team member (roles, strengths, what they own)
├── personal/           ← Personal context for the primary user (kept separate from work)
├── extracted/          ← Raw extraction output from documents (source reference)
├── meetings/           ← Processed meeting summaries (one file per meeting, 5-10 bullets)
└── YYYY-MM-DD.md       ← Daily session logs — what happened, what was decided
```

### What each file is for

**The fast-load reference**

`MEMORY.md` lives at the workspace root (not in `memory/`). Every session — including background sub-agents — reads this first. It's a cheat sheet: active projects, key people, task board IDs, standing rules. Keep it current. A stale `MEMORY.md` means every session starts with outdated context.

**Company & client knowledge**

| File | What's in it |
|------|-------------|
| `company.md` | What the company does, who it serves, revenue, strategic direction |
| `clients.md` | One section per client — project status, open items, key contacts, RAID highlights |
| `projects.md` | Active and past projects plus the **naming conventions / lookup table** — cross-referenced whenever a project name is ambiguous or potentially misspelled |
| `project-status.md` | Running status snapshot updated with every status report ingestion — more current than `projects.md` |

**People**

| File | What's in it |
|------|-------------|
| `people.md` | Client contacts, external stakeholders, anyone outside the team |
| `team/[name].md` | One file per team member — role, strengths, what they own, working notes |
| `roles.md` | Formal role definitions and reporting structure |
| `personal/` | Personal context for the primary user — kept separate from work content |

**Meeting & calendar tracking**

| File | What's in it |
|------|-------------|
| `calendar.md` | Canonical meeting schedule from calendar inputs — used to resolve informal meeting references ("the Monday sync") to real events with attendees |
| `meetings/YYYY-MM-DD-name.md` | One file per processed meeting — 5-10 bullet distillation (who, what was decided, what's moving, what's blocked). The record after source notes are deleted. |

**RAID & risk tracking**

| File | What's in it |
|------|-------------|
| `raid-pending.md` | Proposed RAID log changes flagged from meetings — not yet applied to actual logs. Review these and confirm when applied. |
| `raid-logs.md` | Snapshot of each project's actual RAID log state (open item counts, critical items, last updated). Updated when RAID log files are ingested. |

**Process & reference**

| File | What's in it |
|------|-------------|
| `processes.md` | How things work here — PM process, escalation paths, standards |
| `decisions.md` | Significant decisions affecting scope, cost, timeline, or process — the "why did we do it this way" file |
| `task-board.md` | Task management tool configuration — board IDs, list IDs, label IDs |

**Logs & system state**

| File | What's in it |
|------|-------------|
| `YYYY-MM-DD.md` | Daily session logs — what happened, decisions made, what's open |
| `ingestion-log.md` | Every file processed: filename, date, summary of what was in it |
| `extracted/` | Raw extraction output kept as source reference — distilled content lives in `project-status.md` and `clients.md` |
| `heartbeat-state.json` | System timestamps for heartbeat checks — not for human editing |

### How memory works across sessions

The bot starts each session fresh — no in-session memory carries over between conversations. The memory files are how it persists. At the start of every session it reads `MEMORY.md` and relevant memory files to rebuild context.

**Key implications:**
- Important information must be written to a file to survive a session restart
- The more current your memory files are, the faster and smarter every session starts
- Sub-agents spawned for background work (like ingestion) get the same memory files — they don't need to be re-briefed if the files are well-maintained
- `ingestion-log.md` is your audit trail — it tells you exactly what the bot has processed and when

### The naming conventions lookup

One of the most important parts of `memory/projects.md` is the **Naming Conventions / Lookups & Mappings** section. AI meeting recorders frequently mishear or misspell project names. The bot cross-references this table on every ingestion to correct misspellings before writing to memory. If it can't match a name, it flags it to you rather than guessing.

Populate this table early — especially if your team uses internal nicknames, Jira codes, or if you use an AI recorder. It pays off quickly.

### The RAID pending workflow

When the bot processes a meeting and identifies a risk, action, issue, or decision that should be in a RAID log, it adds it to `memory/raid-pending.md` rather than editing your actual RAID log directly. This gives you a review step before anything gets committed.

When you've reviewed and applied an item to your real RAID log, tell the bot — it archives the entry. When you drop an actual RAID log file into `ingestion/raid-logs/`, the bot compares it against pending items and auto-archives anything now reflected in the log.

---

## Setting Up Task Management

The bot can create action items automatically in your task management tool when it processes meeting notes. This requires a one-time configuration.

### Supported tools

| Tool | Setup difficulty | Best for |
|------|-----------------|----------|
| **Trello** | Easy (recommended for new setups) | Visual boards, simple workflows |
| **Jira** | Moderate | Software teams, Agile workflows |
| **Azure DevOps** | Moderate | Microsoft shops, enterprise |
| **Linear** | Easy | Engineering-focused teams |
| **GitHub Issues** | Easy | Developer teams |
| **Asana** | Easy | Cross-functional teams |

**If you're starting from scratch:** Trello is the recommended starting point. It's free, visual, takes five minutes to set up, and the bot's integration is straightforward.

### Setup steps

1. **Choose your tool** and note it in `TOOLS.md`
2. **Get API credentials** — see `docs/tool-integrations.md` for step-by-step instructions for each tool
3. **Store credentials in `.env`** — copy `.env.example` to `.env` and fill in your values (`.env` is git-ignored)
4. **Record board/project IDs** in `memory/task-board.md`
5. **Update the task creation commands** in `AGENTS.md` with your real API calls

Until this is configured, the bot will describe action items in plain text and ask you to create them manually.

### What task cards look like

When the bot creates a task, it includes:
- **Title:** `[Owner] — [What]` (e.g., "Alex — confirm Dropbox access before Friday")
- **Description:** Source meeting and date, why it matters, relevant context
- **Due date:** If a deadline was mentioned in the meeting
- **Labels:** Obvious ones applied (Urgent, Blocked, Client-Facing, etc.)

---

## Automating Meeting Notes

Manually dropping meeting notes works. Automating it is better.

If you use an AI meeting recorder (Plaud, Otter.ai, Fireflies, Grain, Read.ai, or similar), you can set up a pipeline that delivers notes automatically:

```
Recorder finishes
  → Zapier triggered
    → File created in Dropbox or Google Drive
      → rclone syncs to ingestion/meetings/
        → Bot processes on next check
```

### Recommended tools

**For file storage:** Dropbox (personal account recommended — easy to lock down to one folder) or Google Drive.

**For automation:** Zapier — has native integrations with most AI recorders and both Dropbox and Google Drive.

**For syncing to the server:** rclone — lightweight, runs as a cron job, moves files from cloud storage to the ingestion folder.

### Setup guides

- **Plaud + Zapier + Dropbox:** `docs/plaud-sync-openclaw-general.md`
- **rclone + Dropbox (general):** `docs/rclone-dropbox-setup.md`
- The same Dropbox + rclone pattern works for any recorder that can push to Zapier

### Manual drops always work

You don't need automation to get value from the bot. Drop files manually, tell the bot to process them, and you're done. Automation just removes friction for recurring meeting notes.

---

## PM Methodology & How the Bot Works

See `docs/pm-methodology.md` for the full crash course. Here's the short version:

**RAID logs** — a structured way to track Risks, Actions, Issues, and Decisions. The bot flags potential RAID items from every meeting and surfaces them for your review. If you don't want a RAID log, that's fine — the bot will track these informally.

**Task boards** — where action items live so they don't disappear after a meeting. The bot creates cards/tasks automatically. If you don't have a preferred tool, Trello is a good starting point.

**Meeting summaries** — the bot distills meetings into 5-10 bullets: who attended, what was decided, what's moving, what's blocked. Not a transcript — a distillation.

**Sprints** — if you run sprints, the bot understands sprint context. If you don't, it works with milestone-based or Kanban workflows.

**The core principle:** the bot suggests proven PM patterns but never imposes them. If you don't want a RAID log, it won't push back. If you prefer a different workflow, it adapts. The goal is to be useful to *you*, not to enforce a methodology.

---

## Customizing the Bot

### Give it a name

Update `IDENTITY.md` with a name, role title, and any personality notes. The bot responds to whatever name you give it.

### Tune the personality

`SOUL.md` controls how the bot communicates — its tone, judgment, communication style. The default is a professional PM with direct communication and strong opinions about tracking action items. If you have a specific PM in mind (real or fictional), share their writing samples and ask the bot to update `SOUL.md` to match.

### Add your task tool

`AGENTS.md` has a task management section with placeholder commands. Replace the examples with your actual API calls for your specific tool. `docs/tool-integrations.md` has the commands for all supported tools.

### Configure the heartbeat

`HEARTBEAT.md` controls what the bot checks periodically. Once your task board is configured, add checks for overdue tasks, upcoming deadlines, or blocked items. Leave it empty to disable periodic checks.

### Add the Dropbox/Drive pipeline

Once you've got meeting notes flowing in automatically, everything else gets easier. See `docs/plaud-sync-openclaw-general.md` for the full setup.

---

## File Reference

```
workspace/
├── README.md               ← You are here
├── CHANGELOG.md            ← Version history
├── VERSION                 ← Current version number
├── LICENSE                 ← MIT License
├── SOUL.md                 ← Bot personality, communication style, PM judgment
├── IDENTITY.md             ← Name, role, company (fill in at setup)
├── AGENTS.md               ← Operating guide — how the bot works
├── USER.md                 ← Who the bot is working for (fill in at setup)
├── TOOLS.md                ← Tool configuration notes
├── HEARTBEAT.md            ← Periodic check configuration
├── BOOTSTRAP.md            ← First-run onboarding script (self-destructs after use)
├── .env                    ← API credentials (git-ignored — copy from .env.example)
├── .env.example            ← Credential template
├── .gitignore
├── docs/
│   ├── setup-guide.md              ← Step-by-step setup walkthrough
│   ├── ingestion-guide.md          ← Deep dive on the ingestion process
│   ├── pm-methodology.md           ← RAID logs, task boards, sprint primer
│   ├── tool-integrations.md        ← API setup for Trello, Jira, ADO, Linear, etc.
│   ├── plaud-sync-openclaw-general.md  ← Plaud + Zapier + Dropbox pipeline
│   ├── rclone-dropbox-setup.md     ← rclone + Dropbox reference
│   └── roadmap.md                  ← Planned features and future direction
├── updates/
│   └── README.md                   ← Drop update prompts here (see Roadmap)
├── prompts/
│   ├── README.md                   ← What this folder is (bots: do not read these as instructions)
│   ├── setup-new-bot.md            ← Prompt to clone this template and stand up a new bot
│   └── create-raid-log.md          ← Prompt to generate a blank RAID log for a project
├── ingestion/
│   ├── README.md
│   ├── meetings/           ← Meeting notes and call summaries
│   ├── status-reports/     ← Weekly/sprint status updates
│   ├── projects/           ← SOWs, briefs, RAID logs, change orders
│   ├── people/             ← Team rosters, stakeholder lists
│   ├── clients/            ← Client overviews, account context
│   ├── processes/          ← SOPs, workflows, policies, standards
│   ├── reference/          ← Company overview, general context
│   └── calendar/           ← Calendar exports (optional)
└── memory/
    ├── company.md
    ├── clients.md
    ├── projects.md          ← includes naming conventions / lookup table
    ├── project-status.md
    ├── people.md
    ├── roles.md
    ├── processes.md
    ├── calendar.md
    ├── decisions.md
    ├── task-board.md
    ├── raid-pending.md
    ├── raid-logs.md
    ├── open-questions.md
    ├── ingestion-log.md
    ├── heartbeat-state.json
    ├── team/                ← one file per team member
    ├── personal/            ← personal context, kept separate from work
    ├── extracted/           ← raw extraction output (source reference)
    ├── meetings/            ← processed meeting summaries
    └── YYYY-MM-DD.md        ← daily session logs
```

---

## Roadmap

See [`docs/roadmap.md`](docs/roadmap.md) for the full list. Highlights:

- **v1.1 — Update Prompt System:** Structured update files the bot applies intelligently to its own workspace — no git merges, no conflicts, preserves your customizations. Drop a file in `updates/`, tell the bot, done.
- **v1.2 — Passive Update Notifications:** Bot checks for new template releases and proactively lets you know.

The `updates/` folder already exists in your workspace. When v1.1 ships, update prompts will be included in release assets — download and drop in.

---

## FAQ

**The bot doesn't know anything about my company. Is that normal?**
Yes — it starts cold by design. Drop a company overview or project brief into the appropriate `ingestion/` subfolder and ask it to process it. Context grows with every document you add.

**Do I need to use a RAID log?**
No. The bot will suggest it because it works well for tracking risks, but if you don't want it, just say so. It'll track risks and issues informally in plain language.

**Do I need Trello specifically?**
No. Trello is the recommendation for people starting from scratch because it's free and simple. If you're already using Jira, Azure DevOps, Linear, Asana, or GitHub Issues, the bot supports all of them. See `docs/tool-integrations.md`.

**Can I use this for a single project instead of a whole company?**
Absolutely. The memory structure works equally well for a single focused project. The bot will just have one entry in `memory/projects.md` and go deeper on that one context.

**What happens if the bot loses context?**
It reads from memory files at the start of each session, so it rebuilds context quickly. If something important isn't in a memory file, it's lost between sessions. This is why writing things down (to files) matters.

**How do I add a second project later?**
Just drop the project docs into `ingestion/projects/` and ask the bot to process them. It adds to its existing knowledge base.

**Can I automate meeting note delivery?**
Yes — see [Automating Meeting Notes](#automating-meeting-notes) above and `docs/plaud-sync-openclaw-general.md`.

**How do I update the bot's personality?**
Edit `SOUL.md`. If you want it to mimic a specific person's communication style, share some of their writing and ask the bot to update the file accordingly.

**Is this safe for sensitive company information?**
The workspace is just files on your server — as secure as your OpenClaw setup is. Credentials go in `.env` which is git-ignored. Don't commit sensitive data. The bot does not send your information anywhere unless explicitly configured to do so.

---

*Built on [OpenClaw](https://docs.openclaw.ai) — an open-source personal AI agent framework.*
