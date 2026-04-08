# tools/ — Platform Helper Scripts

Runnable scripts for the agent to call via `exec`. These handle authentication
and CRUD for board platforms that require more than a simple API key.

---

## What's Here

| Script | Platform | Language | Auth |
|--------|----------|----------|------|
| `notion.sh` | Notion | Shell (curl) | Integration token (env var) |
| `planner.py` | Microsoft Planner | Python 3 | OAuth 2.0 client credentials |

---

## Notion Setup

1. Go to [https://www.notion.so/profile/integrations](https://www.notion.so/profile/integrations)
2. Create a new **Internal Integration**
3. Copy the **Internal Integration Secret** (starts with `ntn_` or `secret_`)
4. Share each Notion database you want the bot to access with the integration
   (open the database → ... → Connect to → your integration name)
5. Set the environment variable:

```bash
export NOTION_TOKEN="ntn_your_token_here"
```

To find a database ID: open the database in Notion → copy the URL.
The ID is the 32-character hex string before the `?` (with or without dashes).

---

## Microsoft Planner Setup

Requires an **Azure/Entra ID app registration**. Your IT admin needs to do this once.

1. Go to [https://entra.microsoft.com](https://entra.microsoft.com) → App registrations → New registration
2. Name it (e.g. "PM Bot"), select **Single tenant**, register
3. Note the **Application (client) ID** and **Directory (tenant) ID**
4. Under **Certificates & secrets** → New client secret → copy the value immediately
5. Under **API permissions** → Add a permission → Microsoft Graph → Application permissions
   → Add `Tasks.ReadWrite.All` → Grant admin consent
6. To find your Group ID: go to [https://entra.microsoft.com](https://entra.microsoft.com) → Groups → your group → copy Object ID
7. To find your Plan ID: run `python3 tools/planner.py list-plans --group-id YOUR_GROUP_ID`

Set environment variables:

```bash
export PLANNER_TENANT_ID="your-tenant-id"
export PLANNER_CLIENT_ID="your-client-id"
export PLANNER_CLIENT_SECRET="your-client-secret"
```

> ⚠️ **Premium Planner is not accessible via the API.** Only Basic Planner plans/tasks
> work with Microsoft Graph. If your org is on Premium Planner, this script will return
> empty results or 403 errors — there is no workaround at this time.

---

## Usage (agent)

The agent calls these scripts via `exec`. Example patterns:

```bash
# Notion — list tasks in a database
bash tools/notion.sh list-tasks DATABASE_ID

# Notion — create a task
bash tools/notion.sh create-task DATABASE_ID "Task name" "2026-04-15"

# Planner — list all plans in a group
python3 tools/planner.py list-plans --group-id GROUP_ID

# Planner — list tasks in a plan
python3 tools/planner.py list-tasks --plan-id PLAN_ID

# Planner — create a task
python3 tools/planner.py create-task --plan-id PLAN_ID --title "Task name" --due 2026-04-15 --bucket-id BUCKET_ID
```

Output is always JSON to stdout. Errors go to stderr with a non-zero exit code.
