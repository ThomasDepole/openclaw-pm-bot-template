# memory/naming-conventions.md — Naming Conventions

This file is used during ingestion to correct transcription errors and resolve ambiguous names.
The ingestion process checks every project name, person name, and platform name against this file before writing to memory.

---

## How to Use This File

Add entries in the format:

```
[Incorrect / ambiguous version] → [Canonical name]
```

When processing meeting notes or transcriptions, if a name matches something on the left, always use the canonical name on the right.

If a name appears that is not in this file and cannot be confidently matched to a known project, person, or platform — flag it as an open question. Do not guess.

---

## Projects

<!-- Add your project name corrections here. Examples: -->
<!-- Mis-transcribed → Canonical project name -->

---

## Platforms & Tools

<!-- Add platform name corrections here. Examples: -->
<!-- Mis-transcribed → Canonical platform name -->

---

## People

<!-- Add name corrections here. Examples: -->
<!-- Mis-transcribed → Full canonical name -->

---

## Clients / Organizations

<!-- Add client name corrections here. Examples: -->
<!-- Mis-transcribed → Canonical client name -->

---

## Notes

- This file is workspace-specific — it does not ship pre-populated in the template
- Update it whenever you discover a new transcription error pattern
- If your meeting note tool consistently mis-transcribes a name, add it here permanently
