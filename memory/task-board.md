# Task Board Reference

**Tool:** [FILL IN once configured]  
**Last Updated:** [FILL IN]

---

## Board / Project Structure

[FILL IN once task management tool is connected. Record board/project names, IDs, and column/list structure here so the agent can reference them without re-querying the API every time.]

---

## Trello (if using Trello)

```
## [Board Name]
Board ID: [ID]

| List / Column | ID |
|---------------|----|
| [Name]        | [ID] |
| [Name]        | [ID] |

Labels:
| Name | ID | Color |
|------|----|-------|
| [Name] | [ID] | [color] |
```

---

## Jira (if using Jira)

```
Base URL: https://yourcompany.atlassian.net
Project Key: [KEY]

## [Project Name]
Project ID: [ID]

Issue Types:
- Story: [ID]
- Task: [ID]
- Bug: [ID]
- Epic: [ID]

Common Statuses: To Do / In Progress / In Review / Done
Sprints: [List active/upcoming sprints if relevant]
```

---

## Azure DevOps (if using Azure DevOps)

```
Organization: https://dev.azure.com/[org]
Project: [Project Name]

## [Board Name]
Board ID: [ID]

Columns: [New / Active / Resolved / Closed — or custom]
Work Item Types: Epic / Feature / User Story / Task / Bug
Area Paths: [FILL IN if project uses area paths]
```

---

## Linear (if using Linear)

```
Workspace: [workspace name]
Team: [team name / ID]

States: [Backlog / Todo / In Progress / In Review / Done / Cancelled]
Labels: [FILL IN custom labels]
Cycles (Sprints): [Current cycle ID if applicable]
```

---

## GitHub Issues (if using GitHub Issues)

```
Org / Repo: github.com/[org]/[repo]

Labels: [FILL IN label names used for categorization]
Milestones: [FILL IN active milestones]
Projects: [FILL IN GitHub Projects board name/ID if used]
```

---

## Notes

[FILL IN: Any board-specific conventions, shortcuts, or recurring structures you want the agent to know about]
