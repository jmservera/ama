"""Net-effort comparison for the five journey learning-test bundles (#129, NFR-009).

Deterministic and pure: it sums recorded effort minutes per arm, reports the median and range,
applies each bundle's stop rule to its "target zero" counts and labels saved minutes as capacity.
It runs no experiment, uses no AI and holds no representative data; inputs are constructed cases.

Command: ``python -m zava_forward.core.learning_test_bundles < input.json`` reads one bounded
``learning-bundle-constructed-input-v1`` JSON object from standard input, scores it with
``run_report`` and prints ``render_report`` plus constructed/unverified qualifications. It stores
nothing and reads no file, dataset or network; any refusal exits 1 with no report.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import dataclass
from typing import Any

COMPONENTS = (
    "preparation",
    "checking",
    "correction",
    "coordination",
    "resident_effort",
    "support_cost",
)
ARMS = ("comparator", "workflow")
OUT_OF_SCOPE = frozenset({"O10", "O18", "O19", "O20"})
EVIDENCE_LABEL = "constructed-case evidence"
CAPACITY_NOTE = "Saved minutes are capacity until Finance validates them; not cash or benefit."


@dataclass(frozen=True)
class Bundle:
    key: str
    atlas_ids: tuple[str, ...]
    comparator: str
    zero_measures: tuple[str, ...]


BUNDLES: dict[str, Bundle] = {
    b.key: b
    for b in (
        Bundle(
            "story-once",
            ("O01", "O02", "O03", "O15"),
            "Manual re-asking and chase log",
            ("authority_or_consent_breaches", "promises_without_owner"),
        ),
        Bundle(
            "pre-visit-pack",
            ("O06", "O08", "O09"),
            "Current visit preparation",
            ("offers_misread_as_commitments",),
        ),
        Bundle(
            "change-impact",
            ("O07", "O16"),
            "Manual dependency check",
            ("approvals_wrongly_carried_over",),
        ),
        Bundle(
            "handover-aftercare",
            ("O13", "O14"),
            "Paper handover",
            ("open_remedies_hidden",),
        ),
        Bundle(
            "funding-evidence",
            ("O16", "O17"),
            "Manual evidence pack",
            ("inferred_submissions",),
        ),
    )
}


def case_net_effort(efforts: dict[str, float]) -> float:
    """Sum all six components; a missing or negative component is rejected, not defaulted."""
    unknown = set(efforts) - set(COMPONENTS)
    missing = [c for c in COMPONENTS if c not in efforts]
    if unknown or missing:
        raise ValueError(f"Effort needs exactly {', '.join(COMPONENTS)}.")
    if any(v < 0 for v in efforts.values()):
        raise ValueError("Effort minutes cannot be negative.")
    return float(sum(efforts.values()))


def _summary(totals: list[float]) -> dict[str, Any]:
    return {
        "cases": len(totals),
        "median_minutes": statistics.median(totals),
        "min_minutes": min(totals),
        "max_minutes": max(totals),
    }


def compare_bundle(bundle_key: str, cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare the arms of one bundle over the same constructed cases.

    Each case is ``{"case": id, "arms": {arm: {"effort": {...}, "counts": {...}}}}``.
    """
    bundle = BUNDLES.get(bundle_key)
    if bundle is None:
        raise ValueError(f"Unknown bundle {bundle_key!r}.")
    if OUT_OF_SCOPE & set(bundle.atlas_ids):
        raise ValueError("Out-of-scope opportunities cannot be tested.")
    if not cases:
        raise ValueError("At least one constructed case is required.")
    totals: dict[str, list[float]] = {arm: [] for arm in ARMS}
    breaches: list[str] = []
    for case in cases:
        arms = case.get("arms", {})
        if set(arms) != set(ARMS):
            raise ValueError("Every case needs both arms on the same case.")
        for arm in ARMS:
            data = arms[arm]
            totals[arm].append(case_net_effort(data["effort"]))
            counts = data.get("counts", {})
            for measure in bundle.zero_measures:
                if counts.get(measure) is None:
                    raise ValueError(f"Missing count {measure} for {arm}.")
                if counts[measure] != 0:
                    breaches.append(f"{case.get('case')}/{arm}/{measure}")
    comp, flow = _summary(totals["comparator"]), _summary(totals["workflow"])
    delta = flow["median_minutes"] - comp["median_minutes"]
    return {
        "bundle": bundle_key,
        "comparator_description": bundle.comparator,
        "evidence_label": EVIDENCE_LABEL,
        "comparator": comp,
        "workflow": flow,
        "median_difference_minutes": delta,
        "direction": "workflow lower" if delta < 0 else "comparator lower or equal",
        "stop": bool(breaches),
        "breaches": breaches,
        "capacity_note": CAPACITY_NOTE,
        "assistance_note": "Assistance not available is a valid arm; manual path stays complete.",
    }


