# Deployment notes

For the lab demo, run the status site locally:

```bash
python -m http.server 8080 --directory site
```

The configured port is stored in `config/service.json`.

If the configuration and the running command disagree, the health check may fail.

## Backup

Run the backup script:

python scripts/backup.py

The script creates a timestamped backup folder and copies the configured files and folders into it.

The backup location is configured in config/backup.json. When the backup completes, the script displays the location of the backup folder.

## Recovery

Locate the required timestamped backup folder in the backup directory.

Copy the required files from the backup folder back into the project to restore the previous version.