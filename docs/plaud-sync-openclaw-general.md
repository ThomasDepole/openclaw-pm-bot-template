# Plaud → Zapier → Dropbox → OpenClaw: General Setup Guide

**Purpose:** A generic guide for connecting Plaud meeting recordings to any OpenClaw agent's ingestion folder via Zapier and Dropbox. Adapt paths, folder names, and content mapping to fit your own setup.

---

## Overview

When a Plaud recording finishes, Zapier automatically creates a text file in Dropbox. A sync script on the machine running OpenClaw picks up the file and drops it into your agent's ingestion folder for processing.

**Flow:**
```
Plaud (recording complete)
  → Zapier (trigger: Transcript & Summary Ready)
    → Dropbox (action: Create Text File)
      → rclone (cron job on your server: move to ingestion folder)
        → OpenClaw agent reads and processes the file
```

---

## What You'll Need

- A Plaud account with Zapier integration enabled
- A Zapier account (free tier is sufficient)
- A personal Dropbox account
- OpenClaw running on a Linux server (or local machine)
- rclone installed on that server
- Basic SSH access to your server

---

## Step 1: Create a Dropbox App

This gives rclone scoped, authenticated access to your Dropbox.

1. Go to **https://dropbox.com/developers/apps** → **Create app**
2. Choose **Scoped Access**
3. Choose **Full Dropbox** *(allows multiple folders for multiple purposes; if you only need one folder, App Folder is more isolated)*
4. Name your app (e.g., `OpenClaw Sync`)
5. Click **Create app**
6. Under the **Permissions** tab, enable:
   - `files.content.read`
   - `files.content.write`
   - `files.metadata.read`
   - Click **Submit**
7. Under the **Settings** tab:
   - Add Redirect URI: `http://localhost:53682/`
   - Note your **App key** and **App secret** — you'll need these shortly

---

## Step 2: Install and Authenticate rclone

### Install rclone on your server
```bash
curl https://rclone.org/install.sh | sudo bash
```

### Configure the Dropbox remote

Choose a config file location that makes sense for your setup. A good practice is to keep it alongside your OpenClaw workspace rather than in the default `~/.config/` location:

```bash
rclone config --config /path/to/your/rclone.conf
```

In the wizard:
- `n` → New remote
- Name it: `dropbox`
- Type: `dropbox`
- Enter your **App key** and **App secret**
- Advanced config: `n`
- Auto-open browser: `n` if your server is headless

### Authorize rclone (headless server — manual OAuth)

Since your server likely can't open a browser, authorize from your local machine:

**1.** Open this URL in your local browser (swap in your App key):
```
https://www.dropbox.com/oauth2/authorize?client_id=YOUR_APP_KEY&response_type=code&token_access_type=offline
```

**2.** Click **Continue** → **Allow**. Dropbox will redirect to `localhost:53682` which will fail — that's expected. Copy the full URL from your address bar and extract the value after `code=`.

**3.** On your server, exchange the code for tokens:
```bash
curl -X POST https://api.dropbox.com/oauth2/token \
  -u "YOUR_APP_KEY:YOUR_APP_SECRET" \
  -d "code=PASTE_CODE_HERE&grant_type=authorization_code"
```

**4.** The response includes an `access_token` and a `refresh_token`. Edit your rclone config file and add the token:
```ini
[dropbox]
type = dropbox
client_id = YOUR_APP_KEY
client_secret = YOUR_APP_SECRET
token = {"access_token":"...","token_type":"bearer","refresh_token":"...","expiry":"0001-01-01T00:00:00Z"}
```

> **Why the curl flow?** The console-generated token expires in ~4 hours and has no refresh token. The OAuth code exchange gives you a refresh token so rclone stays authorized indefinitely.

**5.** Test it:
```bash
RCLONE_CONFIG=/path/to/rclone.conf rclone ls dropbox:/
```

---

## Step 3: Create Your Dropbox Folder Structure

Create a folder in Dropbox that Zapier will write to:

```bash
RCLONE_CONFIG=/path/to/rclone.conf rclone mkdir "dropbox:/YourFolderName"
```

