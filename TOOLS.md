# TOOLS.md - Local Configuration Notes

This file is for your environment-specific setup. Fill it in as you configure integrations.

---

## Task Management Tool

**Tool:** [FILL IN: Trello / Jira / Azure DevOps / Linear / Asana / GitHub Issues / Monday.com / Other]

**Connection method:** [FILL IN: REST API / CLI / SDK]

**Base URL / Workspace:** [FILL IN: e.g. https://yourcompany.atlassian.net or trello.com/b/xxx]

**Credentials:** Stored in `.env` as `[FILL IN: env var names]`

**Board/Project IDs:** See `memory/boards/active/[board-name].md`

---

## Meeting Notes Ingestion

**Method:** [FILL IN: Manual drop / Plaud + Zapier + Dropbox / Other]

**Dropbox sync:** [FILL IN: Yes/No — if yes, see `docs/rclone-dropbox-setup.md`]

**Sync path:** [FILL IN: Dropbox folder → local ingestion path]

**Cron job:** [FILL IN: Crontab entry once configured]

---

## Other Integrations

### Slack / Teams
[FILL IN: Webhook URLs or access method if configured]

### GitHub / GitLab
[FILL IN: Repo URLs, access tokens, org names]

### Calendar
[FILL IN: How you share calendar context — screenshots, ICS exports, Google Calendar API, etc.]

### Communication / Email
[FILL IN: If email integration is configured]

---

## Notes

[FILL IN: Any environment-specific quirks, shortcuts, or reminders]
