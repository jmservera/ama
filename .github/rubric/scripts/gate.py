"""Deterministic rubric gate for the rubric-score workflow.

Reads the agent's single `record_rubric_score` safe output, validates it, carries forward
criteria that no changed artifact informs, computes totals, floors and outcome, compares the
total with the baseline on the base branch, and writes decision.json, report.md and latest.json.
The pass or fail decision is made here, never by the agent.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
import posixpath
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prepare  # noqa: E402
import scorecard_adapter  # noqa: E402

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_ERROR = 2

TOOL_TYPE = "record_rubric_score"
MAX_TEXT = 300
MAX_EVIDENCE = 10
COMMENT_MARKER = "<!-- rubric-score -->"

logger = logging.getLogger(__name__)


ZWSP = "\u200b"


def clean_text(text: Any, limit: int = MAX_TEXT) -> str:
    """Neutralise links, URLs, mentions and issue references in untrusted text; idempotent."""
    value = re.sub(r"[\x00-\x1f\x7f]", " ", str(text or ""))
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\]\(", f"]{ZWSP}(", value)
    value = re.sub(r"!\[", f"!{ZWSP}[", value)
    value = re.sub(r"://", f":{ZWSP}//", value)
    value = re.sub(f"@(?!{ZWSP})", f"@{ZWSP}", value)
    value = re.sub(f"#(?!{ZWSP})(?=\\d)", f"#{ZWSP}", value)
    value = re.sub(r"\bwww\.", f"www{ZWSP}.", value, flags=re.IGNORECASE)
    value = re.sub(r"\bGH-(?=\d)", f"GH{ZWSP}-", value, flags=re.IGNORECASE)
    value = re.sub(f"(?<![0-9A-Za-z{ZWSP}])([0-9a-f]{{4}})([0-9a-f]{{3,36}})(?![0-9A-Za-z])", f"\\1{ZWSP}\\2", value)
    return value if len(value) <= limit else value[: limit - 3] + "..."


def sanitize(text: Any, limit: int = MAX_TEXT) -> str:
    """Make untrusted agent text safe for a Markdown table cell."""
    value = clean_text(text, limit)
    return value.replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")


def evidence_path(reference: str) -> str:
    """Normalise an evidence reference to a repository-relative POSIX path without line anchors."""
    value = reference.strip().replace("\\", "/")
    workspace = os.environ.get("GITHUB_WORKSPACE", "").replace("\\", "/").rstrip("/")
    if workspace and value.startswith(workspace + "/"):
        value = value[len(workspace) + 1 :]
    value = re.sub(r"#L\d+(-L?\d+)?$", "", value)
    value = re.sub(r"(:L?\d+(-L?\d+)?)+$", "", value)
    value = posixpath.normpath(value.lstrip("/"))
    return "" if value == "." else value


def outcome_label(rubric: dict[str, Any], total: int, floors_met: bool, submitted: bool = True) -> str:
    """Return the rubric outcome band, honouring the floor check first."""
    if not submitted:
        return rubric["submission_required"]["outcome"]
    if not floors_met:
        return "Not Yet Met (floor)"
    for band in sorted(rubric["outcome_bands"], key=lambda item: item["min"], reverse=True):
        if total >= band["min"]:
            return band["label"]
    return "Not Yet Met"


def parse_scorecard(items: list[dict[str, Any]], criterion_ids: list[str]) -> tuple[dict[str, Any] | None, str | None]:
    """Validate exactly one scorecard item and return its criteria, or an error message."""
    calls = [item for item in items if item.get("type") == TOOL_TYPE]
    if len(calls) != 1:
        return None, f"expected exactly one {TOOL_TYPE} call, found {len(calls)}"
    call = calls[0]
    if "scorecard" not in call:
        try:
            raw = scorecard_adapter.from_inputs(
                {key: value for key, value in call.items() if key != "type"}, criterion_ids
            )
        except ValueError as error:
            return None, str(error)
    else:
        # Previously recorded canonical cards remain readable during main-first activation.
        if set(call) != {"type", "scorecard"}:
            return None, "canonical scorecard call contains unknown fields"
        raw = call["scorecard"]
    try:
        scorecard = json.loads(raw) if isinstance(raw, str) else raw
    except json.JSONDecodeError as error:
        return None, f"scorecard is not valid JSON: {error}"
    if not isinstance(scorecard, dict) or not isinstance(scorecard.get("criteria"), dict):
        return None, "scorecard must be an object with a 'criteria' object"

    criteria: dict[str, Any] = {}
    for cid in criterion_ids:
        entry = scorecard["criteria"].get(cid)
        if not isinstance(entry, dict):
            return None, f"criterion {cid} is missing"
        score = entry.get("score")
        if isinstance(score, bool) or not isinstance(score, int) or not 1 <= score <= 5:
            return None, f"criterion {cid} score must be an integer from 1 to 5"
        evidence = entry.get("evidence", [])
        if not isinstance(evidence, list) or not all(isinstance(item, str) for item in evidence):
            return None, f"criterion {cid} evidence must be a list of strings"
        criteria[cid] = {
            "score": score,
            "evidence": [item[:200] for item in evidence[:MAX_EVIDENCE]],
            "rationale": str(entry.get("rationale", ""))[:1000],
            "change_reason": str(entry.get("change_reason", ""))[:1000],
        }
    extra = set(scorecard["criteria"]) - set(criterion_ids)
    if extra:
        return None, "unknown criteria: " + ", ".join(sorted(extra))
    return {"criteria": criteria, "summary": str(scorecard.get("summary", ""))[:2000]}, None


def evaluate(
    rubric: dict[str, Any],
    baseline: dict[str, Any] | None,
    bootstrap: bool,
    open_criteria: list[str],
    changed_files: list[str],
    items: list[dict[str, Any]],
    agent_result: str,
    detection_result: str,
    removed_files: list[str] | None = None,
    calibration: bool = False,
    artifact_counts: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Pure gate decision; see module docstring.

    Removed paths can justify a lower score only. Calibration runs score from scratch and skip the comparison.
    """
    criterion_ids = [c["id"] for c in rubric["criteria"]]
    baseline_total = (baseline or {}).get("total")
    result: dict[str, Any] = {
        "valid": False,
        "passed": False,
        "bootstrap": bootstrap,
        "calibration": calibration,
        "baseline_total": baseline_total,
        "warnings": [],
    }

    if agent_result != "success":
        result["error"] = f"agent job result was '{agent_result}'"
        return result
    if detection_result not in ("", "success"):
        result["error"] = f"threat detection result was '{detection_result}'"
        return result

    scorecard, error = parse_scorecard(items, criterion_ids)
    if error or scorecard is None:
        result["error"] = error
        return result

    baseline_criteria = (baseline or {}).get("criteria", {})
    removed = set(removed_files or [])
    present = set(changed_files) - removed
    final: dict[str, Any] = {}
    for cid in criterion_ids:
        proposed = scorecard["criteria"][cid]
        previous = baseline_criteria.get(cid)
        if bootstrap or calibration or previous is None:
            final[cid] = proposed
            continue
        if cid not in open_criteria:
            final[cid] = previous
            if proposed["score"] != previous.get("score"):
                result["warnings"].append(f"{cid}: change ignored, no changed artifact informs this criterion")
            continue
        allowed = present | removed if proposed["score"] < previous.get("score", 0) else present
        if proposed["score"] != previous.get("score") and not any(evidence_path(ref) in allowed for ref in proposed["evidence"]):
            final[cid] = previous
            result["warnings"].append(f"{cid}: change ignored, evidence cites no changed file")
            continue
        final[cid] = proposed

    if artifact_counts is not None:
        for cid, rule in prepare.unmet_requirements(rubric, artifact_counts).items():
            if final[cid]["score"] > rule["max"]:
                reason = "required artifact not provided: " + ", ".join(rule["missing"])
                result["warnings"].append(f"{cid}: score forced from {final[cid]['score']} to {rule['max']}, {reason}")
                final[cid] = {
                    **final[cid],
                    "score": rule["max"],
                    "evidence": [] if rule["max"] == 0 else final[cid]["evidence"],
                    "rationale": f"Not demonstrable: {reason}. Maximum {rule['max']} until it is committed.",
                }

    sections = {key: 0 for key in rubric["sections"]}
    for criterion in rubric["criteria"]:
        sections[criterion["section"]] += final[criterion["id"]]["score"]
    total = sum(sections.values())
    required = rubric.get("submission_required") or {}
    submitted = not required or artifact_counts is None or bool(artifact_counts.get(required["artifact"], 0))
    floors_met = submitted and all(sections[key] >= value["floor"] for key, value in rubric["sections"].items()) and all(
        entry["score"] > 1 for entry in final.values()
    )
    drops = [
        cid
        for cid in criterion_ids
        if baseline_criteria.get(cid) and final[cid]["score"] < baseline_criteria[cid].get("score", 0)
    ]
    for cid in drops:
        result["warnings"].append(f"{cid}: dropped from {baseline_criteria[cid]['score']} to {final[cid]['score']}")

    passed = calibration or bootstrap or baseline_total is None or total >= baseline_total
    result.update(
        {
            "valid": True,
            "passed": passed,
            "total": total,
            "sections": sections,
            "floors_met": floors_met,
            "outcome": outcome_label(rubric, total, floors_met, submitted),
            "criteria": final,
            "drops": drops,
            "summary": scorecard["summary"],
        }
    )
    return result


