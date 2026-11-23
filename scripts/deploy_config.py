"""Copy prepared configuration files to a local deployment directory."""

from pathlib import Path
from shutil import copy2


def deploy_configs(source_dir, destination_dir):
    """Copy selected files and return the paths of the deployed copies."""
    source = Path(source_dir)
    destination = Path(destination_dir)

    # Check the source before creating a deployment destination.
    if not source.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source}")

    destination.mkdir(parents=True, exist_ok=True)
    copied = []

    # Inspect entries directly inside the source folder.
    for path in sorted(source.iterdir()):
        if path.is_file() and path.suffix == ".json":
            target = destination / path.name
            copy2(path, target)
            copied.append(target)

    # Return the files the function actually copied.
    return copied
