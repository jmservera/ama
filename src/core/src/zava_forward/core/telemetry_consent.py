"""Issue 151: resident telemetry notice and withdrawal that never touches repairs or safety duties.

Withdrawal declines monitoring consent for every sensor control of one home through the trusted
consumer seam. New readings are then rejected as CONSENT, and the employee sensor view withholds
values for the home. Nothing here reads or writes cases, repairs, hazards or statutory duties.
"""

from collections.abc import Sequence
from dataclasses import dataclass, replace

from zava_forward.core.sensor_consumer import ExercisePolicy, SensorConsumer, SensorControl

NOTICE = {
    "collected": (
        "Your home sensor measures temperature and humidity and sends the readings to "
        "Zava North Homes."
    ),
    "why": "We use the readings to spot damp and cold early and to plan repairs.",
    "who_sees": (
        "Housing and repairs staff with a work reason see the readings. They are not shared "
        "outside Zava North Homes by this service."
    ),
    "how_to_stop": (
        "Tell us at any time and we will stop collecting readings. Contact your housing officer "
        "or use the withdrawal option in your account."
    ),
    "not_affected": (
        "Saying no, or stopping later, does not change your repairs, your tenancy or our safety "
        "duties. We will still repair your home and meet our legal safety checks."
    ),
}

PRESERVED_DUTIES = ("core-housing-repairs", "statutory-safety-duties")


@dataclass(frozen=True)
class WithdrawalOutcome:
    home_id: str
    collection: str
    downstream_views: str
    preserved_duties: tuple[str, ...]
    blocks_repairs_or_safety: bool
    sensors_declined: int


def withdraw(
    consumer: SensorConsumer,
    policy: ExercisePolicy,
    controls: Sequence[SensorControl],
    home_id: str,
) -> WithdrawalOutcome:
    """Decline consent for one home's controls; other homes keep their current consent."""
    owned = [c for c in controls if c.home_id == home_id]
    if not owned:
        raise ValueError("UNKNOWN_HOME")
    consumer.configure(
        policy, [replace(c, consent="declined") if c.home_id == home_id else c for c in controls]
    )
    return WithdrawalOutcome(
        home_id=home_id,
        collection="stopped",
        downstream_views="consent-withheld",
        preserved_duties=PRESERVED_DUTIES,
        blocks_repairs_or_safety=False,
        sensors_declined=len(owned),
    )
