"""Resident sensor monitoring consent for the synthetic showcase (issue 2192).

The resident page never writes SQL itself. A consent change goes through the trusted
SensorConsumer seam, which rewrites the home's controls, the index marker and an audit row
together. The notice text is the issue 151 notice; withdrawing never touches repairs, the
tenancy or safety duties.
"""

from collections.abc import Mapping
from typing import Protocol

from zava_forward.core.sensor_consumer import ConsumerError, SensorConsumer
from zava_forward.core.sensor_sql import SensorMssqlConnector
from zava_forward.core.telemetry_consent import NOTICE

ACTOR = "resident-showcase"
LABEL = "Share my home sensor readings with Zava North Homes staff"
STATE_TEXT = {
    "granted": "Staff can see your readings.",
    "declined": "Staff cannot see your readings. New readings are not stored for your home.",
    "unknown": "No choice is recorded yet. Staff cannot see your readings.",
}
ERROR_TEXT = "We could not save your choice. Try again, or ask your housing officer to record it."


class ConsentPort(Protocol):
    def state(self, home_id: str) -> str: ...

    def set(self, home_id: str, granted: bool) -> str: ...


class SensorConsentPort:
    def __init__(self, consumer: SensorConsumer) -> None:
        self.consumer = consumer

    def state(self, home_id: str) -> str:
        return self.consumer.home_consent(home_id)

    def set(self, home_id: str, granted: bool) -> str:
        self.consumer.set_home_consent(home_id, "granted" if granted else "declined", ACTOR)
        return self.consumer.home_consent(home_id)


def port_from_env(env: Mapping[str, str]) -> ConsentPort | None:
    """Opt-in: a dedicated sensor-writing SQL principal, never the read-only showcase one."""
    if env.get("ZF_DEMO_SENSOR_CONSENT") != "1":
        return None
    prefix = "ZF_DEMO_SENSOR_CONSENT_SQL_"
    sql = {"ZF_SQL_" + k[len(prefix) :]: v for k, v in env.items() if k.startswith(prefix)}
    return SensorConsentPort(SensorConsumer(SensorMssqlConnector(sql)))


def card(port: ConsentPort | None, home_id: str | None) -> dict[str, object]:
    """The resident-facing consent card; fails closed to unavailable."""
    base: dict[str, object] = {"notice": dict(NOTICE), "label": LABEL}
    if port is None or not home_id:
        return {**base, "available": False}
    try:
        state = port.state(home_id)
    except (ConsumerError, ValueError):
        return {**base, "available": False}
    return {**base, "available": True, "state": state, "status": STATE_TEXT[state]}
