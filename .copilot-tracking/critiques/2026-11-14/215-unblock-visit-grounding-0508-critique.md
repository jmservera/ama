# Critique: #215 unblock and visit grounding plan (single pass)

Execution: executed once on the final candidate. Verdict: proceed with amendments, all compatible and applied directly.

* Overlap with the PR #1576 test: do not duplicate; the new suite adds provenance, no-mutation, withheld-claim and rendered-copy contracts. Applied.
* Assertions must not depend on exact fixture prose: use payload fields and stable phrases from `SOURCE_LABELS` and `chat_case_answers`. Applied.
* Resident-consent wording is absent from source; asserting it would fail and adding it is not a bug fix. Rejected as a test assertion; recorded as follow-up. No conflict with a confirmed user decision.
* The Matrix base class adds inherited role tests (as in `PanelTests`); accepted.
