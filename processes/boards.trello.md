# processes/boards.trello.md — Trello Platform Adapter
<!-- platform-specific | read alongside processes/boards.md -->

Trello-specific commands and mechanics. Always read `processes/boards.md` first for generic concepts and routing rules. Board configs (IDs, lists, labels) are in `memory/boards/active/`.

---

## Credentials & Setup

```bash
# Required env vars:
# TRELLO_API_KEY  — from https://trello.com/power-ups/admin
# TRELLO_TOKEN    — from https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&key=YOUR_KEY

JQ="${JQ_PATH:-jq}"  # set JQ_PATH if using a bundled jq binary
```

**Rate limits:** 300 req/10s per API key, 100 req/10s per token.

**Finding IDs:**
- Board ID: open board in Trello → `.json` at end of URL, or use list-boards below
- List/label IDs: see list-board-details below

---

## Discover Boards and IDs

### List all accessible boards
```bash
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=id,name" \
  | $JQ '.[] | {id, name}'
```

### Get lists and labels for a board
```bash
curl -s "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&lists=all&labels=all&fields=name" \
  | $JQ '{lists: [.lists[] | {id, name}], labels: [.labels[] | {id, name, color}]}'
```

Store the IDs you need in `memory/boards/active/[board-name].md`.

---

## Create a Card

```bash
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={listId}" \
  -d "name=Card Title" \
  -d "desc=Context and source"
```

With a due date:
```bash
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={listId}" \
  -d "name=Card Title" \
  -d "desc=Context" \
  -d "due=2026-04-15T17:00:00.000Z"
```

Returns the created card object. Save the `id` if you need to add labels, comments, etc. in follow-up calls.

---

## Add a Label to a Card

```bash
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/idLabels?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "value={labelId}"
```

---

## Move a Card (Change List)

```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={newListId}"
```

---

## Add a Comment to a Card

```bash
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "text=Your comment here"
```

---

## Update a Card (title, due date, description)

```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=New Title" \
  -d "due=2026-04-20T17:00:00.000Z" \
  -d "desc=Updated description"
```

---

## Archive a Card

```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"
```

---

## List Cards in a List

```bash
curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,due,idLabels,dateLastActivity" \
  | $JQ '.[]'
```

---

## List Overdue Cards on a Board

```bash
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,due,idList,closed" \
  | $JQ --arg now "$NOW" \
  '[.[] | select(.due != null and .closed == false and .due < $now)]'
```

---

## Get Recent Board Activity

```bash
curl -s "https://api.trello.com/1/boards/{boardId}/actions?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=updateCard,commentCard,createCard&since={ISO_TIMESTAMP}&limit=50" \
  | $JQ '.'
```

---

## Add Checklist to a Card

```bash
# Create checklist
CHECKLIST_ID=$(curl -s -X POST "https://api.trello.com/1/checklists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idCard={cardId}" \
  -d "name=Action Items" \
  | $JQ -r '.id')

# Add items
curl -s -X POST "https://api.trello.com/1/checklists/$CHECKLIST_ID/checkItems?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=First item"
curl -s -X POST "https://api.trello.com/1/checklists/$CHECKLIST_ID/checkItems?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Second item"
```

---

## Stacy Integration (optional)

If using a second agent (like Stacy) to route card creation requests to this bot, see the board config in `memory/boards/active/` for the target list and workflow details. The pattern:

1. Stacy receives request → spawns PM bot with task details
2. PM bot creates card on the configured list
3. PM bot confirms back (Discord message or card comment)

This pattern is optional — configure only if you have a multi-agent setup. See `AGENTS.md` for isolation rules.
