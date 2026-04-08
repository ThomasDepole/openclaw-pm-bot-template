# processes/raid.md — RAID Log Workflow
<!-- core process | do not customize here -->

RAID stands for **Risks, Actions, Issues, Decisions**. This file covers when to flag RAID items, how to manage the pending workflow, and how to process actual RAID log files.

---

## What Belongs in a RAID Log

Not everything that comes up in a meeting is a RAID item. Apply this filter:

| Type | Flag it if... | Do NOT flag if... |
|------|--------------|-------------------|
| **Risk** | It could derail the project if left unaddressed | It's a general concern with no concrete impact |
| **Action** | It's a tracked dependency with an owner and a due date | It's a vague "we should do this someday" |
| **Issue** | It's actively blocking progress right now | Someone is venting; work is still moving |
| **Decision** | Something was formally decided that affects scope, cost, or timeline | It's a minor clarification or preference |

**Signal over noise.** A RAID log full of marginal items is worse than a clean one — it buries the real risks.

A good RAID item has:
- **Type** (R/A/I/D)
- **Description** — what it is, why it matters
- **Owner** — who is responsible for it
- **Status** — open, in progress, resolved, closed
- **Due date** (for Actions) or **target resolution date** (for Issues/Risks)

---

## The Pending Workflow

The bot cannot edit RAID logs directly — those live in the PM's source-of-truth tool (spreadsheet, Jira, etc.). Instead, proposed changes are tracked in `memory/raid-pending.md` for the primary contact to review and apply.

### When to Add a Pending Item

Add to `memory/raid-pending.md` when you find:
- A new risk, action, issue, or decision in a meeting, status report, or weekly plan
- An existing RAID item that needs a status update or owner change
- A blocker that isn't already tracked in the log

### Format

Each entry in `memory/raid-pending.md`:

```
### [Type] — [Project/Area] — [Short title]
- **Proposed action:** Add / Update / Close
- **Description:** [What it is and why it matters]
- **Owner:** [Person responsible]
- **Due / Target:** [Date or "ongoing"]
- **Status:** [If updating — current status to set]
- **Source:** [Meeting name, date, or document]
- **Flagged:** [YYYY-MM-DD]
- **Resolution:** [Leave blank until Tom reviews]
```

### Review Cycle

1. Bot flags items to `memory/raid-pending.md` as they are identified
2. Bot surfaces pending items to the primary contact: *"I've flagged 2 new RAID items from today's standup — worth a quick review?"*
3. Contact reviews → applies to actual RAID log → confirms
4. Bot archives the resolved entries in `raid-pending.md`
5. Contact tells the bot when to prune archived entries

Do not let pending items pile up unreviewed. Surface them proactively in meeting summaries and daily digests.

---

## Identifying RAID Items in Meetings

When processing a meeting note, scan for these signals:

**Risk signals:**
- "We're worried about..." / "There's a chance that..." / "If X doesn't happen by Y..."
- A dependency on an external party with no confirmed date
- Scope creep without a change order
- A key person unavailable during a critical period

**Action signals:**
- "Can you / Could you / Please..." with a name attached
- "We need to follow up on..." with an owner and timeline
- A deliverable mentioned with a date

**Issue signals:**
- "We're blocked on..." / "We can't proceed until..."
- Something that was supposed to be done and isn't
- A test failure, environment problem, or access issue actively stopping work

**Decision signals:**
- "We've decided to..." / "We're going with..." / "The client approved..."
- A scope change, timeline change, or budget change
- A tradeoff or direction that was formally resolved

**Not a RAID item:**
- "We should think about..." (no owner, no timeline → open question, not RAID)
- Complaints without blockers
- Status updates with no risk or decision attached

---

## Processing Actual RAID Log Files

When a RAID log file is dropped in `ingestion/raid-logs/`, treat it as the authoritative current state. See `processes/ingestion.md` for the step-by-step workflow.

**Key behaviors:**
- The dropped file replaces the previous version entirely — never merge/append
- Check `memory/raid-pending.md` and reconcile: archive items now reflected in the log, leave the rest pending
- Update `memory/raid-logs.md` with a current state snapshot for the project

**What to surface to the contact:**
- New critical or overdue items (create board cards)
- Pending items that are still missing from the log
- Items that changed status since the last version

---

## `memory/raid-logs.md` Structure

This file is a snapshot index — not a copy of the logs, just current status:

```
## [Project Name] — [YYYY-MM-DD last updated]
- **Open Risks:** N (X critical)
- **Open Actions:** N (X overdue)
- **Open Issues:** N
- **Pending Decisions:** N
- **Notes:** [Anything worth flagging at a glance]
```

Update this file every time a RAID log is ingested or a major change is confirmed.

---

## `memory/raid-pending.md` Structure

```
# RAID Pending — Proposed Changes

Items flagged for review. Apply to actual RAID logs, then confirm so I can archive.

---

## Pending

[Entries here]

---

## Archived

[Resolved entries — pruned periodically]
```
