"""Named anomaly injector (#187): live rows carry no labels; the manifest is evaluator-only."""

import copy
import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

from zava_forward.core.synthetic import sensor_faults

VERSION = "sensor-injector-exercise-v1"
CLASSIFICATION = "SYNTHETIC EXERCISE ONLY; injected patterns are not real home conditions"
SCENARIOS = (
    "damp_mould",
    "underheating",
    "overheating",
    "sensor_fault",
    "post_works_verification",
)
# Keys that would reveal an injection if they reached an operational view.
LEAK_KEYS = frozenset(
    {"injected_fault", "ground_truth", "truth", "injection_id", "injected_scenario", "label"}
)
LIVE_FIELDS = frozenset(sensor_faults.READING_FIELDS)


class GroundTruthLeak(ValueError):
    """Raised when a live row would expose injection metadata."""


@dataclass(frozen=True)
class InjectedEvent:
    injection_id: str
    scenario: str
    sensor_id: str
    home_id: str
    start_observed_at: str
    end_observed_at: str
    row_positions: tuple[int, ...]
    channels: tuple[str, ...]
    expected_outcome: str


@dataclass(frozen=True)
class Injection:
    live_rows: tuple[dict[str, str], ...]
    events: tuple[InjectedEvent, ...]


_OUTCOMES = {
    "damp_mould": "REVIEW_CANDIDATE",
    "underheating": "REVIEW_CANDIDATE",
    "overheating": "REVIEW_CANDIDATE",
    "sensor_fault": "INSUFFICIENT",
    "post_works_verification": "IMPROVEMENT",
}


def _apply(scenario: str, temperature: float, humidity: float) -> tuple[float, float]:
    if scenario == "damp_mould":
        return temperature - 5, min(humidity + 37, 100.0)
    if scenario == "underheating":
        return temperature - 6, humidity + 4
    if scenario == "overheating":
        return temperature + 8, max(humidity - 10, 0.0)
    if scenario == "sensor_fault":
        return 20.0, 55.0
    return temperature + 2, humidity - 10


def inject(
    rows: Sequence[Mapping[str, str]],
    scenario: str,
    *,
    sensor_id: str,
    start_slot: int,
    end_slot: int,
    seed: int,
) -> Injection:
    """Overlay one named pattern on slots [start_slot, end_slot); input rows are not mutated."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario {scenario!r}")
    if not 0 <= start_slot < end_slot <= len(rows):
        raise ValueError("Injection window must lie inside the rows")
    live = [copy.deepcopy(dict(row)) for row in rows]
    for row in live:
        leaked = LEAK_KEYS & set(row)
        if leaked:
            raise GroundTruthLeak(f"Input rows carry injection metadata: {sorted(leaked)}")
    for slot in range(start_slot, end_slot):
        row = live[slot]
        temperature, humidity = _apply(
            scenario, float(row["temperature_c"]), float(row["humidity_pct"])
        )
        row["temperature_c"], row["humidity_pct"] = f"{temperature:.2f}", f"{humidity:.2f}"
    first, last = live[start_slot], live[end_slot - 1]
    event = InjectedEvent(
        injection_id=f"{seed}-{scenario}-{sensor_id}-{start_slot}",
        scenario=scenario,
        sensor_id=sensor_id,
        home_id=first["home_id"],
        start_observed_at=first["observed_at"],
        end_observed_at=last["observed_at"],
        row_positions=tuple(range(start_slot, end_slot)),
        channels=("temperature_c", "humidity_pct"),
        expected_outcome=_OUTCOMES[scenario],
    )
    return Injection(tuple(live), (event,))


def live_view(rows: Sequence[Mapping[str, object]]) -> tuple[dict[str, object], ...]:
    """Operational projection: reject label keys and drop every undeclared field."""
    view = []
    for row in rows:
        leaked = LEAK_KEYS & set(row)
        if leaked:
            raise GroundTruthLeak(f"Live row exposes ground truth: {sorted(leaked)}")
        view.append({key: value for key, value in row.items() if key in LIVE_FIELDS})
    return tuple(view)


def manifest(events: Sequence[InjectedEvent], seed: int) -> dict[str, object]:
    return {
        "version": VERSION,
        "classification": CLASSIFICATION,
        "seed": seed,
        "audience": "evaluator-only; never join into live operational views",
        "events": [asdict(event) for event in events],
    }


def write_manifest(path: Path, events: Sequence[InjectedEvent], seed: int) -> None:
    """Write the manifest only to a path that is not part of a live data directory."""
    if path.exists():
        raise FileExistsError("Refusing to overwrite an existing manifest")
    payload = json.dumps(manifest(events, seed), indent=2, sort_keys=True, allow_nan=False)
    path.write_text(payload + "\n", encoding="utf-8")
