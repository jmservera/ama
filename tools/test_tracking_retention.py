"""PR438 safety regressions; all deletion exercises use disposable synthetic data."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tarfile

import pytest

import tracking_retention as retention


@pytest.fixture
def workflow(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> retention.Retention:
    repo = tmp_path / "repo"
    repo.mkdir()
    tracking = repo / retention.TRACKING
    tracking.mkdir()
    names = (".copilot-tracking/a.jpg", ".copilot-tracking/b.pptx")
    for name in names:
        (repo / name).write_bytes(name.encode())
    (tracking / "protected.md").write_text("keep")
    (tracking / "opaque-link").symlink_to(tmp_path / "private-not-opened")
    monkeypatch.setattr(retention, "approved_paths", lambda: names)
    monkeypatch.setattr(retention, "EXPECTED_BYTES", sum(len(name) for name in names))
    monkeypatch.setattr(retention, "CANONICAL", {})
    monkeypatch.setattr(retention, "ARCHIVE_BASE", tmp_path / "archives")
    monkeypatch.setattr(retention.subprocess, "check_output", lambda *args, **kwargs: "fixture\n")
    operation = retention.Retention(repo)
    operation.build()
    return operation


def restore_fixture(operation: retention.Retention) -> Path:
    """Only tests substitute a tiny selection; the CLI has no override."""
    output = operation.repo.parent / "restored"
    operation.restore(output)
    return output / "restore-proof.json"


def rebind_archive(operation: retention.Retention) -> tuple[dict, dict, Path]:
    compact = retention.read_json(operation.manifest)
    destination = Path(compact["external_directory"]).expanduser()
    receipt_path = destination / "receipt.json"
    receipt = retention.read_json(receipt_path)
    receipt["archive_sha256"] = retention.file_hash(destination / "tracking.tar.gz")
    receipt_path.write_text(json.dumps(receipt))
    compact["archive_sha256"] = receipt["archive_sha256"]
    compact["receipt_sha256"] = retention.file_hash(receipt_path)
    operation.manifest.write_text(json.dumps(compact))
    return compact, receipt, destination


def test_given_report_when_selection_expands_then_exact_115_paths() -> None:
    report = Path(__file__).resolve().parents[1] / (
        ".copilot-tracking/research/subagents/2026-10-24/"
        "tracking-retention-pr438-preservation-research.md")
    text = report.read_text()
    section = text.split("### D2: 113 Older Preview Images", 1)[1].split("### Explicit Exclusions", 1)[0]
    expected = set()
    for line in section.splitlines():
        if not line.startswith("| 2026-"):
            continue
        directory, names, count, _ = [cell.strip() for cell in line.strip("|").split("|")]
        expanded = []
        for item in names.split("; "):
            if " through " in item:
                first, last = item.split(" through ")
                match = re.fullmatch(r"(.*?)(\d+)(\.[A-Za-z]+)", first)
                assert match is not None
                prefix, start, suffix = match.groups()
                end = re.search(r"\d+(?=\.[A-Za-z]+$)", last)
                assert end is not None
                width = len(start) if start.startswith("0") else 0
                expanded.extend(f"{prefix}{number:0{width}d}{suffix}"
                                for number in range(int(start), int(end.group()) + 1))
            else:
                expanded.append(item)
        assert len(expanded) == int(count)
        expected.update(f".copilot-tracking/ppt/{directory}{name}" for name in expanded)
    for identifier in ("D1a", "D1b"):
        row = next(line for line in text.splitlines() if line.startswith(f"| {identifier} |"))
        expected.add(row.split("|")[2].strip())

    assert len(expected) == 115
    assert set(retention.approved_paths()) == expected
    assert retention.EXPECTED_BYTES == 26_219_104


def test_given_archive_when_verify_restore_prune_then_only_selected_removed(workflow) -> None:
    compact, receipt, destination = workflow.verify()
    proof = restore_fixture(workflow)

    removed = workflow.prune(proof)

    assert removed == list(retention.approved_paths())
    assert (workflow.repo / ".copilot-tracking/protected.md").read_text() == "keep"
    assert (workflow.repo / ".copilot-tracking/opaque-link").is_symlink()
    assert len(receipt["inventory"]) == 5
    assert compact["selected_count"] == 2
    assert destination.stat().st_mode & 0o777 == 0o700
    assert all(path.stat().st_mode & 0o777 == 0o600 for path in destination.iterdir())


def test_given_archive_tampering_when_verify_then_rejected(workflow) -> None:
    _, _, destination = workflow.verify()
    with (destination / "tracking.tar.gz").open("ab") as stream:
        stream.write(b"tampered")

    with pytest.raises(retention.RetentionError, match="Archive checksum"):
        workflow.verify()


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "traversal", "link", "content", "extra"])
def test_given_rebound_bad_archive_when_readback_then_rejected(workflow, mutation) -> None:
    _, _, destination = workflow.verify()
    archive = destination / "tracking.tar.gz"
    with tarfile.open(archive) as bundle:
        members = [(copy.copy(member), bundle.extractfile(member).read() if member.isfile() else None)
                   for member in bundle]
    target = next(index for index, (member, _) in enumerate(members) if member.isfile())
    if mutation == "missing":
        members.pop(target)
    elif mutation == "duplicate":
        members.append(members[target])
    elif mutation == "traversal":
        members[target][0].name = ".copilot-tracking/../../escape"
    elif mutation == "link":
        member = members[target][0]
        member.type = tarfile.SYMTYPE
        member.linkname = "../../escape"
        member.size = 0
        members[target] = member, None
    elif mutation == "extra":
        member = tarfile.TarInfo(".copilot-tracking/extra")
        members.append((member, b""))
    else:
        member, data = members[target]
        members[target] = member, b"X" * len(data)
    with tarfile.open(archive, "w:gz") as bundle:
        for member, data in members:
            bundle.addfile(member, io.BytesIO(data) if data is not None else None)
    rebind_archive(workflow)

    with pytest.raises(retention.RetentionError):
        workflow.verify()


@pytest.mark.parametrize("mutation", ["extra", "hash", "duplicate", "traversal"])
def test_given_altered_manifest_when_verify_then_rejected(workflow, mutation) -> None:
    compact = retention.read_json(workflow.manifest)
    if mutation == "extra":
        compact["selected"].append({"path": ".copilot-tracking/protected.md", "type": "file",
                                    "size": 4, "sha256": hashlib.sha256(b"keep").hexdigest()})
    elif mutation == "hash":
        compact["selected"][0]["sha256"] = "0" * 64
    elif mutation == "duplicate":
        compact["selected"].append(compact["selected"][0])
    else:
        compact["selected"][0]["path"] = "../escape"
    workflow.manifest.write_text(json.dumps(compact))

    with pytest.raises(retention.RetentionError):
        workflow.verify()


@pytest.mark.parametrize("mutation", ["change", "missing", "symlink", "parent-symlink"])
def test_given_source_drift_when_prune_then_nothing_deleted(workflow, mutation) -> None:
    proof = restore_fixture(workflow)
    target = workflow.repo / retention.approved_paths()[1]
    if mutation == "change":
        target.write_bytes(b"changed")
    elif mutation == "missing":
        target.unlink()
    elif mutation == "symlink":
        target.unlink()
        target.symlink_to("protected.md")
    else:
        original = workflow.repo / ".copilot-tracking"
        original.rename(workflow.repo.parent / "moved")
        original.symlink_to(workflow.repo.parent / "moved", target_is_directory=True)

    with pytest.raises((retention.RetentionError, OSError)):
        workflow.prune(proof)
    assert not (workflow.repo.parent / "archives").joinpath(
        Path(retention.read_json(workflow.manifest)["external_directory"]).name,
        "prune-journal.jsonl").exists()


@pytest.mark.parametrize("kind", ["existing", "symlink", "inside-repo", "traversal"])
def test_given_unsafe_restore_destination_when_restore_then_no_overwrite(workflow, kind) -> None:
    output = workflow.repo.parent / "destination"
    if kind == "existing":
        output.mkdir()
        (output / "keep").write_text("untouched")
    elif kind == "symlink":
        output.symlink_to(workflow.repo)
    elif kind == "traversal":
        output = workflow.repo.parent / "unused" / ".." / "repo" / "new-output"
    else:
        output = workflow.repo / "new-output"

    with pytest.raises(retention.RetentionError):
        workflow.restore(output)
    if kind == "existing":
        assert (output / "keep").read_text() == "untouched"


def test_given_interrupted_unlink_when_recover_then_journal_accounts_exact_removals(workflow, monkeypatch) -> None:
    proof = restore_fixture(workflow)
    original = retention.os.unlink
    calls = []

    def interrupted(leaf, *, dir_fd=None):
        calls.append(leaf)
        original(leaf, dir_fd=dir_fd)
        if len(calls) == 1:
            raise KeyboardInterrupt

    monkeypatch.setattr(retention.os, "unlink", interrupted)
    with pytest.raises(KeyboardInterrupt):
        workflow.prune(proof)
    with pytest.raises(retention.RetentionError, match="journal"):
        workflow.prune(proof)
    monkeypatch.setattr(retention.os, "unlink", original)

    removed = workflow.prune(proof, recover=True)

    assert removed == list(retention.approved_paths())
    _, _, destination = workflow.verify()
    events = [json.loads(line) for line in (destination / "prune-journal.jsonl").read_text().splitlines()]
    assert [event["path"] for event in events[1:] if event["event"] == "removed"] == removed
    assert workflow.prune(proof, recover=True) == removed


def test_given_drift_at_unlink_when_prune_then_journal_retains_pending(workflow, monkeypatch) -> None:
    proof = restore_fixture(workflow)
    original = workflow.check_file
    calls = 0

    def changed(root, entry):
        nonlocal calls
        if root == workflow.repo:
            calls += 1
            if calls == 3:
                (root / entry["path"]).write_bytes(b"late drift")
        original(root, entry)

    monkeypatch.setattr(workflow, "check_file", changed)
    with pytest.raises(retention.RetentionError, match="drift"):
        workflow.prune(proof)
    _, _, destination = workflow.verify()

    assert '"event":"pending"' in (destination / "prune-journal.jsonl").read_text()
    assert all((workflow.repo / name).exists() for name in retention.approved_paths())


@pytest.mark.parametrize("kind", ["fifo", "unreadable"])
def test_given_special_or_unreadable_entry_when_inventory_then_rejected(workflow, kind) -> None:
    target = workflow.repo / ".copilot-tracking/unsafe"
    if kind == "fifo":
        os.mkfifo(target)
    else:
        target.write_text("not readable")
        target.chmod(0)

    with pytest.raises(retention.RetentionError):
        retention.inventory(workflow.repo)


def test_given_file_changes_during_read_when_inventory_then_rejected(workflow, monkeypatch) -> None:
    original = retention.digest
    target = workflow.repo / retention.approved_paths()[0]

    def changing(stream):
        result = original(stream)
        target.write_bytes(b"concurrent edit")
        return result

    monkeypatch.setattr(retention, "digest", changing)

    with pytest.raises(retention.RetentionError, match="changed"):
        retention.inventory(workflow.repo)


def test_given_existing_manifest_when_build_then_no_overwrite(workflow) -> None:
    before = workflow.manifest.read_bytes()

    with pytest.raises(retention.RetentionError, match="already exists"):
        workflow.build()

    assert workflow.manifest.read_bytes() == before


def test_given_nested_restore_when_created_then_all_permissions_are_private(workflow) -> None:
    output = workflow.repo.parent / "nested-restore"

    workflow.restore(output)

    assert all(path.stat().st_mode & 0o777 == (0o700 if path.is_dir() else 0o600)
               for path in [output, *output.rglob("*")])


def test_given_restore_parent_symlink_when_creating_then_escape_rejected(tmp_path) -> None:
    root = tmp_path / "root"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (root / ".copilot-tracking").symlink_to(outside)

    with pytest.raises(OSError):
        retention.restore_parents(root, ".copilot-tracking/escape/file")

    assert list(outside.iterdir()) == []


def test_given_altered_external_receipt_when_verify_then_rejected(workflow) -> None:
    _, _, destination = workflow.verify()
    with (destination / "receipt.json").open("a") as stream:
        stream.write(" ")

    with pytest.raises(retention.RetentionError, match="Receipt checksum"):
        workflow.verify()


def test_given_changed_accounting_when_verify_then_rejected(workflow) -> None:
    compact = retention.read_json(workflow.manifest)
    compact["before"]["file"] += 1
    workflow.manifest.write_text(json.dumps(compact))

    with pytest.raises(retention.RetentionError, match="accounting"):
        workflow.verify()


def test_given_nonprivate_archive_when_verify_then_rejected(workflow) -> None:
    _, _, destination = workflow.verify()
    (destination / "tracking.tar.gz").chmod(0o644)

    with pytest.raises(retention.RetentionError, match="permissions"):
        workflow.verify()


def test_given_protected_drift_when_prune_then_selection_untouched(workflow) -> None:
    proof = restore_fixture(workflow)
    (workflow.repo / ".copilot-tracking/protected.md").write_text("concurrent parent edit")

    with pytest.raises(retention.RetentionError, match="Protected"):
        workflow.prune(proof)

    assert all((workflow.repo / name).exists() for name in retention.approved_paths())


def test_given_canonical_drift_when_verify_then_rejected(workflow, monkeypatch) -> None:
    name = "canonical.pptx"
    (workflow.repo / name).write_bytes(b"changed")
    monkeypatch.setattr(retention, "CANONICAL", {name: hashlib.sha256(b"original").hexdigest()})

    with pytest.raises(retention.RetentionError, match="Canonical"):
        workflow.verify()


def test_given_wrong_selection_size_when_validate_then_rejected(workflow, monkeypatch) -> None:
    monkeypatch.setattr(retention, "EXPECTED_BYTES", 999)

    with pytest.raises(retention.RetentionError, match="byte total"):
        workflow.verify()


def test_given_changed_restore_proof_when_prune_then_selection_untouched(workflow) -> None:
    proof = restore_fixture(workflow)
    payload = retention.read_json(proof)
    payload["verified"].append({"path": ".copilot-tracking/protected.md"})
    proof.write_text(json.dumps(payload))

    with pytest.raises(retention.RetentionError, match="proof mismatch"):
        workflow.prune(proof)

    assert all((workflow.repo / name).exists() for name in retention.approved_paths())


def test_given_cli_when_selection_override_then_unavailable() -> None:
    with pytest.raises(SystemExit):
        retention.create_parser().parse_args(["prune", "--selection", "anything"])
