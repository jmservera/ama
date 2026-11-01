"""Compute rubric scoring state and prepare agent context for the rubric-score workflow.

Modes:
  decide   Print the scoring decision and write it to $GITHUB_OUTPUT when set.
  context  Write context.json, changes.diff and extracted text for the scoring agent.

Only the Python standard library is used so the script runs on a bare Actions runner.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import scorecard_adapter

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_ERROR = 2

RUBRIC_PATH = ".github/rubric/rubric.json"
REGISTRY_PATH = ".github/rubric/artifacts.json"
SCORES_PATH = ".github/rubric/scores/latest.json"
BADGE_PATH = ".github/rubric/scores/badge.svg"
WORKFLOW_PATH = ".github/workflows/rubric-score.md"
SCRIPT_PATHS = (
    ".github/rubric/scripts/prepare.py",
    ".github/rubric/scripts/gate.py",
    ".github/rubric/scripts/scorecard_adapter.py",
)
INSTRUMENT_PATHS = (RUBRIC_PATH, REGISTRY_PATH, WORKFLOW_PATH, *SCRIPT_PATHS)
MAX_DIFF_BYTES = 400_000
MAX_PPTX_UNCOMPRESSED = 200_000_000
MAX_LISTED_FILES = 500

logger = logging.getLogger(__name__)


def git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    """Run a git command in root without raising on failure."""
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)


def git_show(root: Path, ref: str, path: str) -> bytes | None:
    """Return the blob at ref:path, or None when it does not exist."""
    result = git(root, "show", f"{ref}:{path}")
    return result.stdout if result.returncode == 0 else None


def load_trusted_json(root: Path, base_ref: str, path: str) -> tuple[dict[str, Any], bool]:
    """Load JSON from the base ref, falling back to the working tree during bootstrap."""
    blob = git_show(root, base_ref, path)
    if blob is not None:
        return json.loads(blob.decode("utf-8")), True
    head_file = root / path
    if not head_file.is_file():
        raise FileNotFoundError(f"{path} not found on {base_ref} or in the working tree")
    return json.loads(head_file.read_text(encoding="utf-8")), False


@functools.lru_cache(maxsize=256)
def glob_to_regex(pattern: str) -> re.Pattern[str]:
    """Translate a repository glob to a regex where `**/` spans zero or more directories."""
    parts: list[str] = []
    index = 0
    while index < len(pattern):
        if pattern.startswith("**/", index):
            parts.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            parts.append(".*")
            index += 2
        elif pattern[index] == "*":
            parts.append("[^/]*")
            index += 1
        elif pattern[index] == "?":
            parts.append("[^/]")
            index += 1
        else:
            parts.append(re.escape(pattern[index]))
            index += 1
    return re.compile("".join(parts) + r"\Z")


def glob_match(path: str, pattern: str) -> bool:
    """Match a POSIX repository path against a glob pattern."""
    return glob_to_regex(pattern).match(path) is not None


def in_scope(path: str, include: list[str], exclude: list[str]) -> bool:
    """True when path matches an include glob and no exclude glob."""
    return any(glob_match(path, rule) for rule in include) and not any(glob_match(path, rule) for rule in exclude)


def tracked_files(root: Path) -> list[str]:
    """List files tracked in the working tree's index."""
    result = git(root, "ls-files", "-z")
    if result.returncode != 0:
        raise RuntimeError("git ls-files failed: " + result.stderr.decode("utf-8", "replace").strip())
    return [item for item in result.stdout.decode("utf-8", "surrogateescape").split("\0") if item]


def match_files(root: Path, include: list[str], exclude: list[str], max_bytes: int) -> tuple[list[str], list[str]]:
    """Return (in-scope files, in-scope files skipped for size) as sorted POSIX paths."""
    matched: list[str] = []
    oversize: list[str] = []
    for relative in tracked_files(root):
        if not in_scope(relative, include, exclude):
            continue
        candidate = root / relative
        if candidate.is_symlink() or not candidate.is_file():
            continue
        if candidate.stat().st_size > max_bytes:
            logger.warning("Skipping %s: larger than %d bytes", relative, max_bytes)
            oversize.append(relative)
            continue
        matched.append(relative)
    return sorted(matched), sorted(oversize)


