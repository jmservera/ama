# Plan: issue 144 queue request-date correction C1 (2026-11-09)

Research: [research](../../research/2026-11-09-issue-144-queue-request-date-c1-research.md). Details: [details](../../details/2026-11-09/issue-144-queue-request-date-c1-details.md).

Written before any source edit (operation order: originals persisted, research, this plan, then source/test edits).

* [ ] Implement: add fresh `x-ms-date` in `AzureTaskQueue._call`; add contract-enforcing offline regression.
* [ ] Review: one self review; independent exact-head review by the same reviewer remains pending and no human approval is claimed.

Validation tier: owner-selected demo-targeted (no `rpi-checks --all`). Commands: agents queue, worker, dispatch and dependency tests; ruff check and format --check and mypy on changed modules with pinned ruff 0.17.1 and mypy 2.4.0 in an isolated pip venv.

Critique (single pass): proceed. Applied: use `x-ms-date` only (documented alternative to Date, no duplicate); generated per call via `email.utils.formatdate(usegmt=True)`; keep headers otherwise unchanged. Rejected: new dependency, clock injection, hosting or identity wiring.