def render_report(rubric: dict[str, Any], baseline: dict[str, Any] | None, result: dict[str, Any], run_url: str) -> str:
    """Render the sticky PR comment and job summary."""
    lines = [COMMENT_MARKER]
    baseline_total = result.get("baseline_total")
    if not result["valid"]:
        lines += [
            "## Rubric score: FAILED",
            "",
            f"The gate could not record a score: {sanitize(result.get('error'))}.",
            "",
            f"[Workflow run]({run_url})" if run_url else "",
        ]
        return "\n".join(lines) + "\n"

    verdict = "PASS" if result["passed"] else "FAIL"
    if result.get("calibration"):
        basis, verdict = f"calibration run, baseline {baseline_total}/100, not recorded", "INFO"
    elif result["bootstrap"]:
        basis = "bootstrap run, comparison skipped"
    else:
        basis = f"baseline {baseline_total}/100"
    lines += [
        f"## Rubric score: {result['total']}/100 ({basis}) {verdict}",
        "",
        f"Outcome band: {result['outcome']}. Readiness estimate from repository evidence, not a panel prediction.",
        "",
        "| Section | Score | Max | Floor |",
        "|---------|------:|----:|------:|",
    ]
    for key, section in rubric["sections"].items():
        lines.append(f"| {key}. {section['title']} | {result['sections'][key]} | {section['max']} | {section['floor']} |")
    lines += ["", "| Criterion | Baseline | New | Rationale |", "|-----------|---------:|----:|-----------|"]
    baseline_criteria = (baseline or {}).get("criteria", {})
    for criterion in rubric["criteria"]:
        cid = criterion["id"]
        before = baseline_criteria.get(cid, {}).get("score", "")
        entry = result["criteria"][cid]
        live = " (live)" if criterion.get("live") else ""
        lines.append(f"| {cid} {criterion['title']}{live} | {before} | {entry['score']} | {sanitize(entry.get('rationale'))} |")
    if result["warnings"]:
        lines += ["", "### Warnings", ""] + [f"* {sanitize(item)}" for item in result["warnings"]]
    if result.get("summary"):
        lines += ["", "### Scorer summary", "", sanitize(result["summary"], 1500)]
    if run_url:
        lines += ["", f"[Workflow run]({run_url})"]
    return "\n".join(lines) + "\n"


