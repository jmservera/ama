# Changes: issue 163 provider position and DPO decision pack, 2026-11-01

Plan: ../../plans/2026-11-01/issue-163-chat-privacy-provider-position-plan.md

* src/core `chat_privacy.py`: `MODEL_PROVIDER_POSITION["documented_terms"]` (vendor documentation, not DPO-accepted) and revised open items.
* src/core `tests/test_chat_privacy.py`: test that the position is documented but not accepted.
* `docs/reference/research/chat-memory-dpia.md`: sourced provider table, blank decision pack D1 to D8, refreshed open items, ms.date.
* `docs/reference/README.md` index row and `docs/reference/log.md` entry.
* Validation (src/core, venv, pip): 101 chat tests OK; ruff check, ruff format --check and mypy clean. No heavy gate; CI is the evidence.
* Divergence: none.

## Follow-up 2026-11-01 (review round)

* Summary string now keeps the "without permission" qualification and "train or improve"; DPIA D2 asks for a resident Article 6 basis plus Article 9 only for special-category data; the abuse-monitoring row is a verification instruction; the audit-trail test asserts the exact source URL and an ISO retrieved date.
* The earlier "No heavy gate; CI is the evidence" line is superseded: the complete local gate (`tools/rpi-checks.py --all`) is required before publication. Result recorded below.
* Gate result: `tools/rpi-checks.py --all` ran to the Docker/infra groups against a reviewed base, but `origin/main` advanced during the roughly 40 minute run and the gate refused to continue ("Reviewed base differs from current origin/main"). No passing exact-head receipt exists. Publication blocker: re-run the gate on the final head once main is stable; hosted CI is not a substitute and is not claimed as one.

## Follow-up 2026-11-01 (second review round)

* Added the missing blank line between test methods in `src/core/tests/test_chat_privacy.py`. The "recorded below" thread was already addressed by the gate result above. Pending hosted checks were still running at this time; none had failed.
