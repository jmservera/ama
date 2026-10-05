"""Tests for rubric change detection in prepare.py, using temporary git repositories."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate  # noqa: E402
import prepare  # noqa: E402

RUBRIC_DIR = Path(__file__).resolve().parent.parent
SEED = json.loads((RUBRIC_DIR / "scores" / "latest.json").read_text(encoding="utf-8"))
REMOVED = "docs/brds/b.md"
MAX_BYTES = 1000


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def make_repo(root: Path) -> Path:
    """Create a repo on main with two BRD files and a workflow baseline that matches them."""
    git(root, "init", "-b", "main")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "test")
    config = root / ".github" / "rubric"
    (config / "scores").mkdir(parents=True)
    shutil.copy(RUBRIC_DIR / "rubric.json", config / "rubric.json")
    registry = json.loads((RUBRIC_DIR / "artifacts.json").read_text(encoding="utf-8"))
    (config / "artifacts.json").write_text(json.dumps(registry | {"max_file_bytes": MAX_BYTES}), encoding="utf-8")
    (root / "docs" / "brds").mkdir(parents=True)
    (root / "docs" / "brds" / "a.md").write_text("# A\n", encoding="utf-8")
    (root / REMOVED).write_text("# B\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "content")
    files, _ = prepare.match_files(root, ["docs/brds/**/*.md"], [], MAX_BYTES)
    baseline = dict(SEED, source="workflow", fingerprints={"brd": prepare.fingerprint_files(root, files)})
    (config / "scores" / "latest.json").write_text(json.dumps(baseline), encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "baseline")
    return root


@pytest.mark.parametrize(
    ("path", "pattern", "expected"),
    [
        ("docs/brds/a.md", "docs/brds/**/*.md", True),
        ("docs/brds/x/a.md", "docs/brds/**/*.md", True),
        ("docs/brdsx/a.md", "docs/brds/**/*.md", False),
        ("src/app/node_modules/b.js", "**/node_modules/**", True),
        ("docs/capstone/deck/a.pptx", "docs/capstone/deck/*.pptx", True),
        ("docs/capstone/deck/old/a.pptx", "docs/capstone/deck/*.pptx", False),
    ],
)
def test_given_pattern_when_glob_match_then_expected(path, pattern, expected):
    # Act
    matched = prepare.glob_match(path, pattern)

    # Assert
    assert matched is expected


def test_given_name_status_output_when_parsed_then_entries_returned():
    # Arrange
    output = b"M\0a.md\0D\0b.md\0R100\0c.md\0d.md\0"

    # Act
    entries = prepare.parse_name_status(output)

    # Assert
    assert entries == [("M", "a.md", None), ("D", "b.md", None), ("R", "c.md", "d.md")]


def test_given_rename_out_of_scope_when_classified_then_source_is_removed():
    # Arrange
    entries = [("R", "docs/brds/a.md", "docs/archive/a.md")]

    # Act
    changed, removed = prepare.classify_changes(entries, ["docs/brds/**/*.md"], [], [])

    # Assert
    assert (changed, removed) == (set(), {"docs/brds/a.md"})


def test_given_rename_within_scope_when_classified_then_target_changed_and_source_removed():
    # Arrange
    entries = [("R", REMOVED, "docs/brds/c.md")]

    # Act
    changed, removed = prepare.classify_changes(entries, ["docs/brds/**/*.md"], [], ["docs/brds/a.md", "docs/brds/c.md"])

    # Assert
    assert (changed, removed) == ({"docs/brds/c.md"}, {REMOVED})


def test_given_type_change_to_unscorable_when_classified_then_removed():
    # Arrange
    entries = [("T", REMOVED, None)]

    # Act
    changed, removed = prepare.classify_changes(entries, ["docs/brds/**/*.md"], [], ["docs/brds/a.md"])

    # Assert
    assert (changed, removed) == (set(), {REMOVED})


def hide_by_deleting(root: Path) -> bool:
    git(root, "rm", REMOVED)
    return True


def hide_by_renaming_out(root: Path) -> bool:
    (root / "docs" / "archive").mkdir()
    git(root, "mv", REMOVED, "docs/archive/b.md")
    return True


def hide_by_growing(root: Path) -> bool:
    (root / REMOVED).write_text("x" * (MAX_BYTES + 1), encoding="utf-8")
    git(root, "add", REMOVED)
    return True


def hide_by_symlink(root: Path) -> bool:
    git(root, "config", "core.symlinks", "true")
    (root / REMOVED).unlink()
    try:
        (root / REMOVED).symlink_to("a.md")
    except OSError:
        return False
    git(root, "add", REMOVED)
    return True


@pytest.mark.parametrize("hide", [hide_by_deleting, hide_by_renaming_out, hide_by_growing, hide_by_symlink])
def test_given_pr_hiding_scored_file_when_computed_then_path_is_removed(tmp_path, hide):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    if not hide(root):
        pytest.skip("symlinks are unavailable on this host")
    git(root, "commit", "-m", "hide evidence")

    # Act
    state = prepare.compute_state(root, "main", "pull_request")

    # Assert
    assert (state["changed_artifacts"], state["removed_files"]) == (["brd"], [REMOVED])


@pytest.mark.parametrize("merge_args", [["--no-ff", "--no-edit"], ["--squash"]])
def test_given_merge_deleting_scored_file_when_pushed_then_removed_detected(tmp_path, merge_args):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    git(root, "rm", REMOVED)
    git(root, "commit", "-m", "delete")
    git(root, "checkout", "main")
    git(root, "merge", *merge_args, "feature")
    if "--squash" in merge_args:
        git(root, "commit", "-m", "squash")

    # Act
    state = prepare.compute_state(root, "HEAD", "push")

    # Assert
    assert state["removed_files"] == [REMOVED]


def test_given_unchanged_main_when_computed_then_no_scoring(tmp_path):
    # Arrange
    root = make_repo(tmp_path)

    # Act
    state = prepare.compute_state(root, "HEAD", "push")

    # Assert
    assert state["should_score"] is False


@pytest.mark.parametrize(
    ("path", "artifact_id", "criteria"),
    [
        ("prototype/properwarm/domain.py", "solution-code", ["A1", "A3", "A4", "A5", "A6", "A7", "B6"]),
        ("prototype/web/app.js", "solution-code", ["A1", "A3", "A4", "A5", "A6", "A7", "B6"]),
        ("prototype/tests/test_domain.py", "solution-code", ["A1", "A3", "A4", "A5", "A6", "A7", "B6"]),
        ("prototype/scripts/build_container_seed.py", "solution-code", ["A1", "A3", "A4", "A5", "A6", "A7", "B6"]),
        ("prototype/Dockerfile", "solution-code", ["A1", "A3", "A4", "A5", "A6", "A7", "B6"]),
        ("prototype/requirements.txt", "solution-code", ["A1", "A3", "A4", "A5", "A6", "A7", "B6"]),
        ("prototype/README.md", "solution-code", ["A1", "A3", "A4", "A5", "A6", "A7", "B6"]),
        ("prototype/architecture/proper-warm-local-prototype.excalidraw", "solution-code", ["A1", "A3", "A4", "A5", "A6", "A7", "B6"]),
        ("prototype/deploy/main.bicep", "infrastructure", ["A1", "A3", "A5"]),
        ("src/app.py", "solution-code", ["A1", "A3", "A4", "A5", "A6", "A7", "B6"]),
        ("infra/main.bicep", "infrastructure", ["A1", "A3", "A5"]),
    ],
)
def test_given_registered_implementation_change_when_computed_then_expected_criteria_open(
    tmp_path, path, artifact_id, criteria
):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    candidate = root / path
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text("implementation evidence\n", encoding="utf-8")
    git(root, "add", path)
    git(root, "commit", "-m", "add implementation evidence")

    # Act
    state = prepare.compute_state(root, "main", "pull_request")

    # Assert
    assert state["should_score"] is True
    assert state["instrument_changed"] is False
    assert state["changed_artifacts"] == [artifact_id]
    assert state["changed_files"] == [path]
    assert state["open_criteria"] == criteria
    assert state["artifacts"][artifact_id]["files"] == [path]


@pytest.mark.parametrize(
    "path",
    [
        "prototype/seed/container-source/candidate-lifecycle.csv",
        "prototype/seed/container-source/safety-holds.csv",
        "prototype/seed/demo-import.xlsx",
        "prototype/properwarm/__pycache__/domain.py",
        "prototype/web/node_modules/library/index.js",
    ],
)
def test_given_generated_prototype_file_when_computed_then_no_scoring(tmp_path, path):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    candidate = root / path
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_bytes(b"generated fixture")
    git(root, "add", path)
    git(root, "commit", "-m", "add generated fixture")

    # Act
    state = prepare.compute_state(root, "main", "pull_request")

    # Assert
    assert state["should_score"] is False
    assert state["changed_artifacts"] == []
    assert state["changed_files"] == []
    assert state["open_criteria"] == []
    assert all(path not in artifact["files"] for artifact in state["artifacts"].values())


def test_given_registry_activation_in_pr_when_computed_then_base_registry_still_used(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    registry_path = root / ".github" / "rubric" / "artifacts.json"
    active_registry = registry_path.read_text(encoding="utf-8")
    planned_registry = json.loads(active_registry)
    for artifact in planned_registry["artifacts"]:
        if artifact["id"] in ("solution-code", "infrastructure"):
            artifact["status"] = "planned"
    registry_path.write_text(json.dumps(planned_registry), encoding="utf-8")
    git(root, "commit", "-am", "planned registry on main")
    git(root, "checkout", "-b", "feature")
    registry_path.write_text(active_registry, encoding="utf-8")
    candidate = root / "prototype" / "properwarm" / "domain.py"
    candidate.parent.mkdir(parents=True)
    candidate.write_text("implementation evidence\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "activate registry and add prototype")

    # Act
    state = prepare.compute_state(root, "main", "pull_request")

    # Assert
    assert state["instrument_changed"] is True
    assert state["should_score"] is True
    assert len(state["open_criteria"]) == 20
    assert state["changed_artifacts"] == []
    assert state["changed_files"] == []
    assert "solution-code" not in state["artifacts"]
    assert "infrastructure" not in state["artifacts"]


def test_given_pr_deleting_scored_file_when_gated_then_drop_counts(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    git(root, "rm", REMOVED)
    git(root, "commit", "-m", "delete")
    state = prepare.compute_state(root, "main", "pull_request")
    scores = {cid: entry["score"] for cid, entry in SEED["criteria"].items()} | {"A2": 3}
    criteria = {cid: {"score": score, "evidence": [f"{REMOVED}:1"], "rationale": "r"} for cid, score in scores.items()}
    items = [{"type": gate.TOOL_TYPE, "scorecard": json.dumps({"criteria": criteria})}]

    # Act
    result = gate.evaluate(
        state["rubric"], state["baseline"], state["bootstrap"], state["open_criteria"], state["changed_files"],
        items, "success", "success", state["removed_files"],
    )

    # Assert
    assert (state["removed_files"], result["passed"], result["total"]) == ([REMOVED], False, 59)


def test_given_direct_push_deleting_scored_file_when_computed_then_removed_detected(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "rm", REMOVED)
    git(root, "commit", "-m", "delete on main")

    # Act
    state = prepare.compute_state(root, "HEAD", "push")

    # Assert
    assert (state["should_score"], state["removed_files"]) == (True, [REMOVED])


def test_given_force_when_computed_then_all_criteria_open(tmp_path):
    # Arrange
    root = make_repo(tmp_path)

    # Act
    state = prepare.compute_state(root, "HEAD", "workflow_dispatch", force=True)

    # Assert
    assert (state["should_score"], len(state["open_criteria"])) == (True, 20)


def test_given_force_when_context_written_then_baseline_withheld(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    state = prepare.compute_state(root, "HEAD", "workflow_dispatch", force=True)

    # Act
    context = json.loads(prepare.write_context(root, state, tmp_path / "out").read_text(encoding="utf-8"))

    # Assert
    assert (context["calibration"], context["baseline"]) == (True, {"source": None, "total": None, "sections": None, "criteria": {}})


def test_given_pr_when_context_written_then_diff_base_is_merge_base(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    expected = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, check=True).stdout.decode().strip()
    git(root, "checkout", "-b", "feature")
    git(root, "rm", REMOVED)
    git(root, "commit", "-m", "delete")
    git(root, "checkout", "main")
    (root / "docs" / "other.md").write_text("main moved on\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "main moves")
    git(root, "checkout", "feature")
    state = prepare.compute_state(root, "main", "pull_request")

    # Act
    context = json.loads(prepare.write_context(root, state, tmp_path / "out").read_text(encoding="utf-8"))

    # Assert
    assert (context["diff_base"], context["removed_files"]) == (expected, [REMOVED])


def test_given_direct_push_when_context_written_then_diff_base_is_last_scores_commit(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    expected = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, check=True).stdout.decode().strip()
    git(root, "rm", REMOVED)
    git(root, "commit", "-m", "delete on main")
    (root / "docs" / "other.md").write_text("later unrelated change\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "unrelated")
    state = prepare.compute_state(root, "HEAD", "push")

    # Act
    context = json.loads(prepare.write_context(root, state, tmp_path / "out").read_text(encoding="utf-8"))

    # Assert
    assert (context["diff_base"], context["removed_files"]) == (expected, [REMOVED])


def test_given_tip_writes_scores_and_deletes_file_when_pushed_then_removed_detected(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "rm", REMOVED)
    scores = root / ".github" / "rubric" / "scores" / "latest.json"
    scores.write_text(scores.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "delete and touch scores")

    # Act
    state = prepare.compute_state(root, "HEAD", "push")

    # Assert
    assert state["removed_files"] == [REMOVED]


def test_given_stale_squash_when_pushed_then_main_side_edits_are_citable(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    (root / "docs" / "brds" / "a.md").write_text("# A edited on main\n", encoding="utf-8")
    git(root, "commit", "-am", "direct edit on main")
    (root / REMOVED).write_text("# B edited in PR\n", encoding="utf-8")
    scores = root / ".github" / "rubric" / "scores" / "latest.json"
    scores.write_text(scores.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    git(root, "commit", "-am", "squash of an out-of-date PR")

    # Act
    state = prepare.compute_state(root, "HEAD", "push")

    # Assert
    assert "docs/brds/a.md" in state["changed_files"]


def test_given_removed_file_when_context_written_then_diff_has_no_content(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    git(root, "rm", REMOVED)
    git(root, "commit", "-m", "delete")
    state = prepare.compute_state(root, "main", "pull_request")

    # Act
    prepare.write_context(root, state, tmp_path / "out")
    diff = (tmp_path / "out" / "changes.diff").read_text(encoding="utf-8")

    # Assert
    assert ("deleted file mode" in diff, "# B" in diff) == (True, False)


def test_given_rename_within_scope_when_context_written_then_diff_shows_rename(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    git(root, "mv", REMOVED, "docs/brds/c.md")
    git(root, "commit", "-m", "rename")
    state = prepare.compute_state(root, "main", "pull_request")

    # Act
    prepare.write_context(root, state, tmp_path / "out")
    diff = (tmp_path / "out" / "changes.diff").read_text(encoding="utf-8")

    # Assert
    assert ("rename from docs/brds/b.md" in diff, "new file mode" in diff) == (True, False)


def test_given_grown_file_when_context_written_then_only_stat_listed(tmp_path):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    hide_by_growing(root)
    git(root, "commit", "-m", "grow")
    state = prepare.compute_state(root, "main", "pull_request")

    # Act
    prepare.write_context(root, state, tmp_path / "out")
    diff = (tmp_path / "out" / "changes.diff").read_text(encoding="utf-8")

    # Assert
    assert ("Unscorable files (stat only)" in diff, "x" * 100 in diff) == (True, False)


def test_given_non_utf8_path_when_fingerprinted_then_no_encoding_error(tmp_path):
    # Arrange
    name = "docs/bad-\udcff.md"
    try:
        (tmp_path / "docs").mkdir()
        (tmp_path / name).write_text("x", encoding="utf-8")
    except (OSError, UnicodeError):
        pytest.skip("host file system cannot store non-UTF-8 names")

    # Act
    digest = prepare.fingerprint_files(tmp_path, [name])

    # Assert
    assert len(digest) == 64