def build_scores_file(
    result: dict[str, Any], fingerprints: dict[str, str], commit: str, model: str, run_url: str, rubric_version: int | None = None
) -> dict[str, Any]:
    """Build the next latest.json content."""
    return {
        "schema_version": 1,
        "rubric_version": rubric_version,
        "source": "workflow",
        "scored_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "commit": commit or None,
        "model": model or None,
        "run_url": run_url or None,
        "fingerprints": fingerprints,
        "total": result["total"],
        "sections": result["sections"],
        "floors_met": result["floors_met"],
        "outcome": result["outcome"],
        "criteria": {
            cid: {
                "score": entry["score"],
                "evidence": [clean_text(ref, 200) for ref in entry.get("evidence", [])],
                "rationale": clean_text(entry.get("rationale", "")),
            }
            for cid, entry in result["criteria"].items()
        },
    }


def load_items(agent_output: Path | None) -> list[dict[str, Any]]:
    """Read safe-output items; a missing or unreadable file yields no items."""
    if agent_output is None or not agent_output.is_file():
        return []
    try:
        data = json.loads(agent_output.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    items = data.get("items", []) if isinstance(data, dict) else []
    return [item for item in items if isinstance(item, dict)]


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--agent-output", type=Path)
    parser.add_argument("--agent-result", default="success")
    parser.add_argument("--detection-result", default="")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--commit", default="")
    parser.add_argument("--model", default="")
    parser.add_argument("--run-url", default="")
    parser.add_argument("--force", action="store_true", help="Calibration run: report only, never write latest.json")
    return parser


def main() -> int:
    """Entry point."""
    args = create_parser().parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    root = args.root.resolve()
    try:
        state = prepare.compute_state(root, args.base_ref, args.event, args.force)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, RuntimeError, UnicodeError) as error:
        logger.error("Cannot compute rubric state: %s", error)
        return EXIT_ERROR

    result = evaluate(
        state["rubric"],
        state["baseline"],
        state["bootstrap"],
        state["open_criteria"],
        state["changed_files"],
        load_items(args.agent_output),
        args.agent_result,
        args.detection_result,
        state["removed_files"],
        args.force,
        {key: len(value["files"]) for key, value in state["artifacts"].items()},
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)
    report = render_report(state["rubric"], state["baseline"], result, args.run_url)
    (args.out_dir / "report.md").write_text(report, encoding="utf-8")
    if result["valid"] and not args.force:
        scores = build_scores_file(result, state["fingerprints"], args.commit, args.model, args.run_url, state["rubric"].get("rubric_version"))
        (args.out_dir / "latest.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    decision = {
        key: result.get(key)
        for key in ("valid", "passed", "bootstrap", "calibration", "total", "baseline_total", "outcome", "drops", "error")
    }
    (args.out_dir / "decision.json").write_text(json.dumps(decision, indent=2), encoding="utf-8")
    print(json.dumps(decision, indent=2))
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
