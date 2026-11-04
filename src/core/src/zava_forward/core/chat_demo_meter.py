"""Demo-only financial meter records for the employee assistant (#891).

The meter admits a model call only when the ledger holds an authority and a
price for the exact chat configuration. Under the owner-approved demo switch
(ZF_CHAT_DEMO_ACTIVATION with ZF_DEPLOYMENT_PROFILE=demo) this module records
a synthetic, low-cap, one-day authority and price so the demonstration can make
one call per question. Nothing is recorded without the switch, and the records
are labelled synthetic: they are not a finance approval, a real price or a
budget decision.
"""

import logging
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any

from . import ai_registry
from .ai_consumption import reference

TASK = ai_registry.CHAT_TASK
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
    """Idempotently seed today's synthetic authority; a no-op without the demo switch."""
    ai = store.ai
    honoured = ai_registry.demo_activation_honoured(TASK, env)  # type: ignore[no-untyped-call]
    ai.synthetic_price_capabilities = frozenset({TASK}) if honoured else frozenset()
    ledger = getattr(ai, "consumption", None)
    if not honoured or ledger is None:
        return False
    day = (now or datetime.now(UTC)).replace(hour=0, minute=0, second=0, microsecond=0)
    start, end = day.isoformat(), (day + timedelta(days=1)).isoformat()
    label = f"synthetic-demo-chat-{day.date().isoformat()}"
    configuration = ai.configuration(ai.fast, TEMPERATURE, max_tokens)
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
            capability=TASK,
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
        logging.getLogger(__name__).warning("Demo chat meter not seeded (%s)", type(error).__name__)
        return False
    return True
