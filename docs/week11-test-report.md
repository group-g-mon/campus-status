# Week 11 testing report

Project: Campus Status
Tester(s): Ibrahim - A00022173
Date: 23 November 2026
Python version: Python 3.13.14
Git commit or branch: main

## Scope and environment

Testing local Python file operations with pytest in a temporary test directory.
No production files or cloud resources are changed.

## Test plan - Configuration backup

Requirements: B1-B4 in the Week 11 tutorial.
Approach: representative valid and invalid files; expected error for missing source.

| ID   | Test data and starting state                           | Expected result                                      | Actual result                                                             | Status |
| ---- | ------------------------------------------------------ | ---------------------------------------------------- | ------------------------------------------------------------------------- | ------ |
| B-T1 | `monitoring.json` with `{"port": 443}`; no destination | Copy contents unchanged; return its destination path | Copied text equal to `{"port": 443}`; returned `[backup/monitoring.json]` | Pass   |
| B-T2 | `service.json` and `notes.txt`; no destination         | Copy only `service.json`; return only that path      | Destination contained only `service.json`; returned only its path         | Pass   |
| B-T3 | Source path does not exist                             | Raise `FileNotFoundError`; do not create destination | `FileNotFoundError` raised; destination did not exist                     | Pass   |

## Execution and evidence

Manual backup observation (Section 3):
Command run: `.\.venv\Scripts\python.exe -c "from scripts.backup import backup_files; print(backup_files('sample-data/week11-backup-input', 'output/week11-backup'))"`
Observed files in `output/week11-backup`: `monitoring.json` (39 bytes) and `service.json` (44 bytes) only.
`notes.txt` was not copied. Both copied files' contents matched the source files.
This is a manual observation; it is not an automated test result.

Automated backup tests:
Command used: `.\.venv\Scripts\python.exe -m pytest tests/test_backup.py -v`
Summary: 3 passed in 0.12s.
Relevant failure messages, if any: none.
Elapsed time observation, if recorded: 0.12s; observation only, not a performance target.

## Deployment tests

Requirements: D1-D6 in the Week 11 lab.
Method: equivalence partitions for file types and source states;
check actual files, contents, returned paths and errors.

| ID   | Test data and starting state                       | Expected result                                                                                                | Actual result | Status  |
| ---- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------- | ------- |
| D-T1 | Source contains `service.json`; destination absent | Destination created; `service.json` copied with unchanged contents; returns exactly `[deployment/service.json]` | Destination created; contents `{"enabled": true}`; returned `[deployment/service.json]` | Pass |

| D-T2 | Source contains `service.json` and `notes.txt`     | Only `service.json` in destination; returns only that path                                                     | First run: `notes.txt` also deployed (see investigation). After correction: only `service.json` | Fail, then Pass   |

| D-T3 | Source exists but is empty                         | Destination created and empty; returns `[]`                                                                    | Not run       | Not run |
| D-T4 | Source directory does not exist                    | Raise `FileNotFoundError`; destination not created                                                             | Not run       | Not run |

### Defect investigation

### Defect investigation

Requirement checked: D1 and D3 — only files ending in exactly `.json` directly inside the source folder may be copied; other file types must not be copied.

Observed failure and evidence: `test_deploy_excludes_other_files` failed against the supplied starter:

    >       assert sorted(path.name for path in destination.iterdir()) == ["service.json"]
    E       AssertionError: assert ['notes.txt', 'service.json'] == ['service.json']
    E         At index 0 diff: 'notes.txt' != 'service.json'
    E         Left contains one more item: 'service.json'

The destination contained `notes.txt` as well as `service.json`, and the returned list contained both paths. The deployment was therefore unsuitable even though it looked successful.

Cause found in the code: in `scripts/deploy_config.py`, the selection condition was `if path.is_file():`. It accepts every regular file in the source folder and never inspects the extension, so `notes.txt` satisfied it.

Correction made: changed the condition to `if path.is_file() and path.suffix == ".json":`. No other change was needed — `copy2`, the returned list, and the source check already meet D2, D4 and D6. `.JSON` remains excluded because `suffix` is compared exactly.

Result after correction: `test_deploy_excludes_other_files` passed; the destination contained only `service.json`, and the returned list contained only that path.

### Final verification

Command and result for deployment tests:
Command and result for the full test suite:
Anything not tested:

## Findings and limits

Defects found and actions taken:
What has not been tested: