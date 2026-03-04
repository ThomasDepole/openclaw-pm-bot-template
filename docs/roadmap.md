# Roadmap

Planned improvements and ideas for future versions of the OpenClaw PM Bot template.

This is a living document — not a commitment, not a timeline. Just the direction of travel.

---

## v1.1 — Update Prompt System

**The problem:** Traditional git-based updates don't work for workspace templates. Every deployment is customized — `SOUL.md`, `AGENTS.md`, `USER.md`, and memory files all diverge from the template on day one, intentionally. Git merges create conflicts in exactly the files that matter most.

**The solution:** Update prompts — structured markdown files shipped with each release that the bot applies intelligently to its own workspace.

### How it will work

1. A new template version ships with an `updates/vX.X.X-update.md` file in the release assets
2. The user downloads it and drops it into their `updates/` folder
3. The bot reads it and knows:
   - What changed in this version
   - Which changes are safe to apply automatically (new docs, structural additions)
   - Which changes need human review before applying (AGENTS.md behavior, new conventions)
   - Which files to never touch (personalized files, memory)
4. Bot applies what it can, surfaces the rest for the user
5. Bot deletes the update file and logs what was applied

### Why this works

The bot is the right tool for applying updates to itself. It understands which files it has personalized, what the user cares about, and how to interpret natural language instructions. A diff file can't do that. A merge conflict can't do that.

### What update prompts look like (rough sketch)

```markdown
# v1.1.0 Update Prompt

## What changed
- New: `docs/update-guide.md` — explains the update prompt system
- Changed: AGENTS.md — new section on template update handling
- New: `ingestion/status-reports/` subfolder
- Fixed: ingestion README typos

## Safe to apply automatically
- Add `docs/update-guide.md` if it doesn't exist
- Add `ingestion/status-reports/` subfolder and README if missing

## Review with your human before applying
- AGENTS.md has a new "Template Updates" section — review and merge manually
  (don't overwrite — your AGENTS.md is customized)

## Do not apply
- SOUL.md, USER.md, IDENTITY.md, memory/* — these are yours
```

---

## v1.2 — Passive Update Notifications

The bot periodically checks the upstream template repo for new releases via the GitHub API and proactively tells the user when a new version is available.

- Low effort, zero risk
- User decides whether to apply the update
- Pairs naturally with the update prompt system

---

## Future Ideas

**Multi-project mode improvements**
Better separation between project-specific and company-wide context as memory grows. Currently everything lives in flat files — larger deployments may benefit from per-project subfolders.

**Dedicated bot account for template contributions**
Separate GitHub identity for AI-authored PRs, enabling proper review workflows without the "you approved your own PR" awkwardness.

**Heartbeat templates**
Pre-built heartbeat configurations for common PM workflows (sprint cadence, status report days, deadline tracking) that users can drop into `HEARTBEAT.md` without having to write from scratch.

**Onboarding wizard improvements**
`BOOTSTRAP.md` currently runs as a free-form conversation. A more structured wizard could pre-populate more memory files from the answers, reducing time-to-useful-context.

---

## Contributing

Ideas welcome — open an issue or PR on the [template repo](https://github.com/ThomasDepole/openclaw-pm-bot-template).
