"""Pure paired-cohort check: missing data or need must never lower priority (#128, AC-073).

Each constructed pair holds every relevant fact constant and changes one attribute: sensor
completeness, support or contact need, or appointment history. A pair passes only when the
subject case is ranked no lower than its reference and its human-review route has no rank effect.
Results are kept per dimension and are never averaged. Seeded defects that go undetected are
reported. Constructed pairs are not population fairness evidence. No store, clock or network.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from zava_forward.core import journey_register, ranking
from zava_forward.core.rai_release import digest

RECORD_VERSION = "paired-equity-check-v1"
DIMENSIONS = ("sensor_completeness", "support_or_contact_need", "appointment_history")
Ranker = Callable[[Sequence[Mapping[str, Any]]], Sequence[Mapping[str, Any]]]
GAP = (
    "Pair expectations, ranking-policy ownership and thresholds need independent human approval "
    "(OQ-018); this check is not fairness evidence and approves nothing."
)


def _position(case: Mapping[str, Any], anchors: Sequence[Mapping[str, Any]], rank: Ranker) -> int:
    ordered = rank([*anchors, case])
    return next(int(e["rank"]) for e in ordered if e["id"] == case["id"])


def _check_pair(
    pair: Mapping[str, Any], anchors: Sequence[Mapping[str, Any]], rank: Ranker
) -> list[str]:
    reference, subject = pair["reference"], pair["subject"]
    problems = []
    if reference.get("id") != subject.get("id"):
        problems.append("pair_ids_differ")
    elif _position(subject, anchors, rank) > _position(reference, anchors, rank):
        problems.append("priority_lowered")
    if journey_register.human_review_route(subject)["rank_effect"] != "none":
        problems.append("review_route_changes_rank")
    return problems


def evaluate(
    pairs: Sequence[Mapping[str, Any]],
    anchors: Sequence[Mapping[str, Any]],
    seeded_defects: Sequence[str] = (),
    rank: Ranker | None = None,
) -> dict[str, Any]:
    """Check every pair and report counts per dimension; a failing dimension is never averaged."""
    ranker: Ranker = rank or ranking.rank
    dims: dict[str, dict[str, Any]] = {
        d: {"tested": 0, "failed": 0, "failures": []} for d in DIMENSIONS
    }
    blockers: list[str] = []
    failed_ids: set[str] = set()
    for pair in pairs:
        dim = pair.get("dimension")
        pid = str(pair.get("id"))
        if dim not in dims or not (
            isinstance(pair.get("reference"), Mapping) and isinstance(pair.get("subject"), Mapping)
        ):
            blockers.append(f"{pid}:invalid_pair")
            continue
        row = dims[str(dim)]
        row["tested"] += 1
        found = _check_pair(pair, anchors, ranker)
        if found:
            row["failed"] += 1
            row["failures"].append({"pair": pid, "problems": found})
            failed_ids.add(pid)
    for dim, row in dims.items():
        if row["tested"] == 0:
            blockers.append(f"{dim}:no_pairs")
        if row["failed"]:
            blockers.append(f"{dim}:unjustified_deprioritisation")
    blockers += [f"{p}:seeded_defect_undetected" for p in sorted(set(seeded_defects) - failed_ids)]
    record = {
        "version": RECORD_VERSION,
        "synthetic": True,
        "fairness_evidence": False,
        "input_digest": digest({"pairs": list(pairs), "anchors": list(anchors)}),
        "tested": sum(r["tested"] for r in dims.values()),
        "failed": sum(r["failed"] for r in dims.values()),
        "dimensions": dims,
        "seeded_defects": sorted(seeded_defects),
        "detected_defects": sorted(failed_ids),
        "blockers": blockers,
        "status": "pass" if not blockers else "blocked",
        "activation_allowed": False,
        "authority_gap": GAP,
    }
    record["record_hash"] = digest(record)
    return record
