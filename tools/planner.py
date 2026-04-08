#!/usr/bin/env python3
"""
planner.py — Microsoft Planner (Graph API) helper for PM bot agents

Requires: Python 3.8+, requests library (pip install requests)
Auth:     Three env vars (see README.md for setup):
            PLANNER_TENANT_ID
            PLANNER_CLIENT_ID
            PLANNER_CLIENT_SECRET

Usage:
    python3 tools/planner.py list-plans   --group-id GROUP_ID
    python3 tools/planner.py list-buckets --plan-id PLAN_ID
    python3 tools/planner.py list-tasks   --plan-id PLAN_ID [--bucket-id BUCKET_ID]
    python3 tools/planner.py get-task     --task-id TASK_ID
    python3 tools/planner.py create-task  --plan-id PLAN_ID --title "..." [--due YYYY-MM-DD] [--bucket-id BUCKET_ID] [--assignee USER_ID]
    python3 tools/planner.py update-task  --task-id TASK_ID [--title "..."] [--due YYYY-MM-DD] [--percent N]
    python3 tools/planner.py complete-task --task-id TASK_ID
    python3 tools/planner.py list-members --group-id GROUP_ID

Output: JSON to stdout. Errors to stderr + exit 1.

NOTES:
  - Only Basic Planner plans are accessible. Premium Planner is blocked by Microsoft.
  - Updating a task requires an ETag (fetched automatically — handled here).
  - Tokens are cached in /tmp/.planner_token_cache for the duration of their validity.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests library not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
TOKEN_URL_TMPL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
TOKEN_CACHE = Path("/tmp/.planner_token_cache")

TENANT_ID     = os.environ.get("PLANNER_TENANT_ID")
CLIENT_ID     = os.environ.get("PLANNER_CLIENT_ID")
CLIENT_SECRET = os.environ.get("PLANNER_CLIENT_SECRET")


# ── Auth ──────────────────────────────────────────────────────────────────────

def get_token() -> str:
    """Get a valid access token, using cache if possible."""
    if TOKEN_CACHE.exists():
        cached = json.loads(TOKEN_CACHE.read_text())
        if cached.get("expires_at", 0) > time.time() + 60:
            return cached["access_token"]

    for var, name in [(TENANT_ID, "PLANNER_TENANT_ID"),
                      (CLIENT_ID, "PLANNER_CLIENT_ID"),
                      (CLIENT_SECRET, "PLANNER_CLIENT_SECRET")]:
        if not var:
            die(f"Environment variable {name} is not set. See tools/README.md.")

    resp = requests.post(
        TOKEN_URL_TMPL.format(tenant=TENANT_ID),
        data={
            "grant_type":    "client_credentials",
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope":         "https://graph.microsoft.com/.default",
        },
    )
    resp.raise_for_status()
    data = resp.json()

    if "access_token" not in data:
        die(f"Token request failed: {json.dumps(data)}")

    data["expires_at"] = time.time() + data.get("expires_in", 3600)
    TOKEN_CACHE.write_text(json.dumps(data))
    TOKEN_CACHE.chmod(0o600)

    return data["access_token"]


def headers(extra: dict | None = None) -> dict:
    h = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type":  "application/json",
    }
    if extra:
        h.update(extra)
    return h


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def graph_get(path: str) -> requests.Response:
    r = requests.get(f"{GRAPH_BASE}{path}", headers=headers())
    check(r)
    return r


def graph_post(path: str, body: dict) -> dict:
    r = requests.post(f"{GRAPH_BASE}{path}", headers=headers(), json=body)
    check(r)
    return r.json()


def graph_patch(path: str, body: dict, etag: str) -> dict:
    """PATCH requires If-Match ETag header — Planner will 412 without it."""
    r = requests.patch(
        f"{GRAPH_BASE}{path}",
        headers=headers({"If-Match": etag}),
        json=body,
    )
    check(r)
    # 204 No Content on success
    return {"status": "updated"} if r.status_code == 204 else r.json()


def get_etag(path: str) -> tuple[dict, str]:
    """Fetch a resource and return (body, etag). Required before PATCH."""
    r = graph_get(path)
    etag = r.headers.get("ETag", "")
    if not etag:
        die(f"No ETag returned for {path} — cannot update.")
    return r.json(), etag


def check(r: requests.Response):
    if not r.ok:
        try:
            err = r.json()
        except Exception:
            err = r.text
        die(f"Graph API error {r.status_code}: {json.dumps(err)}")


def die(msg: str):
    print(msg, file=sys.stderr)
    sys.exit(1)


def out(data):
    print(json.dumps(data, indent=2))


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_list_plans(args):
    gid = args.group_id or die("--group-id required")
    data = graph_get(f"/groups/{gid}/planner/plans").json()
    out([{"id": p["id"], "title": p["title"]} for p in data.get("value", [])])


def cmd_list_buckets(args):
    pid = args.plan_id or die("--plan-id required")
    data = graph_get(f"/planner/plans/{pid}/buckets").json()
    out([{"id": b["id"], "name": b["name"], "orderHint": b.get("orderHint")}
         for b in data.get("value", [])])


def cmd_list_tasks(args):
    pid = args.plan_id or die("--plan-id required")
    data = graph_get(f"/planner/plans/{pid}/tasks").json()
    tasks = data.get("value", [])
    if args.bucket_id:
        tasks = [t for t in tasks if t.get("bucketId") == args.bucket_id]
    out([{
        "id":              t["id"],
        "title":           t.get("title"),
        "percentComplete": t.get("percentComplete", 0),
        "dueDateTime":     t.get("dueDateTime"),
        "bucketId":        t.get("bucketId"),
        "assignees":       list(t.get("assignments", {}).keys()),
    } for t in tasks])


def cmd_get_task(args):
    tid = args.task_id or die("--task-id required")
    out(graph_get(f"/planner/tasks/{tid}").json())


def cmd_create_task(args):
    pid = args.plan_id or die("--plan-id required")
    title = args.title or die("--title required")

    body: dict = {"planId": pid, "title": title}

    if args.bucket_id:
        body["bucketId"] = args.bucket_id

    if args.due:
        # Graph expects ISO 8601 with time component
        body["dueDateTime"] = f"{args.due}T17:00:00Z"

    if args.assignee:
        body["assignments"] = {
            args.assignee: {
                "@odata.type": "microsoft.graph.plannerAssignment",
                "orderHint":   " !",
            }
        }

    result = graph_post("/planner/tasks", body)
    out({"id": result["id"], "title": result.get("title"), "planId": result.get("planId")})


def cmd_update_task(args):
    tid = args.task_id or die("--task-id required")
    task, etag = get_etag(f"/planner/tasks/{tid}")

    body: dict = {}

    if args.title:
        body["title"] = args.title
    if args.due:
        body["dueDateTime"] = f"{args.due}T17:00:00Z"
    if args.percent is not None:
        body["percentComplete"] = int(args.percent)

    if not body:
        die("Nothing to update — provide at least one of: --title, --due, --percent")

    out(graph_patch(f"/planner/tasks/{tid}", body, etag))


def cmd_complete_task(args):
    tid = args.task_id or die("--task-id required")
    _, etag = get_etag(f"/planner/tasks/{tid}")
    out(graph_patch(f"/planner/tasks/{tid}", {"percentComplete": 100}, etag))


def cmd_list_members(args):
    gid = args.group_id or die("--group-id required")
    data = graph_get(f"/groups/{gid}/members").json()
    out([{
        "id":          m["id"],
        "displayName": m.get("displayName"),
        "mail":        m.get("mail"),
    } for m in data.get("value", [])])


# ── CLI ───────────────────────────────────────────────────────────────────────

COMMANDS = {
    "list-plans":    cmd_list_plans,
    "list-buckets":  cmd_list_buckets,
    "list-tasks":    cmd_list_tasks,
    "get-task":      cmd_get_task,
    "create-task":   cmd_create_task,
    "update-task":   cmd_update_task,
    "complete-task": cmd_complete_task,
    "list-members":  cmd_list_members,
}

parser = argparse.ArgumentParser(
    description="Microsoft Planner helper for PM bot agents",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("command", choices=COMMANDS.keys())
parser.add_argument("--group-id",   help="Microsoft 365 Group ID")
parser.add_argument("--plan-id",    help="Planner Plan ID")
parser.add_argument("--bucket-id",  help="Bucket ID (column/list in Planner)")
parser.add_argument("--task-id",    help="Task ID")
parser.add_argument("--title",      help="Task title")
parser.add_argument("--due",        metavar="YYYY-MM-DD", help="Due date")
parser.add_argument("--percent",    type=int, metavar="0-100", help="Completion percentage")
parser.add_argument("--assignee",   help="User ID to assign the task to")

args = parser.parse_args()
COMMANDS[args.command](args)
