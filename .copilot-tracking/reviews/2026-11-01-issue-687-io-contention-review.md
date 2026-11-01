# Issue 687 IO contention review (2026-11-01)

* Review execution: executed once. Outcome: conformant for the slice.
* AC1: unmet. Injected disk contention reproduces a possible explanation (a stall up to 59,647 ms in one group), but the original 2026-10-23 cause (image restores) stays unproven, and the injected search timing also exceeds the threshold unlike the original single failing group. AC2: met via PR #689 diagnostics. AC3: threshold unchanged; test, Ruff, format and mypy pass.
* Correction cycle (PR #720): writers are now stopped and joined inside the temporary-directory scope via ExitStack; the review comment on AC1 is accepted.
* Residual: hosted CI is the gate evidence; owner confirmation that AC1 is accepted. Use `Refs #687`.
