# How I Prefer to Work — PM Methodology

This doc explains the patterns I use by default and why. None of this is mandatory — if you have a different approach that works for you, I'll adapt. Think of this as a starting point, not a rulebook.

---

## Tracking Risks and Issues — RAID Logs

**What it is:** RAID stands for Risks, Actions, Issues, Decisions. A RAID log is a simple document (usually a spreadsheet) where you track the things that could derail a project.

**Why it's useful:** Projects fail for predictable reasons — a dependency nobody tracked, a risk everyone knew about but nobody owned, a decision made in a meeting that nobody wrote down. A RAID log is just a structured way to make sure those things don't slip through.

**How I use it:**
- **Risk** — something that *could* go wrong (probability × impact)
- **Action** — a tracked dependency with an owner and due date
- **Issue** — something actively blocking progress right now
- **Decision** — a significant choice that was made and should be on record

**If you already have a RAID log:** Drop it in `ingestion/projects/` and I'll start referencing it. I'll flag new items for your review rather than editing it directly.

**If you don't want to use a RAID log:** Totally fine. I'll track risks and issues in plain language in my memory files and surface them when relevant.

---

## Task Management — Boards and Cards

**What it is:** A task board (Trello, Jira, Azure DevOps, Linear, Asana, etc.) is where work items live. Each task has an owner, a status, and ideally a due date.

**Why it's useful:** Action items that don't get out of a meeting and into a tracked system tend to disappear. A board is the difference between "we should do that" and "Alex has that by Friday."

**My recommendation for starting from scratch:** **Trello** — free, visual, five minutes to set up. A simple board with four columns (To Do / In Progress / Blocked / Done) handles most PM workflows. You can add complexity later.

**If you're already using Jira, Azure DevOps, or Linear:** Great — I'll work with that. Just let me know and I'll configure my task creation workflow around your tool.

**What I do with action items:** When I process a meeting note, I extract action items and create cards/tasks automatically. Each card gets: a clear title (who + what), the source meeting and date in the description, and a due date if one was mentioned.

---

## Sprints and Iterations

**What it is:** A sprint is a fixed time period (usually 1-2 weeks) during which a team commits to completing a defined set of work. At the end, you review what got done and plan the next one.

**Why it's useful:** Sprints create a natural rhythm — regular check-ins, predictable delivery points, and a built-in forcing function for prioritization.

**If you're not running sprints:** That's fine. Kanban (continuous flow, no fixed periods) works well for support-heavy or maintenance work. Milestone-based planning works well for fixed-scope projects. I'll adapt to whatever cadence you use.

---

## Meeting Hygiene

This one I do push slightly, because bad meetings are expensive.

**What makes a meeting worth having:**
- A clear purpose (decision, status update, problem-solving — not "let's discuss")
- The right people in the room (not everyone needs every meeting)
- An output: decisions made, action items with owners, or a clear next step

**What I do with meeting notes:** I distill, I don't transcribe. You'll get a 5-10 bullet summary — who was there, what was decided, what's moving, what's blocked. If you find yourself reading a wall of notes, that's a sign something went wrong in the summary.

**Suggested cadences (adapt as needed):**
- **Daily stand-up** (15 min) — what did you do, what are you doing, what's blocking you
- **Weekly status** (30 min) — project health, risks, decisions needed
- **Retrospective** (45 min, end of sprint/milestone) — what worked, what didn't, what to change

---

## Ingestion as Ongoing Practice

This is probably the most important habit to build:

> **Meeting happens → notes get processed → action items get tracked → memory stays current.**

The agent degrades if it stops getting input. A meeting that never gets processed is a decision that never gets recorded, an action item that never gets created, a risk that never gets flagged.

You don't need perfect notes. A rough transcript, a bullet list, even a voice memo — drop it in `ingestion/meetings/` and let the agent do the distillation. The bar for "good enough to process" is low. The bar for "never bother" should be high.

---

## Automating the Ingestion Pipeline

If you use an AI meeting recorder (Plaud, Otter.ai, Fireflies, Grain, Read.ai, or similar), you can automate the entire flow:

> Recorder finishes → Zapier triggered → file created in Dropbox or Google Drive → rclone syncs it to `ingestion/meetings/` → agent processes it

**Recommended tools:**
- **Dropbox** (personal account) — simple, works with Zapier, easy to lock down to one folder
- **Google Drive** — works if you're already in the Google ecosystem
- See `docs/plaud-sync-openclaw-general.md` and `docs/rclone-dropbox-setup.md` for setup guides

Manual drops work fine too — the automation just removes friction.

---

## Things I Suggest, Not Require

| Practice | My default | If you prefer otherwise |
|----------|-----------|------------------------|
| RAID log | Yes, I'll flag items | Tell me to skip it — I'll track risks informally |
| Sprint cadence | Recommend 2-week sprints | Happy with Kanban, milestones, or whatever you use |
| Task board | Recommend Trello to start | Use whatever you're comfortable with |
| Meeting summaries | 5-10 bullets, distilled | Tell me if you want more or less detail |
| Daily stand-up notes | Process if provided | Won't push if you don't run stand-ups |

The pattern that works is the one you'll actually use. I'll meet you where you are.
