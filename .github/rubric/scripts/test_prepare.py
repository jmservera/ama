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


def make_repo(root: Path, artifact_max_bytes: int | None = None) -> Path:
    """Create a repo on main with two BRD files and a workflow baseline that matches them."""
    git(root, "init", "-b", "main")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "test")
    config = root / ".github" / "rubric"
    (config / "scores").mkdir(parents=True)
    shutil.copy(RUBRIC_DIR / "rubric.json", config / "rubric.json")
    registry = json.loads((RUBRIC_DIR / "artifacts.json").read_text(encoding="utf-8"))
    registry["max_file_bytes"] = MAX_BYTES
    if artifact_max_bytes is not None:
        next(entry for entry in registry["artifacts"] if entry["id"] == "brd")["max_file_bytes"] = artifact_max_bytes
    (config / "artifacts.json").write_text(json.dumps(registry), encoding="utf-8")
    (root / "docs" / "brds").mkdir(parents=True)
    (root / "docs" / "brds" / "a.md").write_text("# A\n", encoding="utf-8")
    (root / REMOVED).write_text("# B\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "content")
    files, _ = prepare.match_files(root, ["docs/brds/**/*.md"], [], MAX_BYTES)
    baseline = dict(SEED, source="workflow", rubric_version=json.loads((RUBRIC_DIR / "rubric.json").read_text(encoding="utf-8")).get("rubric_version"), fingerprints={"brd": prepare.fingerprint_files(root, files)})
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
    ("limit", "size", "expected"),
    [(None, MAX_BYTES + 1, False), (1500, 1500, True), (1500, 1501, False)],
)
def test_given_deck_size_override_when_computed_then_only_deck_limit_changes(
    tmp_path, limit, size, expected
):
    root = make_repo(tmp_path)
    registry_path = root / prepare.REGISTRY_PATH
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    deck_entry = next(entry for entry in registry["artifacts"] if entry["id"] == "capstone-deck")
    deck_entry.pop("max_file_bytes", None)
    if limit is not None:
        deck_entry["max_file_bytes"] = limit
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    deck_path = "docs/capstone/deck/zava-forward-cowork-v2-draft.pptx"
    (root / deck_path).parent.mkdir(parents=True)
    (root / deck_path).write_bytes(b"x" * size)
    (root / "docs/brds/oversize.md").write_bytes(b"x" * (MAX_BYTES + 1))
    git(root, "add", ".")
    git(root, "commit", "-m", "configure deck size limit")

    state = prepare.compute_state(root, "HEAD", "push")

    assert (deck_path in state["artifacts"]["capstone-deck"]["files"]) is expected
    assert "docs/brds/oversize.md" not in state["artifacts"]["brd"]["files"]


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("docs/capstone/deck/zava-forward-cowork-v2-draft.pptx", True),
        ("docs/capstone/deck/zava-forward-executive-draft.pptx", False),
        ("docs/capstone/deck/cowork-generated/Zava Forward - More homes ready with control intact.pptx", False),
    ],
)
def test_given_cowork_registry_when_matching_then_only_current_deck_selected(path, expected):
    registry = json.loads((RUBRIC_DIR / "artifacts.json").read_text(encoding="utf-8"))
    deck_entry = next(entry for entry in registry["artifacts"] if entry["id"] == "capstone-deck")

    matched = prepare.in_scope(path, deck_entry["include"], deck_entry["exclude"])

    assert matched is expected

@pytest.mark.parametrize(
    ("artifact_max_bytes", "file_size", "expected"),
    [
        (MAX_BYTES * 2, MAX_BYTES + 1, True),
        (MAX_BYTES * 2, MAX_BYTES * 2, True),
        (MAX_BYTES * 2, MAX_BYTES * 2 + 1, False),
        (None, MAX_BYTES + 1, False),
    ],
    ids=["above-global-limit", "at-artifact-limit", "above-artifact-limit", "global-fallback"],
)
def test_given_artifact_file_size_when_computed_then_configured_limit_applies(
    tmp_path, artifact_max_bytes, file_size, expected
):
    # Arrange
    root = make_repo(tmp_path, artifact_max_bytes)
    git(root, "checkout", "-b", "feature")
    path = "docs/brds/large.md"
    (root / path).write_text("x" * file_size, encoding="utf-8")
    git(root, "add", path)
    git(root, "commit", "-m", "add sized artifact")

    # Act
    state = prepare.compute_state(root, "main", "pull_request")

    # Assert
    assert (path in state["artifacts"]["brd"]["files"]) is expected


