# processes/ingestion.md — Ingestion Customizations
<!-- user layer | read core/ingestion.md first, then add your overrides below -->

> **Read `core/ingestion.md` first.** All ingestion workflows, file type handling, and RAID pending steps are there.

---

## Meeting Note Tool

<!-- Specify what tool generates your meeting notes (Plaud, Otter, manual, etc.) -->
<!-- and any known transcription quirks or error patterns for this deployment. -->

**Tool:** [FILL IN — e.g. Plaud, Otter.ai, manual notes]

**Known transcription errors for this deployment:**
<!-- Add entries to memory/naming-conventions.md, not here. -->
<!-- Note here if there are systematic patterns the agent should always watch for. -->
<!-- e.g. "This tool consistently mishears technical product names — always cross-check" -->

---

## Custom Ingestion Sources

<!-- Document any ingestion sources beyond the standard subfolders. -->
<!-- e.g. "RAID logs come in as .xlsx in ingestion/raid-logs/" -->
<!-- e.g. "Client briefs land in ingestion/clients/ as PDFs" -->
<!-- e.g. "Weekly plans are written inline by the contact, not dropped as files" -->

---

## Ingestion Subfolder Notes

<!-- Any subfolder-specific rules for this deployment go here. -->
<!-- Leave empty if the core workflow applies without changes. -->
