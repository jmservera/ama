---
title: Employee progress dashboard 533 phase details
description: Exact test and validation boundaries for the stock-scale acceptance slice
ms.date: 2026-10-31
---

Task: 533 / employee-progress-dashboard-533. Initial direction: no runtime
rebuild; add stock-scale evidence to the existing semantically covered views.
Base: 5666bd33e1827670e5c07e3e3063bbbe989b59d3.

<!-- rpi:phase id=P01 -->
## P01: Scale regression coverage

<!-- rpi:task id=P01-T01 -->
### P01-T01: Shared existing-home overlay and unit regression

Use scale_fixture.homes() defaults and the first four known synthetic case
templates from synthetic_data. Map existing generated home IDs, resident names
and home attributes onto templates; preserve explicit lifecycle test history.
Expected 60,000 cases: 15,000 each completed/reopened, open, withdrawn and
unknown-closure. Valid lifecycle 45,000; open 15,000; closed archive 45,000.
Known closure episodes 45,000, including 15,000 reopened. Keep existing small
AI records linked to admitted home IDs, without extra inferred activity.
Assert exact daily/weekly totals, final backlog, median/p90, current journey/
team/stalled/overdue and archive combined-filter first/final/empty/beyond IDs.
Inherited JSON/SQLite execution checks reader parity, not SQL Server acceptance.
No persistence or runtime mutation by reads; no removal of existing tests.

Authored within scope, not complete: original Review RV-001 identifies raw
cases replacing initialized store cases without required funding defaults.
Static checks passed; changed-candidate execution blocked by shared-lock
admission. Route fixture correction to later implementation, not this Review.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Scale Playwright and guide

Existing checker gets one explicit --scale flag and runs an additional real
owned loopback app with the shared fixture. Assert all six chart/table/API
values, exact totals, bounded 20-row rendering, all filters retained through
reload, final-page clamping, empty-result controls and demonstration label.
Retain ordinary small-fixture coverage. Axe hash and no page errors remain
required; store external JSON/screenshots, never fixture bytes in git.

Implemented as planned. Pinned axe retrieved; browser NOT RUN due shared lock.

<!-- rpi:phase id=P02 -->
## P02: Validation and evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Actual commands

From src/api, PATH=/tmp/mv/bin:$PATH and
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests:
python3 -m unittest discover -s tests -q; ruff check; ruff format --check;
python3 -m mypy; python3 -m checks.progress_browser_check --scale --axe
<pinned-external-asset> --out <new-external-directory>.
Set PYTHONDONTWRITEBYTECODE=1; external Ruff and mypy caches.
Focused failing checks precede full suite. Inspect actual lock owner and use
flock -n for standalone commands, never queue another heavy check. Parent's
actual locked baseline passed 43 tests in 8.175s using /tmp/mv, so PC-001's
worker-specific filesystem restriction does not block this execution context.
Existing pip-installed namespace distributions are present; caller explicitly
requires the listed PYTHONPATH. Use external caches and clean preflight.
No gate/workflow changes planned, so conditional gate unit selector/hash update
is inapplicable. Complete runner retains its own required tooling checks.

Observed: Ruff check/format and mypy passed (65 formatted files/123 typed source
files), git diff whitespace passed. Focused unit admission exited 1 without
running tests; full API and browser remain blocked. Earlier 43-test baseline
is not changed-candidate validation. Resume on explicit ownership coordination;
no polling or queued replacement. Original critique findings remain preserved.

<!-- rpi:task id=P02-T02 -->
### P02-T02: One independent Review

Reconcile completed tasks and observed evidence first. Reviewer reads bounded
diff, issue/research/plan/critique/details/changes and external validation, writes
only dated Review. Preserve residual live and full Fluent adoption limits.
Route any findings to later work, not another Review in this task. Any material
open finding blocks affected publication; one-pass Review is not approval of
defects. No same-task source correction or closure reassessment.

Executed once: Complete / Not accepted. RV-001 High fixture contract defect,
RV-002 High missing candidate validation/publication evidence and RV-003 Low
separate acceptance work. Original preserved; no second Review or fixes here.

<!-- rpi:phase id=P03 -->
## P03: Publication administration

<!-- rpi:task id=P03-T01 -->
### P03-T01: Local commit

gh api user supplies login/id; set repository-local noreply email for author and
committer. Include required trailer and all original dated evidence.

Executed: local WIP/source/evidence commit 235c3731, privacy-safe author and
committer, required trailer. Original critique/Review preserved; no acceptance
or publication inferred. P03-T02/P03-T03 blocked by RV-001/RV-002.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Complete gate and exact-head assessment

Fetch origin/main and run tools/rpi-checks.py --all --jobs 3 --lock-timeout 0 --base <main>
--out <new-external-directory>. Verify external receipt immediately before
authorized push with freshly fetched main. Source/base/tool/image drift
invalidates publication. No other-worktree touch, private input or cloud bypass.
Missing prerequisites/failing checks or material open Review findings block
publication; original failures stay. Runner self-locks; no outer flock.
Run python3 tools/rpi-checks.py --verify-receipt <external-receipt.json>
--base <fresh-origin-main-sha>. A fresh independent assessor reads exact HEAD/
base, full receipt and original finding dispositions, persists its
administrative conclusion externally, and makes no source/evidence commits.
Fetch and verify again immediately before push if assessment intervenes.
Any identity/input drift blocks publication and requires fresh applicable gate.

<!-- rpi:task id=P03-T03 -->
### P03-T03: Topic PR

Push feat/employee-progress-dashboard-533 and gh pr create --base main with
Refs #533, no closing keyword. Include original Review, exact evidence/receipt
and unmet live/human/hosted approvals. Leave merge to owner.