@pytest.mark.parametrize(
    ("path", "artifact_id", "criteria"),
    [
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
        "src/core/src/zava_forward/core/config.py",
        "src/core/tests/test_config.py",
        "src/core/pyproject.toml",
        "src/api/Dockerfile",
        "src/api/src/zava_forward/api/web/app.js",
    ],
)
def test_given_src_project_file_when_computed_then_solution_code_opens(tmp_path, path):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    candidate = root / path
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text("implementation evidence\n", encoding="utf-8")
    git(root, "add", path)
    git(root, "commit", "-m", "add src file")

    # Act
    state = prepare.compute_state(root, "main", "pull_request")

    # Assert
    assert state["should_score"] is True
    assert state["changed_artifacts"] == ["solution-code"]
    assert state["changed_files"] == [path]
    assert state["artifacts"]["solution-code"]["files"] == [path]


@pytest.mark.parametrize(
    "path",
    [
        "src/api/src/zava_forward/api/web/vendor/lib.js",
        "src/core/data/private-cases.csv",
        "src/core/src/zava_forward/core/data/cases.json",
        "src/core/src/zava_forward.egg-info/PKG-INFO",
        "src/core/build/lib/zava_forward/core.py",
    ],
)
def test_given_src_vendor_data_or_build_file_when_computed_then_no_scoring(tmp_path, path):
    # Arrange
    root = make_repo(tmp_path)
    git(root, "checkout", "-b", "feature")
    candidate = root / path
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text("excluded fixture\n", encoding="utf-8")
    git(root, "add", path)
    git(root, "commit", "-m", "add excluded fixture")

    # Act
    state = prepare.compute_state(root, "main", "pull_request")

    # Assert
    assert state["should_score"] is False
    assert state["changed_files"] == []
    assert all(path not in artifact["files"] for artifact in state["artifacts"].values())


@pytest.mark.parametrize(
    "path",
    [
        "src/api/data/candidate-lifecycle.csv",
        "src/core/data/demo-import.xlsx",
        "src/core/__pycache__/domain.py",
        "src/api/web/vendor/library/index.js",
        "src/api/web/node_modules/library/index.js",
    ],
)
def test_given_generated_file_when_computed_then_no_scoring(tmp_path, path):
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
    candidate = root / "prototype" / "zavaforward" / "domain.py"
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
    assert (state["removed_files"], result["passed"], result["total"]) == ([REMOVED], False, 64)


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
    rubric = prepare.load_trusted_json(root, "HEAD", prepare.RUBRIC_PATH)[0]
    assert list(context["scorecard_template"]["criteria"]) == [criterion["id"] for criterion in rubric["criteria"]]
    assert all(entry["score"] is None and entry["rationale"].startswith("UNSCORED:") for entry in context["scorecard_template"]["criteria"].values())


def test_given_incremental_context_when_scaffold_built_then_all_baseline_fields_are_copied_without_mutation(tmp_path):
    root = make_repo(tmp_path)
    state = prepare.compute_state(root, "HEAD", "push")
    baseline = json.loads(json.dumps(state["baseline"]))
    template = prepare.build_scorecard_template(state["rubric"], state["baseline"], False, False)

    assert list(template["criteria"]) == [criterion["id"] for criterion in state["rubric"]["criteria"]]
    assert template["criteria"]["A2"] == {
        "score": baseline["criteria"]["A2"]["score"],
        "evidence": baseline["criteria"]["A2"]["evidence"],
        "rationale": baseline["criteria"]["A2"]["rationale"],
        "change_reason": "",
    }
    assert state["baseline"] == baseline


def test_given_bootstrap_context_when_written_then_template_is_unscored_and_seed_is_withheld(tmp_path):
    root = make_repo(tmp_path)
    git(root, "rm", ".github/rubric/scores/latest.json")
    git(root, "commit", "-m", "remove baseline for bootstrap")
    state = prepare.compute_state(root, "HEAD", "push")

    context = json.loads(prepare.write_context(root, state, tmp_path / "out").read_text(encoding="utf-8"))

    assert context["bootstrap"] is True
    assert context["baseline"]["criteria"] == {}
    assert list(context["scorecard_template"]["criteria"]) == [criterion["id"] for criterion in state["rubric"]["criteria"]]
    assert all(entry["score"] is None and entry["rationale"].startswith("UNSCORED:") for entry in context["scorecard_template"]["criteria"].values())


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
