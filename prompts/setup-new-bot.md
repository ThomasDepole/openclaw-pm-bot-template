# Prompt: Set Up a New PM Bot

Paste this into any active OpenClaw bot (e.g. your main assistant).
Replace all `{{TOKENS}}` before sending.

---

## Tokens to fill in

| Token | What to put here | Example |
|-------|-----------------|---------|
| `{{BOT_NAME}}` | Short name, no spaces or special chars | `pm-acme`, `sarah-pm`, `ops-bot` |
| `{{DISPLAY_NAME}}` | Human-readable name for the bot | `Acme PM Bot`, `Sarah` |
| `{{CHANNEL_DESCRIPTION}}` | Where the bot will live | `the #pm-bot Discord channel`, `a Telegram DM` |

---

## The Prompt

```
I'd like to set up a new OpenClaw PM bot using the official template. Can you help me stand it up?

Bot name: {{BOT_NAME}}
Display name: {{DISPLAY_NAME}}
Channel: {{CHANNEL_DESCRIPTION}}

Please do the following:

1. Find the .openclaw directory and create a new workspace folder called workspace-{{BOT_NAME}} inside it

2. Clone the PM bot template into that folder:
   git clone https://github.com/ThomasDepole/openclaw-pm-bot-template.git <path>/workspace-{{BOT_NAME}}

3. Show me the openclaw.json snippet I need to add — both the agents.list entry and the bindings entry — to create a new agent called {{BOT_NAME}} pointing at that workspace and bound to {{CHANNEL_DESCRIPTION}}

4. Let me know what to do after I've added the config and restarted the gateway

I'll handle the openclaw.json edit and gateway restart myself — just get the workspace cloned and show me exactly what config to add.
```

---

## What happens next

After the bot clones the workspace and shows you the config:

1. Add the `agents.list` entry and `bindings` entry to your `openclaw.json`
2. Restart the OpenClaw gateway
3. Send your first message to the new bot — it will introduce itself and walk you through setup (driven by `BOOTSTRAP.md`)
