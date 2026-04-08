# boards.planner.md — Microsoft Planner Platform Adapter

Read `processes/boards.md` for the generic board interface this adapter implements.

---

## How Planner Structures Work

Microsoft Planner is accessed via the **Microsoft Graph API**. Plans belong to
Microsoft 365 Groups (Teams channels, SharePoint groups, etc.).

| Planner concept | Board equivalent |
|-----------------|-----------------|
| Plan | Board |
| Bucket | List / column |
| Task | Card |
| Assignment | Assignee |
| % Complete (0–100) | Status / progress |

There are no custom status labels. Completion is tracked by `percentComplete` (0–100).
Convention: 0 = Not Started, 50 = In Progress, 100 = Complete.

> ⚠️ **Premium Planner only (the upgraded paid version)** is NOT accessible via the
> Microsoft Graph API. Only **Basic Planner** works. If your org upgraded to Premium
> Planner, this adapter will not function. There is no workaround.

---

## Authentication

Planner requires **Azure/Entra ID app registration** — there is no simple API key.
See `tools/README.md` for the full setup walkthrough.

- **Auth type:** OAuth 2.0 Client Credentials (app-only, no user sign-in required)
- **Required env vars:** `PLANNER_TENANT_ID`, `PLANNER_CLIENT_ID`, `PLANNER_CLIENT_SECRET`
- **Required Graph permission:** `Tasks.ReadWrite.All` (Application permission, admin consent required)
- **Token endpoint:** `https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token`
- **Token lifetime:** ~1 hour. `tools/planner.py` caches the token automatically.

---

## Key IDs

IDs you'll need:

| What | Where to find it |
|------|-----------------|
| Tenant ID | Azure Portal → Entra ID → Overview → Tenant ID |
| Client ID | Azure Portal → App registrations → your app → Application (client) ID |
| Group ID | Azure Portal → Groups → your group → Object ID |
| Plan ID | Run `python3 tools/planner.py list-plans --group-id GROUP_ID` |
| Bucket ID | Run `python3 tools/planner.py list-buckets --plan-id PLAN_ID` |
| User ID | Run `python3 tools/planner.py list-members --group-id GROUP_ID` |

Store Plan IDs, Bucket IDs, and Group IDs in `memory/boards/active/[board-name].md`.

---

## Script Reference

All operations via `tools/planner.py`. See that file for full argument docs.
Requires `requests`: `pip install requests`

### Find plans and buckets (run once during setup)
```bash
python3 tools/planner.py list-plans   --group-id GROUP_ID
python3 tools/planner.py list-buckets --plan-id PLAN_ID
python3 tools/planner.py list-members --group-id GROUP_ID
```

### List tasks in a plan
```bash
python3 tools/planner.py list-tasks --plan-id PLAN_ID
python3 tools/planner.py list-tasks --plan-id PLAN_ID --bucket-id BUCKET_ID
```
Returns: `[{id, title, percentComplete, dueDateTime, bucketId, assignees}]`

### Get a specific task
```bash
python3 tools/planner.py get-task --task-id TASK_ID
```

### Create a task
```bash
python3 tools/planner.py create-task --plan-id PLAN_ID --title "Task title"
python3 tools/planner.py create-task --plan-id PLAN_ID --title "Task title" \
  --due 2026-04-15 --bucket-id BUCKET_ID --assignee USER_ID
```
Returns: `{id, title, planId}`

### Update a task
```bash
python3 tools/planner.py update-task --task-id TASK_ID --title "New title"
python3 tools/planner.py update-task --task-id TASK_ID --due 2026-04-20
python3 tools/planner.py update-task --task-id TASK_ID --percent 50
```
Multiple flags can be combined. The ETag is fetched automatically.

### Complete a task
```bash
python3 tools/planner.py complete-task --task-id TASK_ID
```
Sets `percentComplete` to 100.

---

## Raw curl (for one-offs)

You need a Bearer token first. Get one by calling the token endpoint or running:
```bash
python3 -c "
import tools.planner as p; import json
token = p.get_token()
print(token[:40] + '...')
"
```
Or set `TOKEN=$(python3 -c "from tools.planner import get_token; print(get_token())")`.

### List tasks in a plan
```bash
curl -s -X GET "https://graph.microsoft.com/v1.0/planner/plans/$PLAN_ID/tasks" \
  -H "Authorization: Bearer $TOKEN"
```

### Create a task
```bash
curl -s -X POST "https://graph.microsoft.com/v1.0/planner/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data "{
    \"planId\": \"$PLAN_ID\",
    \"bucketId\": \"$BUCKET_ID\",
    \"title\": \"Task title\",
    \"dueDateTime\": \"2026-04-15T17:00:00Z\"
  }"
```

### Update a task (requires ETag)
```bash
# 1. Get the ETag
ETAG=$(curl -s -I "https://graph.microsoft.com/v1.0/planner/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | grep -i etag | tr -d '\r' | awk '{print $2}')

# 2. PATCH with If-Match
curl -s -X PATCH "https://graph.microsoft.com/v1.0/planner/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "If-Match: $ETAG" \
  --data '{"percentComplete": 100}'
```

> ⚠️ **ETag is mandatory for all PATCH requests.** Planner will return 412 Precondition Failed
> without it. Always GET the task first to retrieve the current ETag.

---

## Limitations

- No custom status labels — only `percentComplete` (0–100)
- Buckets (columns) must be created in the Planner UI or via API before tasks can be assigned to them
- The app registration needs `Tasks.ReadWrite.All` with **admin consent** — a regular user cannot grant this
- Tokens expire in ~1 hour; `planner.py` handles refresh automatically via `/tmp/.planner_token_cache`
- Personal Microsoft accounts are not supported — requires work/school (M365) account
