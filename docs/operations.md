# Operations notes

## Health check

The health check tests whether the local Campus Status demo service is responding. The service must already be running before you run it.

Run the command from the project root (the `campus-status` folder):

```bash
python scripts/health_check.py
```

The script requests the URL built from `config/service.json` (currently `http://localhost:8080/`). The timeout and expected status code come from `config/monitoring.json` (see the Monitoring settings section).

### Results

| Output | Meaning | Exit code |
|---|---|---|
| `SERVICE OK: <url> returned 200` | The service answered with the expected status. | `0` |
| `SERVICE UNAVAILABLE: <error>` | No response from the service. | `1` |
| `UNEXPECTED STATUS: got X, expected Y` | The service answered, but with a different status code. | `1` |

If you see `SERVICE UNAVAILABLE` with a "connection refused" error, nothing is listening on that host and port. Check that the service is running and that the port matches `config/service.json`.

If you run the command from a different folder, Python may report that it can't open the file. Change to the project root and run it again.

## Configuration validation

Run:

```bash
python scripts/validate_config.py
```

## Backup

Run:

```bash
python scripts/backup.py
```

Backups are written to the local `backup/` directory, which is ignored by Git.
