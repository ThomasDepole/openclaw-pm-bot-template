# processes/ingestion.md — Ingestion Workflow
<!-- core process | do not customize here -->
<!-- workspace-specific config (naming corrections, tool paths, board IDs) belongs in memory/ -->

This file covers all ingestion workflows. Read it before processing any file from the `ingestion/` folder.

---

## Core Rules (All Ingestion Types)

1. **Cross-reference names** — before writing any project name, person name, or platform name to memory, check `memory/naming-conventions.md`. Transcription tools and voice notes introduce errors. If a name can't be matched with confidence, **flag it as an open question — do not assume**.
2. **Create board cards** — for every action item, decision, blocker, client follow-up, or materializing risk you find. See `processes/boards.md` for routing rules. This is not optional and does not require being asked.
3. **Delete source files** — the `ingestion/` folder is a drop zone, not an archive. Your `memory/` files are the record.
4. **Update the ingestion log** — add an entry to `memory/ingestion-log.md`: filename, date processed, one-line summary.

---

## Extracting Binary Files

Office files (`.docx`, `.xlsx`, `.pptx`, `.pdf`) are binary — you cannot `read` them directly. Use the extraction script:

```bash
python3 /home/node/.openclaw/scripts/extract-doc.py ingestion/<filename>
```

Supported formats: `.pdf`, `.docx`, `.xlsx` / `.xls`, `.pptx` / `.ppt`, `.csv`

Plain text (`.txt`, `.md`) — use the `read` tool directly.

**If you get a missing dependency error:**
```bash
pip3 install python-docx openpyxl python-pptx pdfplumber pandas --break-system-packages -q
```
Then retry.

---

## General Document Ingestion

Files dropped flat in `ingestion/` (not a subfolder).

**Steps:**
1. `ls ingestion/` — survey what you're working with
2. Read or extract each file
3. Cross-reference all names (see Core Rules)
4. Synthesize into categories:
   - Company overview (mission, services, structure, strategy)
   - Clients (names, context, active vs. past, key contacts)
   - Projects (status, stakeholders, timelines, risks, blockers)
   - People (team members, roles, relationships, notes)
   - Processes (workflows, standards, tools, decisions)
   - Open questions and gaps
5. Create board cards for anything actionable → `processes/boards.md`
6. Write to memory:
   - `memory/company.md` — company overview
   - `memory/clients.md` — client context
   - `memory/projects.md` — project tracking
   - `memory/people.md` — team and stakeholder notes
   - `memory/processes.md` — workflows and standards
   - `memory/open-questions.md` — unresolved items
7. Update `memory/ingestion-log.md`
8. Delete the source file
9. Report back — what you found, what stood out, open questions, cards created

---

## Meeting Notes

Meeting note files land in `ingestion/meetings/`. These may come from AI transcription tools, voice recorders, manual notes, or automated pipelines.

> **Transcription tools introduce errors.** Names, project names, and technical terms are frequently mis-transcribed. Always cross-reference against `memory/naming-conventions.md` before writing anything to memory.

**Steps:**
1. Read the note — identify date, attendees, and meeting context
2. Cross-reference every name and project reference → `memory/naming-conventions.md`
   - If a name can't be matched → flag as open question, do not guess
3. Check `memory/calendar.md` (if populated) to confirm the real meeting name and attendee list
4. Extract action items → create board cards immediately per `processes/boards.md`
5. Extract project updates → update `memory/projects.md`
6. Identify RAID items → flag to `memory/raid-pending.md` per `processes/raid.md`
7. Write meeting summary → `memory/meetings/YYYY-MM-DD-[meeting-name].md`
   - **5–10 bullets maximum.** Distill; do not transcribe.
   - Who attended | What was decided (not discussed — decided) | What is moving | What is blocked
8. Delete: `rm ingestion/meetings/<filename>`
9. Update ingestion log

**Good meeting summary:** answers what changed, what's next, what's stuck — in 5–10 bullets.
**Bad meeting summary:** a wall of notes nobody will read.

---

## Calendar / Schedule Files

Calendar screenshots or exports land in `ingestion/calendar/`.

**Steps:**
1. Read the file (images: use `read` tool; exports: extract or read directly)
2. Identify the date range
3. Extract: meeting names, dates, times, attendees, visible notes
4. Write to `memory/calendar.md`:
   - If the week already exists → **replace it** (don't append — schedules change)
   - If a new week → add it
5. Delete the source file
6. Update ingestion log

**Why this matters:** When processing meeting notes, check `memory/calendar.md` to match transcription-tool guesses against the real meeting name and attendees. Transcription tools frequently invent meeting names.

---

## Weekly Plans / Status Reports

Regular planning files (weekly plans, status reports, sprint summaries) land in `ingestion/weekly-plans/`.

**Steps:**
1. Read the file — identify the period it covers
2. Extract committed deliverables — what is promised to whom, by when
3. Extract action items — who owns what; check for duplicates against existing board cards
4. Cross-reference project names → `memory/naming-conventions.md`
5. Compare against what you already know — only surface what is **new or additive**
6. Create board cards:
   - Primary contact items → their primary board, New Tasks or equivalent
   - Team items → team board, under the owner's column
   - See `processes/boards.md` for routing
7. Flag RAID items → `memory/raid-pending.md` per `processes/raid.md`
8. Update project status in `memory/projects.md` if the file gives clearer status
9. Write summary → `memory/weekly-plans/YYYY-MM-DD.md` — period, key deliverables, what's new vs. already known
10. Delete the source file
11. Update ingestion log

**Focus on:** commitments with dates, client-facing items, things not already tracked
**Skip:** items with existing board cards, context that repeats what's already in memory

---

## RAID Log Files

Actual RAID log files land in `ingestion/raid-logs/`. Each dropped file is the **latest version** — treat it as authoritative. See `processes/raid.md` for the full RAID workflow.

**Steps:**
1. Extract the file (typically `.xlsx` or `.docx`)
2. Read `memory/raid-pending.md` — check for pending proposed items for this project
3. Compare pending items against the actual log:
   - Item now reflected correctly → archive it in `raid-pending.md`
   - Partially applied or status changed → update the pending entry
   - Still missing → leave in pending, flag to the primary contact
4. Create board cards for overdue actions, critical open risks, or items needing the contact's attention
5. Update `memory/raid-logs.md` — replace the previous entry for this project: open counts by type (R/A/I/D), critical/overdue items, last updated date
6. Delete the source file
7. Update ingestion log
8. Report back — pending items archived, what's still outstanding, anything notable, cards created

**Key rule:** Never merge or append — each dropped file replaces the previous version entirely.

---

## Workspace-Specific Configuration

The following are **not** in this file — they are user-configured in `memory/`:

| What | Where |
|------|-------|
| Project naming corrections (transcription errors, abbreviations) | `memory/naming-conventions.md` |
| Board IDs, list IDs, label IDs | `memory/boards/active/[board-name].md` |
| Known people, roles, and contact info | `memory/people.md` |
| Active clients and projects | `memory/clients.md`, `memory/projects.md` |
| Calendar (real meeting names vs. transcription guesses) | `memory/calendar.md` |