O16_BUNDLES = tuple(b.key for b in BUNDLES.values() if "O16" in b.atlas_ids)


def run_report(run: dict[str, Any]) -> dict[str, Any]:
    """Validate a recorded run's metadata, then compare its arms.

    A run is ``{"bundle", "o16_counted_under", "representative_data_retained", "cases"}``.
    ``o16_counted_under`` is required for bundles that share O16 so effort is counted once.
    """
    bundle = BUNDLES.get(str(run.get("bundle")))
    if bundle is None:
        raise ValueError(f"Unknown bundle {run.get('bundle')!r}.")
    if run.get("representative_data_retained") is not False:
        raise ValueError("State representative_data_retained as false; retention awaits the DPO.")
    owner = run.get("o16_counted_under")
    if "O16" in bundle.atlas_ids and owner not in O16_BUNDLES:
        raise ValueError(f"State which bundle counts O16: {', '.join(O16_BUNDLES)}.")
    if "O16" not in bundle.atlas_ids and owner is not None:
        raise ValueError("o16_counted_under applies only to bundles that include O16.")
    report = compare_bundle(bundle.key, run.get("cases", []))
    report["o16_counted_under"] = owner
    return report


def reconcile_o16(runs: list[dict[str, Any]]) -> str | None:
    """Return the single bundle that counts O16 across runs; reject conflicting claims."""
    owners: set[str] = set()
    for r in runs:
        bundle = BUNDLES.get(str(r.get("bundle")))
        if bundle is None:
            raise ValueError(f"Unknown bundle {r.get('bundle')!r}.")
        owner = r.get("o16_counted_under")
        if "O16" in bundle.atlas_ids:
            if owner not in O16_BUNDLES:
                raise ValueError(f"State which bundle counts O16: {', '.join(O16_BUNDLES)}.")
            owners.add(owner)
        elif owner is not None:
            raise ValueError("o16_counted_under applies only to bundles that include O16.")
    if len(owners) > 1:
        raise ValueError(
            "Runs disagree on which bundle counts O16; effort would be double counted."
        )
    return next(iter(owners), None)


def render_report(report: dict[str, Any]) -> str:
    """Plain-language text for a facilitator; a stop is stated before any effort figure."""
    lines = [f"Bundle: {report['bundle']} (comparator: {report['comparator_description']})"]
    if report["stop"]:
        lines.append("STOP: " + ", ".join(report["breaches"]) + " (target zero).")
    else:
        lines.append("Stop rule: no breach recorded.")
    for arm in ARMS:
        s = report[arm]
        lines.append(
            f"{arm}: {s['cases']} cases, median {s['median_minutes']:g} min, "
            f"range {s['min_minutes']:g} to {s['max_minutes']:g} min"
        )
    lines += [
        "Median difference (workflow minus comparator): "
        f"{report['median_difference_minutes']:g} min ({report['direction']}).",
        f"Evidence: {report['evidence_label']}.",
        report["capacity_note"],
        report["assistance_note"],
    ]
    if report.get("o16_counted_under"):
        lines.append(f"O16 counted under: {report['o16_counted_under']}.")
    return "\n".join(lines)


SCHEMA_VERSION = "learning-bundle-constructed-input-v1"
MAX_INPUT_BYTES = 65536
MAX_CASES = 50
MAX_ID = 1_000_000
MAX_MINUTES = 100_000
MAX_COUNT = 1_000_000
_REQUIRED = ("schema_version", "run", "bundle", "cases")
_ALLOWED = frozenset((*_REQUIRED, "representative_data_retained", "o16_counted_under"))
QUALIFICATIONS = (
    "Constructed input declared by the caller: not verified synthetic provenance, "
    "not a real experiment and not measured user benefit.",
    "Atlas owner bundle-to-opportunity mapping is unconfirmed.",
    "Representative-data retention decision is unsatisfied; none is retained here.",
    "Nothing is stored: no run record, file or database is written.",
)
O16_QUALIFICATION = (
    "O16 counted-under is the caller's constructed accounting choice, "
    "not owner mapping ratification."
)


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"Duplicate key {key[:40]!r}.")
        out[key] = value
    return out


