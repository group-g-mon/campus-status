#!/usr/bin/env python3
"""Create a simple timestamped backup of selected Campus Status files."""

from __future__ import annotations

import datetime as dt
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def copy_item(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination / source.name, dirs_exist_ok=True)
    elif source.is_file():
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination / source.name)
    else:
        print(f"Skipping missing item: {source}")


def main() -> int:
    config = load_json(ROOT / "config" / "backup.json")
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = ROOT / config["backup_dir"] / timestamp
    backup_root.mkdir(parents=True, exist_ok=True)

    for item in config["include"]:
        copy_item(ROOT / item, backup_root)

    print(f"Backup written to {backup_root}")
    return 0



def backup_files(source_dir, destination_dir):
    """Copy direct-child .json files and return their destination paths."""
    source = Path(source_dir)
    destination = Path(destination_dir)

    # Reject a missing source before creating any output directories.
    if not source.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source}")

    destination.mkdir(parents=True, exist_ok=True)
    copied = []

    # Look only at the files immediately inside the source directory.
    for path in sorted(source.iterdir()):
        # Do not copy notes, subdirectories or other file types.
        if path.is_file() and path.suffix == ".json":
            target = destination / path.name
            shutil.copy2(path, target)
            copied.append(target)

    # Report what was actually copied, not what we hoped to copy.
    return copied

if __name__ == "__main__":
    raise SystemExit(main())
