import pytest

from scripts.deploy_config import deploy_configs


def test_deploy_copies_json_file(tmp_path):
    # Arrange: one JSON file; the destination is deliberately absent.
    source = tmp_path / "source"
    source.mkdir()
    (source / "service.json").write_text('{"enabled": true}', encoding="utf-8")
    destination = tmp_path / "deployment"

    # Act: run the real function on the test's own input.
    copied = deploy_configs(source, destination)

    # Assert: contents unchanged (D2), destination created (D4),
    # and the returned path is exactly the deployed copy.
    assert (destination / "service.json").read_text(encoding="utf-8") == '{"enabled": true}'
    assert copied == [destination / "service.json"]


def test_deploy_excludes_other_files(tmp_path):
    # Arrange: one permitted configuration file and one excluded note.
    source = tmp_path / "source"
    source.mkdir()
    (source / "service.json").write_text('{"enabled": true}', encoding="utf-8")
    (source / "notes.txt").write_text("internal notes", encoding="utf-8")
    destination = tmp_path / "deployment"

    # Act
    copied = deploy_configs(source, destination)

    # Assert: check the entire destination, so an extra file cannot hide (D3).
    assert sorted(path.name for path in destination.iterdir()) == ["service.json"]
    assert copied == [destination / "service.json"]


def test_deploy_empty_source(tmp_path):
    # Arrange: the source EXISTS but is empty. This deliberately differs
    # from the missing-source case below, which must raise (D5 vs D6).
    source = tmp_path / "source"
    source.mkdir()
    destination = tmp_path / "deployment"

    # Act
    copied = deploy_configs(source, destination)

    # Assert: a successful deployment of zero files (D5).
    assert destination.is_dir()
    assert list(destination.iterdir()) == []
    assert copied == []


def test_deploy_missing_source(tmp_path):
    # Arrange: the source path is deliberately not created.
    source = tmp_path / "missing"
    destination = tmp_path / "deployment"

    # Act + Assert: this negative test passes when the expected error occurs (D6).
    with pytest.raises(FileNotFoundError):
        deploy_configs(source, destination)

    # An unsuccessful deployment must not leave a misleading destination.
    assert not destination.exists()
