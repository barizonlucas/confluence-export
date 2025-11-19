# Confluence Space Bulk Export (Cloud)
This project automates the **bulk export** of Confluence Cloud spaces from the legacy site  
`https://old-xxx.atlassian.net/wiki`  
to support migration into the new Confluence site  
`https://new-xxx.atlassian.net/wiki`.

Exports are performed via Python using the `atlassian-python-api` library.  
**Imports are done manually in the new Confluence UI**, which is the safest and most reliable option considering Atlassian's current Cloud limitations.

---

## Features
- Bulk export of multiple Confluence spaces from the old instance.
- Automatic generation of `.xml.zip` export files.
- Exports saved into an `exports/` directory.
- Compatible with the native **Space Import** workflow in Confluence Cloud.

---

## Requirements
### System
- Windows 10/11
- Python 3.10+ (tested with Python 3.13)
- Pip installed and working

### Python Dependencies
Install the libraries with:

```powershell
pip install atlassian-python-api requests oauthlib requests_oauthlib
pip install "atlassian-python-api==3.41.11"
```

---

## Atlassian Credentials Setup
You will need:
- **Confluence Old URL:** https://old-xxx.atlassian.net/wiki
- **Your Atlassian email**
- **An API Token**

Generate the API token at [https://id.atlassian.com](https://id.atlassian.com/) -> **Security** -> **API Tokens** -> _Create API Token_.  
Insert your email and token directly into `export_spaces.py`.

---

## Preparing the Space List
Create a file named `spaces.txt` in the project root with **one Space Key per line**, for example:

```
ENT
PMO
CLIENTEX
DELIVERY
OPS
```

### Important
- Space Keys are **not** the space names.
- Space Keys appear in the URL: `/spaces/<SPACE_KEY>/`.
- Do not include spaces, slashes, or comments in the file.

---

## Running the Export Script
From a PowerShell terminal inside the project folder, run:

```powershell
python export_spaces.py
```

The script will:
1. Read all keys from `spaces.txt`.
2. Trigger Confluence XML exports.
3. Download each `.xml.zip` file.
4. Save everything into the `exports/` directory.

### Example Console Output

```
=== Exporting space: ENT ===
Export URL generated: https://...
>>> Space ENT exported to exports/ENT.xml.zip
```

---

## Importing Spaces into the New Confluence
Import each generated `.xml.zip` manually:
1. Go to https://new-xxx.atlassian.net/wiki.
2. Click **Settings** -> **General configuration**.
3. Open **Import Spaces**.
4. Click **Choose file**.
5. Select the exported file (e.g., `ENT.xml.zip`).
6. Click **Import**.
7. After completion, validate:
   - Page tree
   - Attachments
   - Images
   - Permissions

Repeat for each file located in the `exports/` directory.

---

## Post-Migration Validation Checklist
- Verify top-level pages.
- Confirm attachments and images.
- Check cross-page links.
- Adjust space permissions if needed.
- Confirm no broken XML imports.

---

## Project Structure

```
confluenceMigration/
|-- export_spaces.py   # Main bulk export script
|-- spaces.txt         # List of spaces to export
|-- exports/           # Auto-generated folder containing exported .zip files
`-- README.md          # This documentation
```

---

## Contributing
Contributions are welcome. Feel free to propose improvements such as:
- Parallel export
- Logging enhancements
- Retry logic for failed exports
- Mac/Linux support scripts

---

## License
MIT License
