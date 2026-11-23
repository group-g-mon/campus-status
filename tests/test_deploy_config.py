import pytest

from scripts.deploy_config import deploy_configs


def test_deploy_copies_json_file(tmp_path):
    # Arrange: source has one json file, destination does NOT exist yet
    source = tmp_path / "source"
    source.mkdir()
    (source / "service.json").write_text('{"enabled": true}', encoding="utf-8")
    destination = tmp_path / "deployment"

    # Act
    result = deploy_configs(source, destination)

    # Assert: file copied, content unchanged, returned path correct
    copied = destination / "service.json"
    assert copied.exists()
    assert copied.read_text(encoding="utf-8") == '{"enabled": true}'
    assert result == [copied]


def test_deploy_excludes_other_files(tmp_path):
    # Arrange: one json file AND one txt file
    source = tmp_path / "source"
    source.mkdir()
    (source / "service.json").write_text('{"enabled": true}', encoding="utf-8")
    (source / "notes.txt").write_text("internal notes", encoding="utf-8")
    destination = tmp_path / "deployment"

    # Act
    result = deploy_configs(source, destination)

    # Assert: check ALL destination files, not just service.json
    # (exists() alone would pass even if notes.txt was copied too)
    assert sorted(p.name for p in destination.iterdir()) == ["service.json"]
    assert result == [destination / "service.json"]


def test_deploy_empty_source(tmp_path):
    # Arrange: source exists but is empty.
    # This deliberately differs from the missing-source case (that raises an error).
    source = tmp_path / "source"
    source.mkdir()
    destination = tmp_path / "deployment"

    # Act
    result = deploy_configs(source, destination)

    # Assert: destination created, empty, and [] returned
    assert destination.is_dir()
    assert list(destination.iterdir()) == []
    assert result == []


def test_deploy_missing_source(tmp_path):
    # Arrange: source folder does NOT exist
    source = tmp_path / "does_not_exist"
    destination = tmp_path / "deployment"

    # Act + Assert: must raise FileNotFoundError
    with pytest.raises(FileNotFoundError):
        deploy_configs(source, destination)

    # Easy to overlook: destination must NOT have been created
    assert not destination.exists()
