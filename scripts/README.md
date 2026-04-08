# scripts/

This folder is reserved for workspace-level helper scripts.

## Note: Document Extraction Script

The document extraction script used during ingestion lives at the **system level**, not here:

```
/home/node/.openclaw/scripts/extract-doc.py
```

This script is provided by OpenClaw and handles `.pdf`, `.docx`, `.xlsx`, `.pptx`, and `.csv` extraction.
You do not need to copy it here — reference it directly in shell commands:

```bash
python3 /home/node/.openclaw/scripts/extract-doc.py ingestion/your-file.docx
```

If you write custom helper scripts specific to your deployment, you can add them here.
