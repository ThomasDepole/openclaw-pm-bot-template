# rclone + Dropbox Setup Guide (General)

**Purpose:** General reference for setting up rclone to sync with Dropbox on a headless Linux VM.

**Date Written:** 2026-03-03

---

## What is rclone?

rclone is a command-line tool for syncing files between local storage and cloud providers (Dropbox, Google Drive, S3, OneDrive, and many more). It's like rsync but for cloud storage.

---

## Installation

### Linux (VM)
```bash
curl https://rclone.org/install.sh | sudo bash
```

### Windows (PowerShell — for auth on local machine)
```powershell
winget install Rclone.Rclone
```

Verify:
```bash
rclone version
```

---

## Config File Location

By default, rclone stores config at:
- **Linux:** `~/.config/rclone/rclone.conf`
- **Windows:** `%AppData%\rclone\rclone.conf`

### Use a Custom Config Path (Recommended)

To keep config organized inside a specific directory, use the `RCLONE_CONFIG` environment variable:

```bash
# Add to ~/.bashrc for persistent effect
export RCLONE_CONFIG=/path/to/your/rclone.conf
```

Or pass it per-command:
```bash
rclone ls dropbox:/ --config /path/to/rclone.conf
```

> **Tip:** Never use `cd` to change where rclone looks for config — it always uses the default path or `RCLONE_CONFIG`. The working directory has no effect.

---

## Setting Up a Dropbox Remote

### Step 1: Create a Dropbox App

1. Go to **https://dropbox.com/developers/apps** → **Create app**
2. Choose **Scoped Access**
3. Choose access type:
   - **Full Dropbox** — access to all files/folders (use when you need multiple sync targets)
   - **App Folder** — sandboxed to one folder (`/Apps/YourAppName/`) — more secure for single-use
4. Name your app and click **Create app**
5. Go to **Permissions** tab, enable:
   - `files.content.read`
   - `files.content.write`
   - `files.metadata.read`
   - Click **Submit**
6. Go to **Settings** tab:
   - Add Redirect URI: `http://localhost:53682/`
   - Copy your **App key** and **App secret**

---

### Step 2: Configure rclone

```bash
rclone config
```

- `n` → New remote
- Name: `dropbox` (or any name you want)
- Type: `dropbox`
- Enter **App key** and **App secret**
- Advanced config: `n`

When prompted to auto-open browser → if on a headless server, say `n` and use the manual auth flow below.

---

### Step 3: Authorize (Manual OAuth — for Headless Servers)

If you can't open a browser on the server, authorize from your local machine:

**Option A: Using rclone on Windows/Mac locally**
```powershell
rclone authorize "dropbox" "YOUR_APP_KEY" "YOUR_APP_SECRET"
```
> If you get a port binding error on Windows, use Option B instead.

**Option B: Manual curl flow (works everywhere)**

1. Open this URL in your browser (replace `YOUR_APP_KEY`):
```
https://www.dropbox.com/oauth2/authorize?client_id=YOUR_APP_KEY&response_type=code&token_access_type=offline
```

2. Click **Continue** → **Allow**. You'll be redirected to `localhost:53682` which fails to load — that's expected. Copy the full URL from your browser address bar and extract the `code=` parameter value.

3. Exchange the code for tokens on the server:
```bash
curl -X POST https://api.dropbox.com/oauth2/token \
  -u "YOUR_APP_KEY:YOUR_APP_SECRET" \
  -d "code=PASTE_CODE_HERE&grant_type=authorization_code"
```

4. The response JSON looks like:
```json
{
  "access_token": "sl.u.ABC...",
  "token_type": "bearer",
  "refresh_token": "ABC...",
  "expires_in": 14400
}
```

5. Edit your rclone config file and set the token:
```ini
[dropbox]
type = dropbox
client_id = YOUR_APP_KEY
client_secret = YOUR_APP_SECRET
token = {"access_token":"sl.u.ABC...","token_type":"bearer","refresh_token":"ABC...","expiry":"0001-01-01T00:00:00Z"}
```

> **Important:** Always get a `refresh_token` (via the curl flow above). Console-generated access tokens expire in ~4 hours and have no refresh token.

---

### Step 4: Test the Connection

```bash
rclone ls dropbox:/
```

List a specific folder:
```bash
rclone ls "dropbox:/MyFolder"
```

---

## Common rclone Commands

| Command | What it does |
|---------|--------------|
| `rclone ls dropbox:/` | List files in Dropbox root |
| `rclone lsd dropbox:/` | List directories only |
| `rclone copy src/ dropbox:/dest/` | Copy files (no deletions) |
| `rclone sync dropbox:/src/ /local/dest/` | Sync (destination mirrors source; deletes extras in dest) |
| `rclone move dropbox:/src/ /local/dest/` | Move files (copies then deletes from source) |
| `rclone mkdir "dropbox:/NewFolder"` | Create a folder |
| `rclone size dropbox:/` | Show total size |

---

## Sync vs Move vs Copy

| Command | Copies files | Deletes from source | Deletes extras from dest |
|---------|-------------|---------------------|--------------------------|
| `copy` | ✅ | ❌ | ❌ |
| `sync` | ✅ | ❌ | ✅ (mirrors source) |
| `move` | ✅ | ✅ | ❌ |

**Use `move` when:** You want files transferred and removed from the source (e.g., ingestion pipelines where files should be consumed once).  
**Use `sync` when:** You want the destination to always mirror the source.  
**Use `copy` when:** You want a one-way copy with no deletions anywhere.

---

## Setting Up a Cron Job

```bash
crontab -e
```

Example — run every 5 minutes:
```
*/5 * * * * /path/to/your/sync-script.sh
```

### Example Sync Script

```bash
#!/bin/bash
export RCLONE_CONFIG=/path/to/rclone.conf
rclone move "dropbox:/IncomingFolder" \
  "/local/destination/" \
  --log-file=/path/to/rclone-sync.log \
  --log-level INFO
```

> **Note on `--delete-empty-src-dirs`:** This flag removes empty directories from the source after a move. Use with caution if other processes (like Zapier) depend on those directories existing — they will be deleted and may need to be recreated.

---

## Locking Access to a Specific Folder

If you want to restrict rclone to a single Dropbox folder (for security):

**Option 1 — App Folder (Dropbox-level restriction)**
- When creating the Dropbox app, choose **App Folder** instead of Full Dropbox
- rclone can only see `/Apps/YourAppName/` — nothing else in Dropbox is accessible
- Specify the folder in your sync command as `dropbox:/` (the app folder is the root)

**Option 2 — Full Dropbox with path restriction**
- Use Full Dropbox access but always specify a subfolder in your rclone commands
- `rclone move "dropbox:/SpecificFolder" /local/dest/`
- rclone won't touch anything outside that path as long as your scripts are scoped correctly

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `bind: forbidden` error on Windows | Firewall blocking port 53682 | Try `netsh advfirewall firewall add rule name="rclone" dir=in action=allow protocol=TCP localport=53682` or use manual curl flow |
| `Couldn't decode response` during config | Pasted raw token instead of rclone's JSON blob format | Use the manual curl flow to get properly formatted tokens |
| Token expires after a few hours | No refresh token | Redo auth with `token_access_type=offline` in the auth URL |
| Config not found | rclone using default path, not custom path | Set `RCLONE_CONFIG` env var or pass `--config` flag |
| Files re-copied every run | Using `copy` or `sync` instead of `move` | Switch to `rclone move` for consume-once pipelines |

---

## File Structure Recommendation

Keep all rclone-related files together:

```
/home/clawadmin/.openclaw/
├── rclone.conf              ← rclone config (all remotes)
├── scripts/
│   └── sync-dropbox.sh      ← sync script(s)
└── logs/
    └── rclone-sync.log      ← sync logs
```
