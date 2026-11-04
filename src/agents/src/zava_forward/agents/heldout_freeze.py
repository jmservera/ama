"""Offline pre-evaluation freeze check for a held-out AI evaluation (#108).

Checks that a freeze manifest records, before any evaluation, the task, model, prompt, policy and
source versions, an independently labelled held-out split with seed and denominators, expected
outcomes, critical-error definitions, cohorts, sufficient samples and named threshold approval,
and that held-out answers never overlap prompt or tuning material. The result is ``frozen`` or
``insufficient`` with every gap listed, plus a content digest. A frozen manifest only permits an
evaluation to start; it is not an evaluation, an approval of a model, or authority for actual
calls, which need separate finite authorization. Constructed fixtures are not held-out proof.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from zava_forward.core.rai_release import digest, named

VERSION_KEYS = ("task", "model", "prompt", "policy", "source")
THRESHOLD_KEYS = ("max_critical_misses", "min_accuracy", "min_sample_per_cohort")
NOTE = (
    "Freeze check only: it does not evaluate a model, approve a threshold or authorize actual "
    "calls. Constructed fixtures are not independently labelled held-out evidence."
)


def _ids(value: Any) -> list[str] | None:
    if not isinstance(value, Sequence) or isinstance(value, str):
        return None
    return list(value) if all(isinstance(i, str) and i.strip() for i in value) else None


def _versions(manifest: Mapping[str, Any]) -> list[str]:
    versions = manifest.get("versions")
    if not isinstance(versions, Mapping):
        return ["versions missing"]
    return [f"versions.{key} not recorded" for key in VERSION_KEYS if not named(versions.get(key))]


def _split(manifest: Mapping[str, Any], gaps: list[str]) -> list[str]:
    held = manifest.get("held_out")
    if not isinstance(held, Mapping):
        gaps.append("held_out split missing")
        return []
    ids = _ids(held.get("case_ids"))
    if not ids:
        gaps.append("held_out.case_ids missing or invalid")
        ids = []
    elif len(set(ids)) != len(ids):
        gaps.append("held_out.case_ids contains duplicates")
    if not named(held.get("seed")):
        gaps.append("held_out.seed not recorded")
    if held.get("denominator") != len(ids):
        gaps.append("held_out.denominator does not equal the number of case ids")
    labeller, author = held.get("labelled_by"), held.get("prompt_author")
    if not named(labeller):
        gaps.append("held_out.labelled_by not recorded")
    elif not named(author):
        gaps.append("held_out.prompt_author not recorded, independence unproven")
    elif str(labeller).strip().casefold() == str(author).strip().casefold():
        gaps.append("held_out labeller is not independent of the prompt author")
    expected, critical = held.get("expected"), held.get("critical_errors")
    if (
        not isinstance(expected, Mapping)
        or set(expected) != set(ids)
        or not all(named(v) for v in expected.values())
    ):
        gaps.append("expected outcome missing for a held-out case or not matching the case ids")
    if not (
        isinstance(critical, Sequence) and not isinstance(critical, str) and critical
    ) or not all(named(c) for c in critical):
        gaps.append("critical errors not defined")
    return ids


def _leakage(manifest: Mapping[str, Any], ids: list[str], gaps: list[str]) -> None:
    prompt_ids = _ids(manifest.get("prompt_case_ids"))
    tuning_ids = _ids(manifest.get("tuning_case_ids"))
    if prompt_ids is None or tuning_ids is None:
        gaps.append("prompt_case_ids and tuning_case_ids must be recorded, even when empty")
        return
    overlap = sorted(set(ids) & (set(prompt_ids) | set(tuning_ids)))
    if overlap:
        gaps.append("held-out answers overlap prompt or tuning cases: " + ", ".join(overlap))


def _cohorts(
    manifest: Mapping[str, Any], ids: list[str], limits: Mapping[str, Any], gaps: list[str]
) -> None:
    cohorts = manifest.get("cohorts")
    if not isinstance(cohorts, Mapping) or not cohorts:
        gaps.append("cohorts not declared")
        return
    minimum = limits.get("min_sample_per_cohort")
    for name, members in sorted(cohorts.items()):
        listed = _ids(members)
        if listed is None or not set(listed) <= set(ids):
            gaps.append(f"cohort {name} is not a subset of the held-out cases")
        elif isinstance(minimum, int) and not isinstance(minimum, bool) and len(listed) < minimum:
            gaps.append(f"cohort {name} has {len(listed)} cases, below the minimum {minimum}")


def _thresholds(manifest: Mapping[str, Any], gaps: list[str]) -> Mapping[str, Any]:
    limits = manifest.get("thresholds")
    if not isinstance(limits, Mapping):
        gaps.append("thresholds missing")
        return {}
    for key in THRESHOLD_KEYS:
        value = limits.get(key)
        if isinstance(value, bool) or not isinstance(value, int | float) or value < 0:
            gaps.append(f"thresholds.{key} not a non-negative number")
    approval = manifest.get("threshold_approval")
    bound = isinstance(approval, Mapping) and approval.get("manifest_digest") == _digest(manifest)
    if not (isinstance(approval, Mapping) and named(approval.get("by")) and bound):
        gaps.append("thresholds lack named approval bound to the manifest digest")
    return limits


def _digest(manifest: Mapping[str, Any]) -> str:
    return str(digest({k: v for k, v in manifest.items() if k != "threshold_approval"}))


def check_freeze(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Return ``frozen`` only when every freeze requirement is recorded and consistent."""
    gaps = _versions(manifest)
    ids = _split(manifest, gaps)
    _leakage(manifest, ids, gaps)
    limits = _thresholds(manifest, gaps)
    _cohorts(manifest, ids, limits, gaps)
    return dict(
        outcome="insufficient" if gaps else "frozen",
        gaps=gaps,
        manifest_digest=_digest(manifest),
        held_out_cases=len(ids),
        note=NOTE,
    )
