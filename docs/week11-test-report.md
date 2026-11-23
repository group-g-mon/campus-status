<!-- Paste this section UNDER the existing sections of your tutorial report. -->

## Deployment tests

Requirements: D1-D6 in the Week 11 lab.
Method: equivalence partitions for file types and source states;
check actual files, contents, returned paths and errors.

Reason for the chosen cases: each case is one kind of input the function can get.
A normal JSON file (D1, D2, D4), a JSON file plus an unwanted file type (D3),
an empty source (D5) and a missing source (D6).

| ID | Test data and starting state | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- |
| D-T1 | Source contains `service.json` (`{"enabled": true}`); destination absent | `deployment/service.json` is created with the same text; returns `[deployment/service.json]` | Starter version: 1 passed. File created, content `{"enabled": true}`, returned list matched. | Pass |
| D-T2 | Source contains `service.json` and `notes.txt` | Destination holds only `service.json`; returned list has only that path | Starter version: **failed**. Destination held `['notes.txt', 'service.json']`. After correction: 1 passed, destination holds `['service.json']`. | Fail (starter) / Pass (corrected) |
| D-T3 | Source exists but is empty; destination absent | Destination folder is created and empty; returns `[]` | 1 passed. Destination exists, is empty, returned `[]`. | Pass |
| D-T4 | Source directory does not exist | `FileNotFoundError` raised; destination not created | 1 passed. Error raised, destination does not exist. | Pass |

### Defect investigation

Requirement checked:
D1 and D3 (copy only `.json` files directly inside the source; do not copy other file types).

Observed failure and evidence:
Version tested: starter code, unchanged. `test_deploy_excludes_other_files` failed with
`AssertionError: assert ['notes.txt', 'service.json'] == ['service.json']`.
The unwanted `notes.txt` was copied to the destination. D-T1 still passed, because it only
had a JSON file, so it could not see the problem.

Cause found in the code:
The `if` inside the `for` loop was `if path.is_file():`. It only checks that the entry is a file,
and never checks the extension, so every file type was copied.

Correction made:
Line 21 of `scripts/deploy_config.py` changed to
`if path.is_file() and path.suffix == ".json":`.
Nothing else was changed. `.JSON` (uppercase) is skipped, as the lab says.

Result after correction:
`test_deploy_excludes_other_files` passed. All 4 deployment tests passed.

### Final verification

Command and result for deployment tests:
`python -m pytest tests/test_deploy_config.py -v` -> 4 passed in 0.01s

Command and result for the full test suite:
`python -m pytest -q` -> **REPLACE WITH YOUR OWN OUTPUT** (mine ran only the 4 deployment tests: `4 passed in 0.01s`.
Your repo also has the Week 10 tests, so your count will be higher.)

Anything not tested:
No real server or cloud service. No large folders. No `.JSON` uppercase files.
Subdirectories (D3, optional D-T5) were not tested. Nested folders and file permissions were not tested.