Name it whatever makes sense for your use case (e.g., `/OpenClaw/ingestion`, `/MeetingNotes`, `/AIInbox`).

---

## Step 4: Create the Sync Script and Cron Job

### Sync script

```bash
#!/bin/bash
export RCLONE_CONFIG=/path/to/rclone.conf
rclone move "dropbox:/YourDropboxFolder" \
  "/path/to/your/openclaw/ingestion/folder/" \
  --log-file=/path/to/rclone-sync.log \
  --log-level INFO
```

Save this as a `.sh` file and make it executable:
```bash
chmod +x /path/to/sync-script.sh
```

> **`rclone move` vs `rclone sync`:** Use `move` so files are deleted from Dropbox after being transferred. This prevents the same file from being re-processed on every sync run.  
> **Avoid `--delete-empty-src-dirs`** if you have Zapier (or any other tool) writing to fixed subfolders — that flag will delete the empty folders and break your Zapier target path.

### Schedule with cron

```bash
crontab -e
```

Run every 5 minutes:
```
*/5 * * * * /path/to/sync-script.sh
```

---

## Step 5: Configure Zapier

### Trigger
- App: **Plaud**
- Event: **Transcript & Summary Ready**
- Connect your Plaud account and test to load sample fields

### Action
- App: **Dropbox**
- Event: **Create Text File** *(not "Upload File" — that requires a binary; "Create Text File" accepts plain text directly)*

### Configure the action fields

| Field | Guidance |
|-------|----------|
| **Folder** | The Dropbox folder you created in Step 3 |
| **File Name** | Use Plaud's `Title` field — Dropbox will automatically append `.txt` |
| **File Content** | Map to the Plaud field(s) you want your agent to receive (see below) |
| **Overwrite** | Set to **True** to avoid errors on duplicate uploads |
| **Include sharing link** | **No** |

### Choosing what to put in File Content

Plaud provides several fields. Choose based on what your agent needs:

| Use case | What to map |
|----------|-------------|
| AI summary only (concise, processed) | `Summary` field |
| Full verbatim transcript | `Transcript` field |
| Both | Combine: `Summary:\n{{Summary}}\n\nTranscript:\n{{Transcript}}` |
| Everything available | Map all fields with clear labels |

The file content becomes exactly what your OpenClaw agent reads, so structure it in a way that's easy to parse. Markdown formatting (headers, bullets) works well.

---

## Step 6: Test End-to-End

1. In Zapier, click **Test** on the action step — a file should appear in your Dropbox folder
2. On your server, run the sync script manually:
   ```bash
   /path/to/sync-script.sh
   ```
3. Confirm the file landed in your ingestion folder:
   ```bash
   ls /path/to/openclaw/ingestion/
   ```
4. Verify your OpenClaw agent picks it up and processes it
5. Turn on the Zap

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Port binding error on Windows during `rclone authorize` | Firewall blocking port 53682 | Use the manual curl OAuth flow in Step 2 |
| Files keep reappearing in Dropbox | Using `rclone sync` instead of `move` | Switch to `rclone move` in your script |
| File extension is `.txt` instead of your preferred format | Dropbox "Create Text File" always appends `.txt` | Expected — name your file without an extension in Zapier, or account for `.txt` in your agent's ingestion reader |
| Token expires after a few hours | No refresh token (used console-generated token) | Redo auth using the manual OAuth curl flow |
| Dropbox folder disappears after sync | Used `--delete-empty-src-dirs` | Remove that flag — it deletes empty source directories |
| Zapier can't find the target folder | Folder was deleted from Dropbox | Recreate the folder manually or via rclone mkdir |

---

## Notes for OpenClaw Users

- Your agent's ingestion folder path depends on how your workspace is configured. Check your agent's workspace directory for an `ingestion/` subfolder.
- The agent processes whatever lands in the ingestion folder — the file content becomes the agent's input. Structure it clearly.
- If you want the agent to delete files after processing, make sure your ingestion workflow handles cleanup (or configure your agent to delete processed files).
- For multiple agents, create separate Dropbox subfolders (e.g., `/OpenClaw/agent-one/`, `/OpenClaw/agent-two/`) and set up separate sync script entries or separate cron jobs per agent.