def _reject_constant(name: str) -> Any:
    raise ValueError("Non-finite numbers are not accepted.")


def _exact(value: Any, keys: tuple[str, ...], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(f"{label} needs exactly: {', '.join(keys)}.")
    return value


def _identifier(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_ID:
        raise ValueError(f"{label} must be an integer from 1 to {MAX_ID}.")
    return value


def _validate_input(raw: Any) -> dict[str, Any]:
    """Check the closed numeric envelope; bundle, retention and O16 rules stay in run_report."""
    if not isinstance(raw, dict):
        raise ValueError("Input must be one JSON object.")
    if set(raw) - _ALLOWED:
        raise ValueError("Unknown input key.")
    missing = [key for key in _REQUIRED if key not in raw]
    if missing:
        raise ValueError(f"Input needs {', '.join(missing)}.")
    if raw["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}.")
    _identifier(raw["run"], "run")
    bundle = BUNDLES.get(raw["bundle"]) if isinstance(raw["bundle"], str) else None
    if bundle is None:
        raise ValueError(f"Unknown bundle {raw['bundle']!r}.")
    cases = raw["cases"]
    if not isinstance(cases, list) or not 1 <= len(cases) <= MAX_CASES:
        raise ValueError(f"cases must hold 1 to {MAX_CASES} constructed cases.")
    seen: set[int] = set()
    for item in cases:
        item = _exact(item, ("case", "arms"), "Each case")
        if _identifier(item["case"], "case") in seen:
            raise ValueError("Case numbers must be unique.")
        seen.add(item["case"])
        arms = _exact(item["arms"], ARMS, "arms")
        for arm in ARMS:
            data = _exact(arms[arm], ("effort", "counts"), f"{arm} arm")
            effort = _exact(data["effort"], COMPONENTS, f"{arm} effort")
            for name, minutes in effort.items():
                if (
                    isinstance(minutes, bool)
                    or not isinstance(minutes, int | float)
                    or not 0 <= minutes <= MAX_MINUTES
                ):
                    raise ValueError(f"{name} must be a number from 0 to {MAX_MINUTES} minutes.")
            counts = _exact(data["counts"], bundle.zero_measures, f"{arm} counts")
            for name, count in counts.items():
                if (
                    isinstance(count, bool)
                    or not isinstance(count, int)
                    or not 0 <= count <= MAX_COUNT
                ):
                    raise ValueError(f"{name} must be an integer from 0 to {MAX_COUNT}.")
    return {
        key: raw[key]
        for key in ("bundle", "representative_data_retained", "o16_counted_under", "cases")
        if key in raw
    }


def main(argv: list[str] | None = None) -> int:
    """Read one constructed envelope from stdin and print the existing report; store nothing."""
    parser = argparse.ArgumentParser(
        prog="python -m zava_forward.core.learning_test_bundles", description=__doc__
    )
    parser.parse_args(argv)
    try:
        if sys.stdin.isatty():
            raise ValueError("pipe one constructed JSON object on standard input.")
        data = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(data) > MAX_INPUT_BYTES:
            raise ValueError(f"Input is larger than {MAX_INPUT_BYTES} bytes.")
        raw = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_unique_pairs,
            parse_constant=_reject_constant,
        )
        number = raw.get("run") if isinstance(raw, dict) else None
        report = run_report(_validate_input(raw))
    except (ValueError, RecursionError) as error:
        sys.stderr.write(f"Learning report refused: {str(error)[:200]}\n")
        return 1
    qualifications = list(QUALIFICATIONS)
    if report.get("o16_counted_under"):
        qualifications.append(O16_QUALIFICATION)
    print("\n".join([f"CONSTRUCTED, UNVERIFIED INPUT (run {number}).", render_report(report)]))
    print("\n".join(qualifications))
    return 0


if __name__ == "__main__":
    sys.exit(main())
