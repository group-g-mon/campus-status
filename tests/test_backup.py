import pytest

from scripts.backup import backup_files


def test_backup_copies_one_configuration(tmp_path):
    # Arrange: prepare one source file in an isolated temporary folder.
    source = tmp_path / "source"
    source.mkdir()
    (source / "monitoring.json").write_text('{"port": 443}', encoding="utf-8")
    destination = tmp_path / "backup"  # It does not exist yet.

    # Act: run the real backup function with the test's input files.
    copied = backup_files(source, destination)

    # Assert: the copied contents and reported path match the requirement.
    assert (destination / "monitoring.json").read_text(encoding="utf-8") == '{"port": 443}'
    assert copied == [destination / "monitoring.json"]


def test_backup_excludes_notes(tmp_path):
    # Arrange: one permitted configuration file and one excluded note.
    source = tmp_path / "source"
    source.mkdir()
    (source / "service.json").write_text('{"enabled": true}', encoding="utf-8")
    (source / "notes.txt").write_text("internal notes", encoding="utf-8")
    destination = tmp_path / "backup"

    copied = backup_files(source, destination)

    # Check the entire output, so an extra file cannot go unnoticed.
    assert sorted(path.name for path in destination.iterdir()) == ["service.json"]
    assert copied == [destination / "service.json"]


def test_backup_missing_source(tmp_path):
    source = tmp_path / "missing"  # Deliberately do not create it.
    destination = tmp_path / "backup"

    # The specified exception is the correct result for this input.
    with pytest.raises(FileNotFoundError):
        backup_files(source, destination)

    # An unsuccessful backup must not create a misleading destination.
    assert not destination.exists()