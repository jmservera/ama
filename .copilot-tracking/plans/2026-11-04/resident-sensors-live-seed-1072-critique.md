<!-- markdownlint-disable-file -->
# Critique: resident sensors live seed plan (#1072)

Execution: inline, once, by the implementing agent (no separate reviewer). Verdict: proceed with the stop-and-record plan.

* Applied: the plan must not claim the live fix; the PR uses `Refs` only.
* Applied: the stale-data blocker (backfill ends 2026-09-30) is part of the owner decision, since seeding alone would not render the forecast.
* Rejected: using a temporary SQL firewall rule or public access, because `infra/README.md` forbids it.
* Rejected: adding the operator as SQL Entra admin or running a new job definition without separate approval; both are access changes the task told us not to guess.
