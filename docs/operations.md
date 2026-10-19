# Operations notes

## Health check

Run:

```bash
python scripts/health_check.py
```

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

## Monitoring settings

Monitoring behaviour is configured in `config/monitoring.json`:

```json
{
  "interval_seconds": 30,
  "timeout_seconds": 5,
  "expected_status": 200
}
```

| Setting | Current value | Meaning |
|---|---|---|
| `interval_seconds` | `30` | How many seconds the service waits between one status check and the next. |
| `timeout_seconds` | `5` | How many seconds a check waits for a response before it counts as failed. |
| `expected_status` | `200` | The HTTP status code that means the service is healthy. Any other code is treated as unhealthy. |

After changing any value, run the validator to confirm the file is still correct:

```bash
python scripts/validate_config.py
```

Keep `timeout_seconds` lower than `interval_seconds` so one check finishes before the next begins.