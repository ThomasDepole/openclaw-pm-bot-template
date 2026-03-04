# Prompt: Create a RAID Log

Paste this into your PM bot to generate a blank RAID log file for a project.
Replace all `{{TOKENS}}` before sending.

---

## Tokens to fill in

| Token | What to put here | Example |
|-------|-----------------|---------|
| `{{PROJECT_NAME}}` | Full project name | `Acme Website Redesign` |
| `{{PROJECT_CODE}}` | Short code or ID (optional) | `ACME`, `PRJ-001` |
| `{{OWNER}}` | Who owns/manages this RAID log | `Sarah Chen`, `PM team` |

---

## The Prompt

```
Can you create a blank RAID log file for a project?

Project: {{PROJECT_NAME}}
Code: {{PROJECT_CODE}}
Owner: {{OWNER}}

Create the file at memory/raid-logs/{{PROJECT_CODE}}-raid-log.md (create the raid-logs/ folder if it doesn't exist).

The log should have four sections — Risks, Actions, Issues, Decisions — each with a table using these columns:

Risks: ID | Description | Likelihood (H/M/L) | Impact (H/M/L) | Owner | Mitigation | Status | Last Updated
Actions: ID | Description | Owner | Due Date | Status | Notes | Last Updated
Issues: ID | Description | Severity (H/M/L) | Owner | Resolution | Status | Last Updated
Decisions: ID | Description | Decision Made | Made By | Date | Rationale | Last Updated

Leave all tables empty (header rows only). Add a header with the project name, owner, and today's date. Let me know when it's done.
```

---

## After the bot creates it

The RAID log file will be at `memory/raid-logs/{{PROJECT_CODE}}-raid-log.md`. You can:
- Open and fill it in manually
- Tell the bot to add entries as they come up in meetings
- Ask the bot to surface items from `memory/raid-pending.md` into this log
