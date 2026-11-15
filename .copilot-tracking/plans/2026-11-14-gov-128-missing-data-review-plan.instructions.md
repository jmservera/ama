# Plan: #128 AC2 and AC3

1. Add optional named human reviewer to `human_review_route` and `route_cases` (non-human attribution leaves a visible `named_reviewer_missing` blocker, never a drop); fail closed on malformed appointment history.
2. Add `aggregate_usability`: rejects staff or person identifiers, unknown measures, and unapproved minimum cell size; suppresses small cells; reports aggregates only.
3. Focused tests in `tests/test_journey_register.py`; ruff check and format (line length 100); unit tests for journey and paired-equity modules.
Critique: single self-critique found the API default must stay compatible with `paired_equity`; applied.
