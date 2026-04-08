# HEARTBEAT.md

Periodic board checks. The agent runs these on every heartbeat poll.

## Setup

1. Complete board setup in `memory/boards/active/[board-name].md`
2. Replace all `YOUR_*` placeholders below with your actual IDs
3. Set your platform env vars (see `processes/boards.[platform].md`)
4. Delete this setup note when done

Find IDs using the discovery commands in `processes/boards.[platform].md`.

---

## Rhythm

| When | What |
|------|------|
| Monday morning (first run of week) | Monday Digest — full week picture |
| Every morning Tue–Fri (first run of day) | Morning Brief — priorities + overdue |
| Midday (first run after noon local time) | Midday Nudge — friendly check-in on open items |
| Every heartbeat | Quiet checks — alert only on new overdue or meaningful activity |

State is tracked in `memory/heartbeat-state.json`.

---

## Monday Digest

Run if: today is Monday AND `lastMondayDigest` is not today's date.

```bash
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Overdue cards on your primary board (not in Done list)
curl -s "https://api.trello.com/1/boards/YOUR_BOARD_ID/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,due,idList,closed" \
  | jq --arg now "$NOW" \
  '[.[] | select(.due != null and .closed == false and .idList != "YOUR_DONE_LIST_ID" and .due < $now)]'

# Cards completed last week
WEEK_AGO=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)
curl -s "https://api.trello.com/1/boards/YOUR_BOARD_ID/actions?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=updateCard&since=$WEEK_AGO&limit=50" \
  | jq '[.[] | select(.data.listAfter.id == "YOUR_DONE_LIST_ID")] | .[] | .data.card.name'
```

**Alert format:**
> 📅 **Monday Digest — week of [date]**
>
> **Last week: ✅ Done**
> - [card names]
>
> **Still overdue:**
> - 🔴 [card] — [N] days overdue (>1 week)
> - 🟠 [card] — [N] days overdue (3–7 days)
> - 🟡 [card] — [N] days overdue (1–2 days)
>
> **Suggested focus this week:**
> 1. [top priority — Urgent + oldest overdue first]
> 2. [second priority]
> 3. [third priority]

Update state: `lastMondayDigest = today's date`

---

## Morning Brief (Tue–Fri)

Run if: today is NOT Monday AND `lastMorningBrief` is not today's date.

Same overdue query as Monday Digest. Surface top 3 priorities.

**Alert format:**
> 🌅 **Morning Brief — [Day, Date]**
>
> **Overdue:**
> - 🔴 [card] — [N] days overdue
> - 🟠 [card] — [N] days overdue
>
> **Suggested focus today:**
> 1. [top priority]
> 2. [second priority]
> 3. [third priority]

Update state: `lastMorningBrief = today's date`

---

## Midday Nudge

Run if: `lastMiddayNudge` is not today AND current UTC hour >= 17 (≈ noon ET, adjust for your timezone).

Pull top 3–5 still-open overdue items. Keep it brief and warm.

**Alert format:**
> ☀️ **Midday check-in** — how's the day going?
>
> Still on the radar:
> - **[card name]** — overdue since [date]
> - **[card name]** — [brief context]
>
> Anything I can help move forward?

Update state: `lastMiddayNudge = today's date`

---

## Real-Time Check: New Overdue Cards

Run every heartbeat. Alert only when a card becomes **newly** overdue — not on every run.

```bash
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
curl -s "https://api.trello.com/1/boards/YOUR_BOARD_ID/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,due,idList,closed" \
  | jq --arg now "$NOW" \
  '[.[] | select(.due != null and .closed == false and .idList != "YOUR_DONE_LIST_ID" and .due < $now)] | map(.id)'
```

Compare result to `state.knownOverdueIds`. Alert only for IDs not already in that list.
Update `knownOverdueIds` to the full current list after every run.

**Alert format (only if new):**
> ⚠️ New overdue: **[card name]** — just went past due

Silent if nothing new.

---

## Real-Time Check: Board Activity

Run every heartbeat. Detect meaningful changes since `lastActionsCheck`.

```bash
curl -s "https://api.trello.com/1/boards/YOUR_BOARD_ID/actions?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=updateCard,commentCard,createCard&since=LAST_ACTIONS_CHECK_TIMESTAMP&limit=50" \
  | jq '.'
```

Surface only meaningful signals:

| Signal | How to detect |
|--------|--------------|
| Card moved to Done | `data.listAfter.id == "YOUR_DONE_LIST_ID"` |
| Card moved out of Done | `data.listBefore.id == "YOUR_DONE_LIST_ID"` |
| Card moved out of inbox/new | `data.listBefore.id == "YOUR_INBOX_LIST_ID"` |
| Due date changed | `data.old.due` exists |
| New card created | `createCard` action |

Skip label changes, minor edits, attachment adds.

**Alert format (if signals found):**
> 📋 Board activity:
> - ✅ **[Card name]** moved to Done
> - 📅 **[Card name]** due date changed → [new date]
> - ➕ New card: **[Card name]**

Silent if nothing meaningful. Update `lastActionsCheck` after every run.

---

## Done List Archive

Run once per day. Skip if `lastDoneArchiveCheck` is today.

```bash
curl -s "https://api.trello.com/1/lists/YOUR_DONE_LIST_ID/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,dateLastActivity" \
  | jq '.[]'
```

Track first-seen date in `state.doneCardsSeen`. Archive cards seen ≥7 days ago.

```bash
curl -s -X PUT "https://api.trello.com/1/cards/CARD_ID?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"
```

**Alert format (only if archived):**
> 🗂️ Archived [N] completed card(s) from Done (7 days old)

Update `lastDoneArchiveCheck` after running.

---

## State File

`memory/heartbeat-state.json` tracks run history and prevents duplicate alerts:

```json
{
  "lastActionsCheck": "2026-01-01T00:00:00Z",
  "lastMorningBrief": "2026-01-01",
  "lastMiddayNudge": "2026-01-01",
  "lastMondayDigest": "2026-01-01",
  "lastDoneArchiveCheck": "2026-01-01",
  "knownOverdueIds": [],
  "doneCardsSeen": {}
}
```

---

## Placeholder Reference

| Placeholder | What to replace with | Where to find it |
|-------------|---------------------|-----------------|
| `YOUR_BOARD_ID` | Your primary Trello board ID | `processes/boards.trello.md` discovery commands |
| `YOUR_DONE_LIST_ID` | The "Done" or "Complete" list ID | Same |
| `YOUR_INBOX_LIST_ID` | The "New Tasks" or inbox list ID | Same |

Store all IDs in `memory/boards/active/[board-name].md` for reference.

---

## Adapting for Other Platforms

This example uses Trello. For Notion or Planner:
- Replace curl commands with `tools/notion.sh` or `tools/planner.py` calls
- See `core/boards.notion.md` and `core/boards.planner.md` for equivalent queries
- The alert formats, rhythm, and state tracking logic stay the same regardless of platform
