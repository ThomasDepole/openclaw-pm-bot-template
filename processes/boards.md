# processes/boards.md — Board Customizations
<!-- user layer | read core/boards.md first, then add your customizations below -->

> **Read `core/boards.md` first.** All generic board concepts, card naming, routing patterns, and platform adapter references are there.

---

## Active Platform

<!-- Specify which platform adapter to load for this workspace. -->
<!-- e.g. "This workspace uses Trello — load processes/boards.trello.md" -->

**Active platform:** [FILL IN — Trello / Notion / Planner / Jira]

---

## Custom Routing Rules

<!-- Add any routing overrides specific to your deployment. -->
<!-- e.g. "All client-facing cards get the 'External' label" -->
<!-- e.g. "Cards for the design team go to the Design board, not the team board" -->
<!-- Leave empty if core/boards.md routing works as-is. -->

---

## Board Config

Board IDs, list IDs, and label IDs live in `memory/boards/active/[board-name].md`, not here.
See `processes/boards.[platform].md` for the platform adapter.
