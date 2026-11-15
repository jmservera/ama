# Brief: 435 batch C1 call-site inventory (2058)

Cycle 1 of 5 CI fix for PR #1559. Hosted `src-api` failed `test_every_provider_call_site_is_classified`: `agents/src/zava_forward/agents/heldout_aoai.py` is a provider call site missing from `INVENTORY` in `src/api/tests/test_ai_call_site_inventory.py`. Classify it accurately, validate with focused-tier pip-only checks, commit locally with `Refs #435` and `Refs #432`; do not push or edit GitHub.
