<!-- markdownlint-disable-file -->
---
title: Resident survey publication correction phase details
description: Exact validation, review and publication contract for correction1
ms.date: 2026-10-31
---

## Metadata

Task `571-correction1`, slug `resident-survey-check-571-correction1`, parent 571.
Plan uses the same date/slug. Initial merged HEAD `e2e815e2`, main `a75bbdff`.
Approved coverage lock: no test/source/workflow additions/removals.

<!-- rpi:phase id=P01 -->
## P01: Validate merged correction

<!-- rpi:task id=P01-T01 -->
### P01-T01: Verify invariants and run requested validation

Verify ancestry, zero main score/workflow/runner/log delta and retained browser/
README delta. Existing pip environment `/tmp/ama-571-20261031-env` points to this
worktree and passes pip check. From src/api run
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests
/tmp/ama-571-20261031-env/bin/python -m unittest discover -s tests -q`,
`ruff check --no-cache .` and `ruff format --check .`.
Run complete `python -m checks.resident_assistant_browser_check --axe
/tmp/ama-571-axe-4.10.3.min.js --out <new-external-directory>` under
`flock -w 1800 /tmp/ama-rpi-heavy.lock`; retry lock admission once, not a failing
executed test. Existing check verifies axe hash and uses synthetic loopback data.
Keep exact outputs, counts, report identities and limitations in changes.
Light tests/lints require no lock. Never inspect/reuse foreign outputs.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Reconcile canonical evidence

Depends on P01-T01. Record actual commands/outcomes, source SHA256, base and
head, any missing-dependency recovery and prior adverse attempts. Reconcile
plan markers, these details, changes/state, blockers and remaining publication.
No broad cleanup; original artifacts retain historical states.

<!-- rpi:phase id=P02 -->
## P02: Review and publish

<!-- rpi:task id=P02-T01 -->
### P02-T01: Single independent correction Review

Depends on P01-T02. Activate rpi-review once for this distinct child; independent
reviewer writes only new correction Review. Original Review not repeated or
rewritten. Compare main...candidate source and correction evidence, actual
issue criteria and retained acceptance limits. Record outcome separately from
execution and route residual work, without a current-task Review loop.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit and exact-head gated publication

Depends on P02-T01. Git identity already resolved via gh api user; verify local
privacy-safe author/committer. Commit all task-owned original correction evidence
with required trailer. Create a clean detached task-owned validation worktree
from that exact commit if this checkout has ignored test inputs.
Fetch main; full runner command `PYTHONDONTWRITEBYTECODE=1 python3
tools/rpi-checks.py --all --lock-timeout 1800 --base <current-main-sha>
--out <new-external-directory>`. Runner owns the same global lock; an outer
flock would self-deadlock. Retry admission once using a fresh directory; preserve
failure. No partial tier, cloud fallback or altered hash/skip policy.
After full receipt passes, fetch main and verify receipt against it immediately
before independent exact-head assessment and push. No commit/source/tool/image
change between gate and push. Keep authoritative final receipt external;
post-publication status can live in session storage/PR to avoid self-invalidation.
Unresolved material correction Review findings or a non-approving exact-head
assessment block push/PR; route them to later work without repeating this Review.
Outside-scope human/live acceptance caveats do not become automated approvals.
Push original branch using `git push -u origin HEAD`; create PR main with tracked
original and correction artifact links. Closes only if independently reviewed
evidence proves root cause, local check/prompt agreement and unweakened resident
acceptance; otherwise Refs and named unproven criteria.
Never merge PR, force push or mutate issue approvals. Hosted/owner gates separate.

## Current Completion and Review Handoff

P01-T01 and P01-T02 complete. API exact discovery passed: 1430 tests in
758.350s, 320 explicit opt-in skips. Ruff check passed; 65 files formatted.
Complete resident check passed after shared-lock admission on first attempt:
Chromium 156.0.8078.4, pinned axe executed, 32 scans, zero violations, 42
incomplete-rule occurrences in 31 states, no console errors/external requests.
No dependency recovery or source change required. Changes records exact commands
and external hashes. P02-T01 and P02-T02 remain outstanding at Review handoff.
Human/AT/live/model/native zoom/WCAG acceptance not run or established.

P02-T01 now complete: exactly one independent correction Review, Complete /
Residual work; bounded source/merge/evidence approved, no material defect.
Low RV-001 retained outside scope. Reviewer supports three actual issue criteria,
not broader approval. P02-T02 pending evidence commit/full gate/verify/approving
exact-head assessment/push/PR. Final authoritative evidence remains external.
