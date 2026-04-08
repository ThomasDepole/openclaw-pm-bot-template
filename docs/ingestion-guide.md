# Ingestion Guide — Building Your PM Agent's Memory

**The most important thing to understand:** Your PM agent starts with zero context. It doesn't know your company, your clients, your team, or your projects. Ingestion is how you fix that.

Think of it like onboarding a new employee. On day one they're smart and capable, but they need to be briefed. The more thoroughly you brief them, the faster they become genuinely useful. Skipping ingestion and expecting the agent to be helpful is like sending a new hire into a client meeting with no background.

---

## How Ingestion Works

1. **You drop files** into the `ingestion/` folder (or subfolders — see below)
2. **You tell the agent** to process them: *"Can you ingest what's in the ingestion folder?"*
3. **The agent reads, organizes, and writes** structured notes to `memory/` files
4. **Source files are deleted** — the `ingestion/` folder is a drop zone, not an archive
5. **You ask questions** — now the agent has context to work with

That's it. The more you feed in, the smarter it gets.

---

## Where to Drop Files

| Folder | What goes here |
|--------|----------------|
| `ingestion/meetings/` | Meeting notes, call summaries, scrum notes, AI transcripts |
| `ingestion/status-reports/` | Weekly/sprint status updates, project health reports |
| `ingestion/projects/` | SOWs, project briefs, charters, change orders |
| `ingestion/people/` | Team rosters, org charts, stakeholder lists |
| `ingestion/clients/` | Client overviews, account context, key contacts |
| `ingestion/processes/` | SOPs, workflows, policies, standards, methodologies |
| `ingestion/reference/` | Company overview, general context, anything else |
| `ingestion/calendar/` | Calendar screenshots or exports |
| `ingestion/raid-logs/` | RAID log files (authoritative current version) |

*Each subfolder has a `README.md` with more detail on what belongs there and tips for that file type.*

---

## What to Drop First (Priority Order)

Don't dump everything at once — start with what gives the most context fastest.

### Tier 1 — Foundation (drop these first)
These tell the agent what world it's operating in. Without these, everything else is context-free.

- **Company overview** — what the company does, who it serves, how it makes money. Even a rough internal doc or the "About" section of your website works.
- **Team roster** — names, roles, who reports to whom. A spreadsheet, org chart, or even a list in a text file.
- **Client list** — active clients, what you're doing for each, key contacts.

### Tier 2 — Work Context
Once the agent knows who everyone is and what the company does, layer in the work.

- **Active project list or status dashboard** — what's in flight, what's done, what's upcoming
- **Project status reports** — even old ones; they build understanding of scope and history
- **Existing RAID logs** — the agent can reference these and add to them as it processes meetings

### Tier 3 — How Things Work
- **Process documentation** — how you run sprints, how escalations work, how projects are kicked off
- **Meeting cadences** — what meetings happen, how often, who attends
- **Templates or standards** — how work is structured, what "done" looks like

### Ongoing
- **Meeting notes** — the most valuable ongoing input. The more consistently meetings are ingested, the more the agent's picture of the work stays current.
- **Calendar screenshots** — helps the agent match meeting references in notes to actual scheduled events

---

## Supported File Formats

| Format | How it's read |
|--------|--------------|
| `.md`, `.txt` | Read directly |
| `.pdf` | Extracted via script |
| `.docx` | Extracted via script |
| `.xlsx`, `.csv` | Extracted as markdown table |
| `.pptx` | Extracted slide-by-slide |
| `.png`, `.jpg` | Read directly (calendar screenshots, diagrams) |

For binary files, the agent uses an extraction script automatically. If it fails, see the troubleshooting note in `docs/setup-guide.md`.

---

## What the Agent Does With Your Files

When you ask the agent to ingest, it:

1. **Reads each file** and identifies what type of content it contains
2. **Organizes the information** into categories — company, clients, projects, people, processes, open questions
3. **Writes to memory files** — structured, queryable notes in `memory/`
4. **Updates the ingestion log** — so you can see what's been processed and when
5. **Surfaces key findings** — tells you what it found, what stood out, and any questions it has
6. **Deletes the source file** — the drop zone stays clean; memory files are the record

---

## The Memory Files

After ingestion, your information lives here:

| File | What's in it |
|------|-------------|
| `memory/company.md` | What the company does, its services, structure, culture |
| `memory/clients.md` | Client names, context, active work, key contacts |
| `memory/projects.md` | Active and past projects — status, team, timeline, risks |
| `memory/people.md` | Team members and stakeholders — roles, background, notes |
| `memory/processes.md` | How things work — workflows, standards, methodologies |
| `memory/calendar.md` | Upcoming and recent meetings (from calendar screenshots) |
| `memory/decisions.md` | Key decisions made — what was decided, when, by whom |
| `memory/raid-pending.md` | RAID items flagged from meetings, pending your review |
| `memory/open-questions.md` | Things that are unclear or need follow-up |
| `memory/ingestion-log.md` | Log of every file ingested — what it was, when, what was in it |
| `memory/meetings/` | Processed meeting summaries — one file per meeting |

---

## What Good Ingestion Looks Like

**A company overview doc** might result in `memory/company.md` containing: mission, service lines, target clients, team structure, revenue model, key differentiators.

**A team roster spreadsheet** might result in `memory/people.md` with a section per person: name, title, which projects they're on, any relevant background.

**A project status report** might result in `memory/projects.md` being updated with: current status, upcoming milestones, open blockers, stakeholder notes.

**A meeting notes file** might result in: a summary in `memory/meetings/`, 2-3 new Trello/Jira cards for action items, and 1-2 new entries in `memory/raid-pending.md`.

---

## Tips for Better Ingestion

- **More context is better than less.** If you're unsure whether to drop something, drop it. The agent filters signal from noise.
- **Name files helpfully.** `2026-03-03-weekly-standup.md` is better than `notes.txt`. The agent works with whatever you give it, but clear names help.
- **Meeting notes don't need to be polished.** Raw AI transcripts, rough notes, even bullet lists work. The agent distills them.
- **Drop calendar screenshots regularly.** They help the agent connect meeting references in notes to actual scheduled events and participants.
- **Re-ingest when things change significantly.** If a major project shifts, drop an updated status report. The agent will update its notes.

---

## The Compounding Effect

This is worth saying explicitly: **the agent gets exponentially more useful over time.**

In week one, it will ask a lot of questions. By week four, it will know your clients well enough to flag when a risk in one meeting connects to a pattern it saw three meetings ago. It will know your team well enough to notice when someone is overloaded. It will know your processes well enough to push back when something is skipping a step.

That doesn't happen without consistent ingestion. The investment is front-loaded — it pays off fast.
