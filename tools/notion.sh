#!/usr/bin/env bash
# notion.sh — Notion API helper for PM bot agents
#
# Requires: curl, jq (or the bundled jq at $JQ_PATH)
# Auth:     NOTION_TOKEN env var (Internal Integration Secret)
#
# Usage:
#   bash tools/notion.sh list-tasks   DATABASE_ID
#   bash tools/notion.sh create-task  DATABASE_ID "Title" [YYYY-MM-DD] [assignee_id]
#   bash tools/notion.sh update-task  PAGE_ID status ["New Title"] [YYYY-MM-DD]
#   bash tools/notion.sh complete-task PAGE_ID
#   bash tools/notion.sh archive-task  PAGE_ID
#   bash tools/notion.sh get-task      PAGE_ID
#   bash tools/notion.sh list-databases
#
# Status values are whatever your database's Status property uses.
# Inspect with: bash tools/notion.sh get-task PAGE_ID | jq '.properties.Status'
#
# Output: JSON to stdout. Errors to stderr + exit 1.

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────

NOTION_API="https://api.notion.com/v1"
NOTION_VERSION="2022-06-28"
TOKEN="${NOTION_TOKEN:?NOTION_TOKEN env var is not set}"
JQ="${JQ_PATH:-jq}"

# ── Helpers ───────────────────────────────────────────────────────────────────

_notion() {
  local method="$1"; shift
  local path="$1";   shift
  local data="${1:-}"

  local args=(-s -X "$method"
    -H "Authorization: Bearer $TOKEN"
    -H "Notion-Version: $NOTION_VERSION"
    -H "Content-Type: application/json"
  )

  if [[ -n "$data" ]]; then
    args+=(--data "$data")
  fi

  local response
  response=$(curl "${args[@]}" "${NOTION_API}${path}")

  # Surface API errors
  local status
  status=$(echo "$response" | $JQ -r '.status // empty')
  if [[ -n "$status" && "$status" != "200" ]]; then
    echo "$response" >&2
    exit 1
  fi

  echo "$response"
}

# ── Commands ──────────────────────────────────────────────────────────────────

cmd_list_tasks() {
  local db_id="${1:?Usage: list-tasks DATABASE_ID}"

  _notion POST "/databases/${db_id}/query" '{
    "sorts": [{ "property": "Due Date", "direction": "ascending" }],
    "filter": {
      "property": "Status",
      "select": { "does_not_equal": "Done" }
    }
  }' | $JQ '[.results[] | {
    id:     .id,
    title:  (.properties.Name.title[0].plain_text // "(untitled)"),
    status: (.properties.Status.select.name // null),
    due:    (.properties["Due Date"].date.start // null),
    done:   .archived
  }]'
}

cmd_get_task() {
  local page_id="${1:?Usage: get-task PAGE_ID}"
  _notion GET "/pages/${page_id}"
}

cmd_create_task() {
  local db_id="${1:?Usage: create-task DATABASE_ID TITLE [DUE_DATE] [ASSIGNEE_ID]}"
  local title="${2:?Title required}"
  local due="${3:-}"
  local assignee="${4:-}"

  # Build properties JSON
  local props
  props=$(printf '{"Name":{"title":[{"text":{"content":"%s"}}]}}' "$title")

  if [[ -n "$due" ]]; then
    props=$(echo "$props" | $JQ --arg d "$due" \
      '.["Due Date"] = {"date": {"start": $d}}')
  fi

  if [[ -n "$assignee" ]]; then
    props=$(echo "$props" | $JQ --arg uid "$assignee" \
      '.Assignee = {"people": [{"id": $uid}]}')
  fi

  local body
  body=$(jq -n \
    --argjson props "$props" \
    --arg db "$db_id" \
    '{"parent":{"database_id":$db},"properties":$props}')

  _notion POST "/pages" "$body" | $JQ '{
    id:     .id,
    title:  (.properties.Name.title[0].plain_text // "(untitled)"),
    url:    .url
  }'
}

cmd_update_task() {
  local page_id="${1:?Usage: update-task PAGE_ID STATUS [TITLE] [DUE_DATE]}"
  local status="${2:?Status required}"
  local title="${3:-}"
  local due="${4:-}"

  local props
  props=$(printf '{"Status":{"select":{"name":"%s"}}}' "$status")

  if [[ -n "$title" ]]; then
    props=$(echo "$props" | $JQ --arg t "$title" \
      '.Name = {"title": [{"text": {"content": $t}}]}')
  fi

  if [[ -n "$due" ]]; then
    props=$(echo "$props" | $JQ --arg d "$due" \
      '.["Due Date"] = {"date": {"start": $d}}')
  fi

  local body
  body=$(jq -n --argjson props "$props" '{"properties":$props}')

  _notion PATCH "/pages/${page_id}" "$body" | $JQ '{
    id:     .id,
    title:  (.properties.Name.title[0].plain_text // "(untitled)"),
    status: (.properties.Status.select.name // null)
  }'
}

cmd_complete_task() {
  local page_id="${1:?Usage: complete-task PAGE_ID}"
  cmd_update_task "$page_id" "Done"
}

cmd_archive_task() {
  local page_id="${1:?Usage: archive-task PAGE_ID}"
  _notion PATCH "/pages/${page_id}" '{"archived":true}' | $JQ '{id:.id, archived:.archived}'
}

cmd_list_databases() {
  _notion POST "/search" '{"filter":{"value":"database","property":"object"}}' \
    | $JQ '[.results[] | {id:.id, title:(.title[0].plain_text // "(untitled)")}]'
}

# ── Dispatch ──────────────────────────────────────────────────────────────────

COMMAND="${1:-}"
shift || true

case "$COMMAND" in
  list-tasks)      cmd_list_tasks "$@" ;;
  get-task)        cmd_get_task "$@" ;;
  create-task)     cmd_create_task "$@" ;;
  update-task)     cmd_update_task "$@" ;;
  complete-task)   cmd_complete_task "$@" ;;
  archive-task)    cmd_archive_task "$@" ;;
  list-databases)  cmd_list_databases "$@" ;;
  *)
    echo "Usage: notion.sh <command> [args]" >&2
    echo "Commands: list-tasks, get-task, create-task, update-task, complete-task, archive-task, list-databases" >&2
    exit 1
    ;;
esac
