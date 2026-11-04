"""Comparison record for the discovery assistant against non-agent methods (issue 125).

Pure and deterministic: no store, network, model or clock access. It holds the discovery brief's ten
evaluation measures and three comparators (manual analysis, conventional business intelligence,
deterministic workflow reporting) plus the assistant. Humans supply a pointer to the observed result
for each measure and method; nothing is scored or inferred here, and the report never says the
assistant is better or approved. A measure is comparable only when every method has a usable
pointer. The accountable discovery owner and the benefits and evaluation owner judge the results.
"""

import hashlib
import json
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any

EVALUATION_VERSION = "discovery-assistant-evaluation-v1"

MEASURES: tuple[tuple[str, str], ...] = (
    ("population-coverage", "Includes incomplete, paused, excluded and reopened cases"),
    ("identifier-reconciliation", "Property and building records unmatched or disputed"),
    ("event-accuracy", "Source owners confirm the mapped state and timestamp"),
    ("calculation-repeatability", "Same approved dataset gives the same durations and counts"),
    ("attribution-quality", "Owners confirm, reject or dispute a proposed cause"),
    ("traceability", "Every finding traces to source events and calculation rules"),
    ("review-effort", "Analyst and domain-owner time after correction and assurance"),
    ("decision-usefulness", "Analysis changes a process, capacity, contract or capital decision"),
    ("error-severity", "Omission or wrong attribution could conceal safety or resident risk"),
    ("whole-life-value", "Benefit exceeds integration, review, assurance, support and exit cost"),
)
MEASURE_KEYS = tuple(key for key, _ in MEASURES)
METHODS: tuple[str, ...] = (
    "assistant",
    "manual-analysis",
    "conventional-bi",
    "deterministic-workflow-reporting",
)
COMPARATORS = tuple(m for m in METHODS if m != "assistant")

_REFERENCE = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._:/#-]{2,119}\Z")
_PLACEHOLDERS = frozenset({"tbc", "tbd", "todo", "n/a", "none", "pending", "unknown"})
MANUAL_PATH = (
    "Manual analysis, conventional reporting and export remain available; "
    "nothing here needs a model."
)


@dataclass(frozen=True)
class MeasureResult:
    """A human-supplied pointer to an observed result for one measure and one method."""

    measure: str
    method: str
    result_reference: str
    recorded_by_role: str


@dataclass(frozen=True)
class ComparisonReport:
    evaluation_version: str
    comparable: tuple[str, ...]
    incomplete: dict[str, tuple[str, ...]]
    invalid: tuple[str, ...]
    criterion_met: bool = False
    assistant_preferred: bool = False
    approved_solution: bool = False
    manual_path: str = MANUAL_PATH
    next_step: str = ""
    notes: tuple[str, ...] = field(default_factory=tuple)


def _valid(value: object) -> bool:
    return (
        isinstance(value, str)
        and _REFERENCE.fullmatch(value) is not None
        and value.strip().lower() not in _PLACEHOLDERS
    )


def compare_methods(results: Iterable[MeasureResult]) -> ComparisonReport:
    """List measures with result pointers for every method; never ranks or approves.

    `criterion_met` stays False: whether the comparison satisfies the acceptance criterion is a
    human judgement of the pointed-to results, not something this code can decide.
    """
    seen: dict[tuple[str, str], MeasureResult] = {}
    invalid: list[str] = []
    for r in results:
        if r.measure not in MEASURE_KEYS or r.method not in METHODS:
            invalid.append(f"unknown:{str(r.measure)[:40]}/{str(r.method)[:40]}")
        elif (r.measure, r.method) in seen:
            invalid.append(f"duplicate:{r.measure}/{r.method}")
        elif not (_valid(r.result_reference) and _valid(r.recorded_by_role)):
            invalid.append(f"unusable-evidence:{r.measure}/{r.method}")
        else:
            seen[(r.measure, r.method)] = r
    comparable: list[str] = []
    incomplete: dict[str, tuple[str, ...]] = {}
    for key in MEASURE_KEYS:
        missing = tuple(m for m in METHODS if (key, m) not in seen)
        if missing:
            incomplete[key] = missing
        else:
            comparable.append(key)
    done = not incomplete and not invalid
    return ComparisonReport(
        evaluation_version=EVALUATION_VERSION,
        comparable=tuple(comparable),
        incomplete=incomplete,
        invalid=tuple(invalid),
        next_step=(
            "Evaluation owner reviews the pointed-to results and records a human conclusion."
            if done
            else "Record results for every method on each incomplete measure."
        ),
        notes=("Result pointers are supplied by humans and not verified by this code.",),
    )


@dataclass(frozen=True)
class RepeatabilityResult:
    runs: int
    identical: bool
    digests: tuple[str, ...]


def _digest(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check_repeatability(
    calculation: Callable[[Any], Any], dataset: Any, runs: int = 3
) -> RepeatabilityResult:
    """Run a deterministic calculation repeatedly on one dataset and compare output digests."""
    if runs < 2:
        raise ValueError("runs must be at least 2")
    digests = tuple(_digest(calculation(dataset)) for _ in range(runs))
    return RepeatabilityResult(runs, len(set(digests)) == 1, digests)
