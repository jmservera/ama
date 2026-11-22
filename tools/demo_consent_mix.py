"""Plan and apply the synthetic consent mix for the live IoT demo (issue 184).

The mix is applied only through the repository's SensorConsumer.configure, which rewrites the
policy, every control, the per-home index and the index marker together. Synthetic fixtures only:
no resident consent is claimed. A pure planner is kept separate from the SQL apply step so it can
be tested without a database; `apply` needs ZF_SQL_* settings and the sensor ddl rights.

Usage (from an environment with the src projects installed):
    python tools/demo_consent_mix.py select HOME_ID...      # at least half of all homes, one per line
    python tools/demo_consent_mix.py select-readings HOME_ID...  # cohort whose granted homes alone
                                                            # cover half of all homes (issue 2191);
                                                            # the granted count goes to stderr
    python tools/demo_consent_mix.py plan [--granted N] HOME_ID...   # print the plan, no writes
    python tools/demo_consent_mix.py apply [--granted N] HOME_ID...  # SensorConsumer.configure
    python tools/demo_consent_mix.py control OWNER REF HOME_ID...   # control.json to stdout
"""

from __future__ import annotations

import json
import math
import os
import sys
from datetime import UTC, datetime, timedelta

from zava_forward.core.sensor_consumer import ExercisePolicy, SensorControl
from zava_forward.core.synthetic.sensor_identity import sensor_key

WINDOW_DAYS = 13
GRANTED_SHARE = 0.5
MAX_COHORT = 500
COVERAGE = 0.5
READING_SHARE = 0.5
HEADROOM = 0.15  # stale share: skipped runs plus the gap before the next run is ingested
DECLINED_SHARE = 0.1


def select_cohort(all_homes: list[str], coverage: float = COVERAGE) -> list[str]:
    """Pick at least `coverage` of ALL demo homes, evenly spread and repeatable.

    The result is capped by the control limit; a fleet too large for that refuses rather than
    silently covering less than the share asked for.
    """
    homes = sorted(set(all_homes))
    if not homes or not 0 < coverage <= 1:
        raise ValueError("COHORT_INVALID")
    wanted = math.ceil(len(homes) * coverage)
    if wanted > MAX_COHORT:
        raise ValueError("COHORT_TOO_LARGE")
    return [homes[i * len(homes) // wanted] for i in range(wanted)]


def select_reading_cohort(
    all_homes: list[str],
    reading_share: float = READING_SHARE,
    headroom: float = HEADROOM,
    declined_share: float = DECLINED_SHARE,
) -> tuple[list[str], int]:
    """Pick a cohort whose granted homes alone store readings for `reading_share` of ALL homes.

    Only granted homes are stored; declined homes are rejected at the receiver. `headroom` is the
    share of granted homes allowed to be stale at any instant (skipped slots, ingestion lag), and
    `declined_share` keeps a visible declined minority so the consent mix stays demonstrable.
    Returns the cohort and the number of granted homes in it.
    """
    homes = sorted(set(all_homes))
    if not homes or not 0 < reading_share <= 1 or not 0 <= headroom < 1:
        raise ValueError("COHORT_INVALID")
    if not 0 <= declined_share < 1:
        raise ValueError("COHORT_INVALID")
    granted = math.ceil(len(homes) * reading_share / (1 - headroom))
    declined = math.ceil(granted * declined_share) or 1
    size = granted + declined
    if size > len(homes):
        raise ValueError("COHORT_INVALID")
    if size > MAX_COHORT:
        raise ValueError("COHORT_TOO_LARGE")
    return [homes[i * len(homes) // size] for i in range(size)], granted


def plan(
    home_ids: list[str], now: datetime, granted: int | None = None
) -> tuple[ExercisePolicy, list[SensorControl], list[str]]:
    """Split the cohort between granted and declined, spread so any slice keeps the mix.

    `granted` defaults to half the cohort; an explicit count keeps at least one declined home.

    Homes outside the cohort get no control, so the Home sensors page shows Readings withheld
    for them. Returns the policy, the controls and the cohort homes that carry a device.
    """
    if not 1 <= len(home_ids) <= MAX_COHORT or len(set(home_ids)) != len(home_ids):
        raise ValueError("COHORT_INVALID")
    slot = now.replace(minute=now.minute - now.minute % 5, second=0, microsecond=0)
    start = (slot - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = (slot + timedelta(days=WINDOW_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    policy = ExercisePolicy(
        window_start=start,
        window_end=end,
        max_past_seconds=7200,
        max_future_seconds=600,
        temperature_min=-10,
        temperature_max=45,
        humidity_min=0,
        humidity_max=100,
        accountable_role="exercise-data-quality-review",
        manual_route="manual-sensor-review",
        reviewer="Demo walkthrough owner",
    )
    if granted is None:
        granted = round(len(home_ids) * GRANTED_SHARE)
    if not 1 <= granted < len(home_ids):
        raise ValueError("COHORT_INVALID")
    flags = [
        (i * granted) // len(home_ids) != ((i + 1) * granted) // len(home_ids)
        for i in range(len(home_ids))
    ]
    controls = [
        SensorControl(
            sensor_id=sensor_key(home),
            home_id=home,
            mapping_start=start,
            mapping_end=end,
            consent="granted" if flags[i] else "declined",
            calibration_start=start,
            calibration_end=end,
            calibration_confirmed=True,
            temperature_unit="degC",
            humidity_unit="percent",
        )
        for i, home in enumerate(home_ids)
    ]
    return policy, controls, list(home_ids)


def control_document(
    owner: str, reference: str, homes: list[str], now: datetime
) -> dict[str, object]:
    return {
        "version": "live-sim-control-v1",
        "enabled": True,
        "expires_at": (now + timedelta(days=WINDOW_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "approval_reference": reference,
        "owner": owner,
        "homes": homes,
    }


def apply(home_ids: list[str], granted: int | None = None) -> None:
    from zava_forward.core.sensor_consumer import SensorConsumer
    from zava_forward.core.sensor_sql import SensorMssqlConnector

    policy, controls, _ = plan(home_ids, datetime.now(UTC), granted)
    SensorConsumer(SensorMssqlConnector(os.environ)).configure(policy, controls)


def main(argv: list[str]) -> int:
    mode, rest = (argv[0], argv[1:]) if argv else ("", [])
    now = datetime.now(UTC)
    if mode == "select" and rest:
        try:
            print("\n".join(select_cohort(rest)))
        except ValueError as error:
            print(error, file=sys.stderr)
            return 2
        return 0
    if mode == "select-readings" and rest:
        try:
            cohort, granted = select_reading_cohort(rest)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 2
        print("\n".join(cohort))
        print(f"granted {granted} of {len(cohort)}", file=sys.stderr)
        return 0
    if mode == "control" and len(rest) >= 3:
        print(json.dumps(control_document(rest[0], rest[1], rest[2:], now)))
        return 0
    if mode in ("plan", "apply") and rest:
        granted = None
        if rest[0] == "--granted" and len(rest) > 2 and rest[1].isdigit():
            granted, rest = int(rest[1]), rest[2:]
        try:
            _, controls, _ = plan(rest, now, granted)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 2
        for c in controls:
            print(c.home_id, c.sensor_id, c.consent)
        if mode == "apply":
            apply(rest, granted)
            print("configured", len(controls))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
