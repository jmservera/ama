"""Retained-reading entry point for the exercise sensor analysis (issue 111).

Reads stored readings and trusted consent through the sensor consumer's read-only methods and
passes them to the pure derivation. It never writes, never creates a task and never ranks. If the
retained store cannot be read, the result is INSUFFICIENT with no priority effect and the manual
review route stays available.
"""

from dataclasses import replace
from datetime import datetime, timedelta

from .sensor_analysis import INSUFFICIENT, AnalysisPolicy, Signal, derive_signal
from .sensor_consumer import ConsumerError, SensorConsumer
from .synthetic.sensor_scenarios import Window

UNAVAILABLE = "RETAINED_READINGS_UNAVAILABLE"


def analyse_retained(
    consumer: SensorConsumer,
    home_id: str,
    window: Window,
    as_of: datetime,
    policy: AnalysisPolicy | None = None,
) -> Signal:
    """Derive the signal for one home from retained readings; fail closed to INSUFFICIENT."""
    last = (window.end - timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    first = window.start.strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        consent = consumer.home_consent(home_id)
        rows = consumer.observed_series([home_id], {home_id: (first, last)})
    except ConsumerError:
        empty = derive_signal(home_id, [], window, as_of, "unknown", policy)
        return replace(
            empty, sufficiency=INSUFFICIENT, outcome=INSUFFICIENT, reasons=(UNAVAILABLE,)
        )
    return derive_signal(home_id, rows, window, as_of, consent, policy)