def fingerprint_files(root: Path, files: list[str]) -> str:
    """Hash file paths and contents so renames and edits both change the fingerprint."""
    digest = hashlib.sha256()
    for relative in files:
        digest.update(relative.encode("utf-8", "surrogateescape"))
        digest.update(b"\0")
        digest.update((root / relative).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def differs_from_base(root: Path, base_ref: str, path: str) -> bool:
    """True when the working-tree file differs from (or is missing on) the base ref.

    Compares git object ids so line-ending conversion on checkout does not count as a change.
    """
    head_id = git(root, "hash-object", "--", path).stdout.decode("utf-8").strip() if (root / path).is_file() else ""
    base = git(root, "rev-parse", "--verify", "--quiet", f"{base_ref}:{path}")
    base_id = base.stdout.decode("utf-8").strip() if base.returncode == 0 else ""
    return head_id != base_id


def edited_by_branch(root: Path, base_ref: str, path: str) -> bool:
    """True when this branch changed the file since it forked from the base ref.

    Comparing with the current base would flag files that only changed on the base after the fork,
    such as a main-only baseline refresh that a three-way merge preserves.
    """
    fork = git(root, "merge-base", base_ref, "HEAD")
    if fork.returncode != 0 or not fork.stdout.strip():
        return differs_from_base(root, base_ref, path)
    return differs_from_base(root, fork.stdout.decode("utf-8").strip(), path)


def parse_name_status(output: bytes) -> list[tuple[str, str, str | None]]:
    """Parse `git diff --name-status -z` into (status letter, path, rename or copy target)."""
    tokens = output.decode("utf-8", "surrogateescape").split("\0")
    entries: list[tuple[str, str, str | None]] = []
    index = 0
    while index < len(tokens) and tokens[index]:
        status = tokens[index][0]
        if status in ("R", "C"):
            entries.append((status, tokens[index + 1], tokens[index + 2]))
            index += 3
        else:
            entries.append((status, tokens[index + 1], None))
            index += 2
    return entries


def usable_baseline_commit(root: Path, baseline: dict[str, Any] | None) -> str:
    """Return the baseline's recorded commit when it exists and is an ancestor of HEAD, else an empty string."""
    commit = (baseline or {}).get("commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        return ""
    if git(root, "cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
        return ""
    if git(root, "merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
        return ""
    return commit


def diff_args(root: Path, base_ref: str, event: str, baseline: dict[str, Any] | None = None) -> list[str] | None:
    """Return the git diff range that identifies changed files, or None when it cannot be resolved.

    Pull requests compare with the merge base. Other events compare with the commit the baseline
    was scored at when it is an ancestor of HEAD, so a lagging baseline refresh still covers every
    merge since. Otherwise they compare with the last commit that wrote the scores file, so direct
    pushes and squash merges are still covered.
    """
    if event == "pull_request":
        return [f"{base_ref}...HEAD"]
    scored = usable_baseline_commit(root, baseline)
    if scored:
        return [scored, "HEAD"]
    result = git(root, "log", "-1", "--format=%H", base_ref, "--", SCORES_PATH)
    commit = result.stdout.decode("utf-8").strip() if result.returncode == 0 else ""
    if not commit:
        return None
    head = git(root, "rev-parse", "HEAD").stdout.decode("utf-8").strip()
    # When the tip itself wrote the scores, compare with its first parent so its own artifact edits stay visible.
    if commit == head and git(root, "rev-parse", "--verify", "--quiet", f"{commit}^1").returncode == 0:
        return [f"{commit}^1", "HEAD"]
    return [commit, "HEAD"]


def baseline_freshness(
    root: Path, base_ref: str, baseline: dict[str, Any] | None, artifacts: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """Report how far the recorded baseline lags behind the base ref for scored paths.

    `pending` lists scored paths that changed on the base ref since the baseline commit and is None
    (unknown) when that commit is missing or is not an ancestor of the base ref.
    """
    commit = (baseline or {}).get("commit")
    commit = commit if isinstance(commit, str) else None
    result: dict[str, Any] = {"commit": commit, "known": False, "pending": None}
    if not commit or not re.fullmatch(r"[0-9a-f]{40}", commit):
        return result
    if git(root, "cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
        return result
    if git(root, "merge-base", "--is-ancestor", commit, base_ref).returncode != 0:
        return result
    diff = git(root, "diff", "--name-status", "-M", "-z", commit, base_ref)
    if diff.returncode != 0:
        return result
    touched: set[str] = set()
    for status, path, target in parse_name_status(diff.stdout):
        touched.add(path)
        if target:
            touched.add(target)
    pending = {
        path
        for path in touched
        if any(in_scope(path, artifact["include"], artifact["exclude"]) for artifact in artifacts.values())
    }
    result.update(known=True, pending=sorted(pending))
    return result


def classify_changes(
    entries: list[tuple[str, str, str | None]], include: list[str], exclude: list[str], files: list[str]
) -> tuple[set[str], set[str]]:
    """Split diff entries into (changed scorable paths, removed or unscorable paths) for one artifact.

    Any in-scope path touched by the diff that is not currently scored (deleted, renamed away,
    replaced by a symlink, grown past the size limit) counts as removed so its loss can lower scores.
    """
    touched: set[str] = set()
    for status, path, target in entries:
        if status == "R":
            touched.add(path)
            if target:
                touched.add(target)
        else:
            touched.add(target or path)
    in_scope_paths = {path for path in touched if in_scope(path, include, exclude)}
    scorable = set(files)
    return in_scope_paths & scorable, in_scope_paths - scorable


def compute_state(root: Path, base_ref: str, event: str, force: bool = False) -> dict[str, Any]:
    """Compute what changed relative to the trusted baseline and which criteria are open to rescoring."""
    rubric, rubric_from_base = load_trusted_json(root, base_ref, RUBRIC_PATH)
    registry, registry_from_base = load_trusted_json(root, base_ref, REGISTRY_PATH)

    baseline_blob = git_show(root, base_ref, SCORES_PATH)
    baseline = json.loads(baseline_blob.decode("utf-8")) if baseline_blob else None

    reasons: list[str] = []
    bootstrap = False
    if baseline is None:
        bootstrap = True
        reasons.append("no baseline on the base branch")
    elif baseline.get("source") == "manual-seed":
        bootstrap = True
        reasons.append("baseline is the manual seed")
    if baseline is not None and baseline.get("rubric_version") != rubric.get("rubric_version"):
        bootstrap = True
        reasons.append("rubric version changed; baseline is rescored without comparison")
    if not (rubric_from_base and registry_from_base):
        bootstrap = True
        reasons.append("rubric configuration not yet on the base branch")
    if force:
        reasons.append("forced calibration run")

    max_bytes = int(registry.get("max_file_bytes", 2_000_000))
    artifacts: dict[str, dict[str, Any]] = {}
    for entry in registry.get("artifacts", []):
        if entry.get("status") != "active":
            continue
        artifact_max_bytes = int(entry.get("max_file_bytes", max_bytes))
        files, _oversize = match_files(root, entry.get("include", []), entry.get("exclude", []), artifact_max_bytes)
        artifacts[entry["id"]] = {
            "title": entry.get("title", entry["id"]),
            "extractor": entry.get("extractor", "text"),
            "criteria": entry.get("criteria", []),
            "include": entry.get("include", []),
            "exclude": entry.get("exclude", []),
            "files": files,
            "fingerprint": fingerprint_files(root, files) if files else None,
        }

    previous = (baseline or {}).get("fingerprints", {})
    changed_artifacts = sorted(
        artifact_id
        for artifact_id in set(artifacts) | set(previous)
        if (artifacts.get(artifact_id) or {}).get("fingerprint") != previous.get(artifact_id)
    )
    if changed_artifacts:
        reasons.append("changed artifacts: " + ", ".join(changed_artifacts))

    range_args = diff_args(root, base_ref, event, baseline)
    entries: list[tuple[str, str, str | None]] | None = None
    if range_args is not None:
        result = git(root, "diff", "--name-status", "-M", "-z", *range_args)
        if result.returncode == 0:
            entries = parse_name_status(result.stdout)
        else:
            logger.warning("git diff failed: %s", result.stderr.decode("utf-8", "replace").strip())

    # Push and dispatch runs use HEAD as the base ref, so an instrument change on main shows only in the range.
    instrument_changed = any(differs_from_base(root, base_ref, path) for path in INSTRUMENT_PATHS)
    if not instrument_changed and event != "pull_request" and entries:
        ranged = {path for _status, path, target in entries for path in (path, target) if path}
        instrument_changed = bool(ranged & set(INSTRUMENT_PATHS))
    if instrument_changed:
        reasons.append("scoring instrument changed")
    if event == "pull_request":
        scores_file_changed = edited_by_branch(root, base_ref, SCORES_PATH)
        badge_changed = edited_by_branch(root, base_ref, BADGE_PATH)
    else:
        scores_file_changed = differs_from_base(root, base_ref, SCORES_PATH)
        badge_changed = False
    if scores_file_changed:
        reasons.append("scores file differs from the base branch")
    if badge_changed:
        reasons.append("badge differs from the base branch")
    recorded_scores_changed = event == "pull_request" and (scores_file_changed or badge_changed)
    if entries is None and changed_artifacts and not (bootstrap or force):
        raise RuntimeError("cannot determine changed files relative to the baseline; refusing to score")

    changed_files: set[str] = set()
    removed_files: set[str] = set()
    for artifact_id in changed_artifacts:
        artifact = artifacts.get(artifact_id)
        if artifact is None:
            continue
        if entries is None:
            changed_files |= set(artifact["files"])
            continue
        present, removed = classify_changes(entries, artifact["include"], artifact["exclude"], artifact["files"])
        if event != "pull_request":
            # Push ranges can miss main-side edits merged earlier (stale squash), so every scored file may be cited.
            present |= set(artifact["files"])
        changed_files |= present
        removed_files |= removed
    changed_files |= removed_files

    all_ids = [criterion["id"] for criterion in rubric["criteria"]]
    if bootstrap or force or instrument_changed:
        open_criteria = list(all_ids)
    else:
        informed = {cid for artifact_id in changed_artifacts for cid in (artifacts.get(artifact_id) or {}).get("criteria", [])}
        open_criteria = [cid for cid in all_ids if cid in informed]

    should_score = force or bootstrap or instrument_changed or scores_file_changed or badge_changed or bool(changed_artifacts)
    return {
        "event": event,
        "base_ref": base_ref,
        "rubric": rubric,
        "baseline": baseline,
        "bootstrap": bootstrap,
        "force": force,
        "instrument_changed": instrument_changed,
        "should_score": should_score,
        "reasons": reasons or ["no scored artifact changed"],
        "artifacts": artifacts,
        "fingerprints": {key: value["fingerprint"] for key, value in artifacts.items() if value["fingerprint"]},
        "diff_args": range_args,
        "removed_files": sorted(removed_files),
        "changed_artifacts": changed_artifacts,
        "changed_files": sorted(changed_files),
        "open_criteria": open_criteria,
        "recorded_scores_changed": recorded_scores_changed,
        "baseline_freshness": baseline_freshness(root, base_ref, baseline, artifacts) if baseline else None,
    }


def extract_pptx_text(path: Path) -> str:
    """Extract slide and speaker-note text from a PPTX without third-party packages."""
    namespace = "{http://schemas.openxmlformats.org/drawingml/2006/main}t"

    def slide_number(name: str) -> int:
        match = re.search(r"(\d+)\.xml$", name)
        return int(match.group(1)) if match else 0

    lines: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if sum(info.file_size for info in archive.infolist()) > MAX_PPTX_UNCOMPRESSED:
            return f"PPTX not extracted: uncompressed size exceeds {MAX_PPTX_UNCOMPRESSED} bytes.\n"
        slides = sorted((n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)), key=slide_number)
        for slide in slides:
            number = slide_number(slide)
            root = ElementTree.fromstring(archive.read(slide))
            text = " ".join(node.text for node in root.iter(namespace) if node.text)
            lines.append(f"## Slide {number}\n\n{text}\n")
            notes = f"ppt/notesSlides/notesSlide{number}.xml"
            if notes in names:
                notes_root = ElementTree.fromstring(archive.read(notes))
                notes_text = " ".join(node.text for node in notes_root.iter(namespace) if node.text)
                if notes_text.strip():
                    lines.append(f"Speaker notes: {notes_text}\n")
    return "\n".join(lines)


def unmet_requirements(rubric: dict[str, Any], artifact_counts: dict[str, int]) -> dict[str, dict[str, Any]]:
    """Map each criterion whose required evidence is absent to its forced treatment.

    `requires_any` lists artifact ids of which at least one must hold files; otherwise the
    criterion is not demonstrable and is recorded as 0. `cap_without` caps the score when one
    artifact is missing. Artifacts that are not active in the registry count as absent.
    """
    unmet: dict[str, dict[str, Any]] = {}
    for criterion in rubric["criteria"]:
        required = criterion.get("requires_any")
        cap = criterion.get("cap_without")
        if required and not any(artifact_counts.get(artifact, 0) for artifact in required):
            unmet[criterion["id"]] = {"max": 0, "missing": list(required), "mode": "any of"}
        elif cap and not artifact_counts.get(cap["artifact"], 0):
            unmet[criterion["id"]] = {"max": int(cap["max"]), "missing": [cap["artifact"]], "mode": "cap"}
    return unmet


def build_scorecard_template(
    rubric: dict[str, Any],
    baseline: dict[str, Any] | None,
    bootstrap: bool,
    calibration: bool,
    artifact_counts: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Build the complete scorecard scaffold from trusted rubric and baseline data."""
    use_baseline = not (bootstrap or calibration)
    baseline_criteria = (baseline or {}).get("criteria", {}) if use_baseline else {}
    unmet = unmet_requirements(rubric, artifact_counts) if use_baseline and artifact_counts is not None else {}
    criteria: dict[str, dict[str, Any]] = {}
    for criterion in rubric["criteria"]:
        cid = criterion["id"]
        previous = baseline_criteria.get(cid)
        if unmet.get(cid, {}).get("max") == 0:
            criteria[cid] = {
                "score": 1,
                "evidence": [],
                "rationale": "Required artifact not provided (" + ", ".join(unmet[cid]["missing"]) + "): submit 1; the gate records 0.",
                "change_reason": "",
            }
        elif (
            isinstance(previous, dict)
            and isinstance(previous.get("score"), int)
            and not isinstance(previous.get("score"), bool)
            and 1 <= previous["score"] <= 5
        ):
            criteria[cid] = {
                "score": previous["score"],
                "evidence": list(previous.get("evidence", [])),
                "rationale": previous.get("rationale", ""),
                "change_reason": "",
            }
        else:
            criteria[cid] = {
                "score": None,
                "evidence": [],
                "rationale": "UNSCORED: assess from the rubric and repository evidence.",
                "change_reason": "",
            }
    return {"criteria": criteria, "summary": ""}


def write_context(root: Path, state: dict[str, Any], out_dir: Path) -> Path:
    """Write the agent context bundle and return the context.json path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    extracted: dict[str, str] = {}
    for artifact in state["artifacts"].values():
        if artifact["extractor"] != "pptx":
            continue
        for relative in artifact["files"]:
            target = out_dir / "extracted" / (re.sub(r"[^A-Za-z0-9._-]", "_", relative) + ".md")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(extract_pptx_text(root / relative), encoding="utf-8")
            extracted[relative] = target.as_posix()

    diff_path = out_dir / "changes.diff"
    # Only paths that still exist but cannot be scored (oversize, symlink) are reduced to a stat line.
    unscorable = {path for path in state["removed_files"] if (root / path).exists() or (root / path).is_symlink()}
    present = [path for path in state["changed_files"] if path not in unscorable]
    if state["diff_args"] and (present or unscorable):
        diff = git(root, "diff", "-M", "-D", *state["diff_args"], "--", *present).stdout if present else b""
        if unscorable:
            stat = git(root, "diff", "-M", "--stat", *state["diff_args"], "--", *sorted(unscorable)).stdout
            diff = b"# Unscorable files (stat only)\n" + stat + b"\n" + diff
        diff_path.write_bytes(diff[:MAX_DIFF_BYTES])
    else:
        diff_path.write_text("", encoding="utf-8")

    baseline = {} if state["force"] or state["bootstrap"] else (state["baseline"] or {})
    diff_base = ""
    if state["diff_args"]:
        first = state["diff_args"][0]
        if "..." in first:
            merge_base = git(root, "merge-base", first.split("...")[0], "HEAD")
            diff_base = merge_base.stdout.decode("utf-8").strip() if merge_base.returncode == 0 else ""
        else:
            diff_base = first
    context = {
        "event": state["event"],
        "rubric_guide": state["rubric"].get("guide"),
        "rubric_config": RUBRIC_PATH,
        "bootstrap": state["bootstrap"],
        "calibration": state["force"],
        "instrument_changed": state["instrument_changed"],
        "reasons": state["reasons"],
        "open_criteria": state["open_criteria"],
        "changed_artifacts": state["changed_artifacts"],
        "changed_files": state["changed_files"],
        "removed_files": state["removed_files"],
        "diff_range": " ".join(state["diff_args"] or []),
        "diff_base": diff_base,
        "changes_diff": diff_path.as_posix(),
        "artifacts": {
            key: {
                "title": value["title"],
                "criteria": value["criteria"],
                "files": value["files"][:MAX_LISTED_FILES],
                "file_count": len(value["files"]),
            }
            for key, value in state["artifacts"].items()
        },
        "extracted_text": extracted,
        "live_criteria": [c["id"] for c in state["rubric"]["criteria"] if c.get("live")],
        "unmet_requirements": unmet_requirements(
            state["rubric"], {key: len(value["files"]) for key, value in state["artifacts"].items()}
        ),
        "scorecard_template": build_scorecard_template(
            state["rubric"],
            baseline,
            state["bootstrap"],
            state["force"],
            {key: len(value["files"]) for key, value in state["artifacts"].items()},
        ),
        "baseline": {
            "source": baseline.get("source"),
            "total": baseline.get("total"),
            "sections": baseline.get("sections"),
            "criteria": baseline.get("criteria", {}),
        },
    }
    context_path = out_dir / "context.json"
    context["tool_inputs_template"] = scorecard_adapter.to_inputs(
        context["scorecard_template"], [criterion["id"] for criterion in state["rubric"]["criteria"]]
    )
    context_path.write_text(json.dumps(context, indent=2), encoding="utf-8")
    return context_path


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=["decide", "context"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--base-ref", required=True, help="Trusted ref holding the baseline, e.g. origin/main")
    parser.add_argument("--event", default=os.environ.get("GITHUB_EVENT_NAME", "workflow_dispatch"))
    parser.add_argument("--out", type=Path, default=Path("/tmp/gh-aw/agent/rubric"))
    parser.add_argument("--force", action="store_true", help="Calibration run: rescore every criterion, report only")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def main() -> int:
    """Entry point."""
    args = create_parser().parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s: %(message)s")
    root = args.root.resolve()
    try:
        state = compute_state(root, args.base_ref, args.event, args.force)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, RuntimeError, UnicodeError) as error:
        logger.error("Cannot compute rubric state: %s", error)
        return EXIT_ERROR

    baseline_total = (state["baseline"] or {}).get("total", "")
    summary = {
        "should_score": state["should_score"],
        "bootstrap": state["bootstrap"],
        "baseline_total": baseline_total,
        "reasons": state["reasons"],
        "changed_artifacts": state["changed_artifacts"],
        "removed_files": state["removed_files"],
        "open_criteria": state["open_criteria"],
    }
    print(json.dumps(summary, indent=2))

    if args.mode == "decide":
        output_file = os.environ.get("GITHUB_OUTPUT")
        if output_file:
            with open(output_file, "a", encoding="utf-8") as handle:
                handle.write(f"should_score={'true' if state['should_score'] else 'false'}\n")
                handle.write(f"bootstrap={'true' if state['bootstrap'] else 'false'}\n")
                handle.write(f"baseline_total={baseline_total}\n")
                handle.write(f"reason={'; '.join(state['reasons'])}\n")
        return EXIT_SUCCESS

    context_path = write_context(root, state, args.out)
    logger.info("Wrote %s", context_path)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
