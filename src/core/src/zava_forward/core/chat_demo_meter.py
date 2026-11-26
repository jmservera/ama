"""Demo-only financial meter records for the employee assistant (#891).

The meter admits a model call only when the ledger holds an authority and a
price for the exact chat configuration. Under the owner-approved demo switch
(ZF_CHAT_DEMO_ACTIVATION with ZF_DEPLOYMENT_PROFILE=demo) this module records
a synthetic, low-cap authority for each UTC hour and price so the demonstration can make
one call per question. Nothing is recorded without the switch, and the records
are labelled synthetic: they are not a finance approval, a real price or a
budget decision.
"""

import logging
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any

from . import ai_registry, continuity
from .ai_consumption import reference

TASK = ai_registry.CHAT_TASK
QUALITY_TASK = "quality-evidence"
OWNER = "synthetic-demo-owner-" + ai_registry.DEMO_ACTIVATION["accountable_owner"]
PRICE_SOURCE = "https://azure.microsoft.com/pricing/details/azure-openai/"
CALLS, TOKENS, AMOUNT = 20, 100000, "1"
TEMPERATURE = 0  # the evidence call the employee assistant uses


def ensure(
    store: Any,
    max_tokens: int,
    env: Mapping[str, str] | None = None,
    now: datetime | None = None,
) -> bool:
    """Idempotently seed this hour's synthetic authority; a no-op without the demo switch."""
    honoured = ai_registry.demo_activation_honoured(TASK, env)  # type: ignore[no-untyped-call]
    return _seed(store, TASK, honoured, max_tokens, now, "chat", "demo_chat_seeded")


def ensure_quality(
    store: Any,
    max_tokens: int,
    env: Mapping[str, str] | None = None,
    now: datetime | None = None,
) -> bool:
    """The same synthetic hourly meter for Quality, under the owner demo override only."""
    return _seed(
        store,
        QUALITY_TASK,
        continuity.demo_owner_override(env),
        max_tokens,
        now,
        "quality",
        "demo_quality_seeded",
    )


def _seed(
    store: Any,
    task: str,
    honoured: bool,
    max_tokens: int,
    now: datetime | None,
    kind: str,
    flag: str,
) -> bool:
    ai = store.ai
    ai.synthetic_price_capabilities = (
        frozenset(getattr(ai, "synthetic_price_capabilities", ())) - {task}
    ) | ({task} if honoured else frozenset())
    ledger = getattr(ai, "consumption", None)
    if not honoured or ledger is None:
        return False
    moment = (now or datetime.now(UTC)).replace(minute=0, second=0, microsecond=0)
    # One budget per hour: a settlement the ledger holds as liability-unknown stops the model for
    # the rest of that hour only. Authority windows may not overlap, so each slot abuts the next.
    start, end = moment.isoformat(), (moment + timedelta(hours=1)).isoformat()
    label = f"synthetic-demo-{kind}-{moment.strftime('%Y-%m-%dT%H')}"
    configuration = ai.configuration(ai.fast, TEMPERATURE, max_tokens)
    # Each ledger write opens a new SQL connection, takes the exclusive write lock and rereads it.
    seeded = (label, configuration, CALLS, TOKENS, AMOUNT)
    if getattr(ledger, flag, None) == seeded:
        return True
    try:
        price = ledger.price(
            source=PRICE_SOURCE,
            source_hash=reference(label + "-price"),
            retrieved=start,
            version=label,
            model=ai.model_version,
            currency="USD",
            start=start,
            end=end,
            input_rate="1",
            output_rate="2",
            cached_rate="0.5",
            synthetic=True,
        )
        ledger.authorize(
            authority=f"{label}-{configuration[:12]}",
            owner=OWNER,
            evidence=label + "-evidence",
            price=price,
            capability=task,
            configuration=configuration,
            start=start,
            end=end,
            budgets=[
                dict(id=reference(label + "-budget"), calls=CALLS, tokens=TOKENS, amount=AMOUNT)
            ],
            max_calls=1,
            max_depth=1,
        )
    except Exception as error:
        # Ledger refusals are fixed text without case data, so the cause can be logged.
        logging.getLogger(__name__).warning(
            "Demo chat meter not seeded (%s: %s)", type(error).__name__, error
        )
        return False
    setattr(ledger, flag, seeded)
    return True
