# Task Management Tool Integration Guide

**Purpose:** How to connect this PM agent to the most common project/task management tools.

---

## Trello

**Auth method:** API Key + Token (user-level)

### Get credentials
1. Go to **https://trello.com/power-ups/admin** → create a Power-Up (or use an existing one)
2. Generate an **API Key** from that Power-Up's API Key page
3. Generate a **Token** by visiting: `https://trello.com/1/authorize?key=YOUR_API_KEY&scope=read,write&expiration=never&name=OpenClaw&response_type=token`
4. Store in `.env`:
   ```
   TRELLO_API_KEY=your_key
   TRELLO_TOKEN=your_token
   ```

### Find board/list IDs
```bash
source .env

# List your boards
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id"

# List columns/lists on a board
curl -s "https://api.trello.com/1/boards/BOARD_ID/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

### Create a task
```bash
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList=LIST_ID" \
  -d "name=Task title" \
  -d "desc=Context and source"
```

### Notes
- Rate limit: 300 req/10s per API key
- `jq` at `/home/node/.openclaw/jq` for parsing JSON responses

---

## Jira

**Auth method:** Email + API Token (Basic Auth)

### Get credentials
1. Go to **https://id.atlassian.com/manage-profile/security/api-tokens** → Create API token
2. Store in `.env`:
   ```
   JIRA_EMAIL=your_email@company.com
   JIRA_API_TOKEN=your_token
   JIRA_BASE_URL=https://yourcompany.atlassian.net
   ```

### Find project keys
```bash
source .env
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/project" | jq '.[].key'
```

### Create a task
```bash
source .env
curl -s -X POST "$JIRA_BASE_URL/rest/api/3/issue" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": { "key": "YOUR_PROJECT_KEY" },
      "summary": "Task title",
      "description": { "type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Context here"}]}] },
      "issuetype": { "name": "Task" }
    }
  }'
```

### Optional: Jira CLI
```bash
# Install
npm install -g jira-cli
# or: brew install ankitpokhrel/tap/jira-cli (Mac)

# Create issue
jira issue create --type Task --summary "Task title" --body "Context"
```

---

## Azure DevOps

**Auth method:** Personal Access Token (PAT)

### Get credentials
1. Go to **https://dev.azure.com/[your-org]** → User Settings → Personal Access Tokens
2. Create a token with **Work Items: Read & Write** scope
3. Store in `.env`:
   ```
   ADO_ORG=https://dev.azure.com/yourorg
   ADO_PROJECT=YourProjectName
   ADO_PAT=your_pat_here
   ```

### Create a work item
```bash
source .env
curl -s -X POST \
  "$ADO_ORG/$ADO_PROJECT/_apis/wit/workitems/\$Task?api-version=7.0" \
  -u ":$ADO_PAT" \
  -H "Content-Type: application/json-patch+json" \
  -d '[
    { "op": "add", "path": "/fields/System.Title", "value": "Task title" },
    { "op": "add", "path": "/fields/System.Description", "value": "Context here" }
  ]'
```

### Optional: Azure CLI
```bash
# Install
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az extension add --name azure-devops

# Configure
az devops configure --defaults organization=$ADO_ORG project="$ADO_PROJECT"
echo $ADO_PAT | az devops login

# Create work item
az boards work-item create --type Task --title "Task title" --description "Context"
```

---

## Linear

**Auth method:** Personal API Key

### Get credentials
1. Go to **https://linear.app/settings/api** → Create personal API key
2. Store in `.env`:
   ```
   LINEAR_API_KEY=lin_api_your_key_here
   ```

### Find team IDs
```bash
source .env
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ teams { nodes { id name } } }"}'
```

### Create an issue
```bash
source .env
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CreateIssue($input: IssueCreateInput!) { issueCreate(input: $input) { issue { id title } } }",
    "variables": {
      "input": {
        "teamId": "YOUR_TEAM_ID",
        "title": "Task title",
        "description": "Context here"
      }
    }
  }'
```

---

## GitHub Issues

**Auth method:** Personal Access Token or GitHub App

### Get credentials
1. Go to **https://github.com/settings/tokens** → Generate new token (classic)
2. Scopes needed: `repo` (for private repos) or `public_repo`
3. Store in `.env`:
   ```
   GITHUB_TOKEN=ghp_your_token
   GITHUB_REPO=org/repo-name
   ```

### Create an issue (CLI — recommended)
```bash
# Install gh CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh

# Authenticate
echo $GITHUB_TOKEN | gh auth login --with-token

# Create issue
gh issue create --repo $GITHUB_REPO --title "Task title" --body "Context" --label "priority:high"
```

### Create an issue (REST API)
```bash
source .env
curl -s -X POST "https://api.github.com/repos/$GITHUB_REPO/issues" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Task title","body":"Context here","labels":["task"]}'
```

---

## Asana

**Auth method:** Personal Access Token

### Get credentials
1. Go to **https://app.asana.com/0/my-apps** → Create new personal access token
2. Store in `.env`:
   ```
   ASANA_PAT=your_pat_here
   ```

### Find workspace and project IDs
```bash
source .env

# Get workspaces
curl -s -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces" | jq '.data[] | {gid, name}'

# Get projects in workspace
curl -s -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/projects?workspace=WORKSPACE_GID" | jq '.data[] | {gid, name}'
```

### Create a task
```bash
source .env
curl -s -X POST "https://app.asana.com/api/1.0/tasks" \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Task title",
      "notes": "Context here",
      "projects": ["PROJECT_GID"]
    }
  }'
```

---

## General Notes

- **Store all credentials in `.env`** — never hardcode in memory files or scripts
- **Record IDs in `memory/task-board.md`** — so the agent doesn't have to re-fetch them every time
- **Update `AGENTS.md`** with your actual commands once configured — the generic placeholders won't work until you do
- **Test manually first** — run the curl/CLI command directly before trusting the agent to use it
