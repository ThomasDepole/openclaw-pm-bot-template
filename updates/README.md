# Updates

This folder is where template updates are applied.

---

## For Bots: Read This First

If you find a file in this folder (e.g. `v1.1.0-update.md`), that is an **update prompt**. It contains instructions from the template maintainer describing what changed in a new version and how to apply those changes to your workspace.

**When you find an update file here:**

1. Read it fully before doing anything
2. Follow its instructions — it will tell you what to apply automatically, what to review with your human first, and what to skip if you've customized those files
3. When done, delete the update file and log what was applied in your daily memory file
4. Let your human know what changed

Update prompts are designed to be applied intelligently — they are not blind overwrites. Your customizations (SOUL.md, AGENTS.md, USER.md, memory files) are preserved unless the prompt explicitly tells you otherwise and you've confirmed with your human.

---

## For Users: How to Apply Updates

When a new version of this template is released:

1. Check the [releases page](https://github.com/ThomasDepole/openclaw-pm-bot-template/releases) for update prompts
2. Download the `vX.X.X-update.md` file from the release assets
3. Drop it into this folder (`updates/`)
4. Tell your bot: *"There's an update prompt in the updates folder — can you apply it?"*
5. Review what the bot did and confirm

That's it. No git merges, no conflicts, no overwriting your customizations.

---

## Why This Folder Exists

Traditional git-based updates don't work well for workspace templates because every deployment is customized. Your `SOUL.md`, `AGENTS.md`, and memory files are yours — they've diverged from the template on day one, intentionally.

Update prompts solve this by letting the bot apply changes intelligently, the same way you'd brief a team member on what changed rather than handing them a diff file.

This system is planned for v1.1. The folder exists now so every deployed bot knows to check it.

---

## Update File Naming Convention

```
updates/
└── v1.1.0-update.md    ← drop update prompts here
```

Files should be named `vX.X.X-update.md`. The bot will process and delete them after applying.
