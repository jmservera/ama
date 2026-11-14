<!-- markdownlint-disable-file -->
# Changes: Issue #104 controlled-record non-mutation proof

* Plan: [104-controlled-nomutate-0230-plan.md](../../plans/2026-11-14/104-controlled-nomutate-0230-plan.md)

## Added

* `src/api/tests/test_ai_controlled_record_non_mutation.py`: nine tests, auto-discovered by `unittest discover -s tests`.
  * Chat: six adversarial prompts (approve or unblock a hold, rank, consent, sign-off, funding) over three roles and two reply modes (hostile, supported); non-existent approve, execute and rank routes refused; a role without chat access changes nothing.
  * Assistants: all five invoke, claim, dispatch, complete, verify, accept, edit-accept, reject; reject without verification; malformed output; proactive scan; unauthorised invocation.
  * Positive control: a human hazard referral, receipt and resident decision do change the snapshot.
  * Snapshot: raw SQL case rows, procurement meta, recommendations, staff, hazard, decision, sign-off, finance, grant and funding extracts, ranking map and ranking archive file digests. The hazard hold stays `Active`; audit growth is limited to `chat.*` actions.

## Not changed

* No production code, `src/api/pyproject.toml` (PR #1604) or `docs/reference/log.md`.

## Divergences and findings

* Issue text names `/api/cases/{id}/chat`; no such route exists. Chat is `/api/chat/threads/*` and `/api/chat/unstored-ask`. The module asserts the former path is refused.
* The test fixture logs "Rule evaluation unavailable" (no law store loaded) during human seeding. This is expected noise and does not affect the assertions.
* Not covered: MSSQL dialect, browser surfaces, live provider calls, other controlled domains not seeded (procurement orders, stock holds beyond the snapshot of `meta.procurement`).

## Validation (focused tier, local only)

* `ruff check` and `ruff format --check`: pass.
* `python3 -m unittest tests.test_ai_controlled_record_non_mutation -v`: 9 tests, OK. Discovery via `unittest discover -s tests` also runs it.
* Not run: full local gate, hosted CI, independent exact-head review, owner sign-off. No criterion is ticked by this change.
