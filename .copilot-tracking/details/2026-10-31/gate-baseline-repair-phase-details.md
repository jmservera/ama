<!-- markdownlint-disable-file -->
# RPI Phase Details: Complete local gate baseline repair

## Metadata

* Task ID: a81da11b-4af4-4c2c-bd8a-ca8a765c6fd4
* Task slug: gate-baseline-repair
* Related plan: .copilot-tracking/plans/2026-10-31/gate-baseline-repair-plan.md
* Evidence: .copilot-tracking/research/2026-10-31/gate-baseline-repair-research.md, C1-C7

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Repair and validation | complete | P01-T01 through P01-T03 |
| P02 | Review and publication | original Review complete; publication pending | P02-T01 through P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Repair and validation

The clean original full gate failed browser strict lint and static tooling
synthetic-output parsing. Lists remain live by identity; capture defaults do
not copy them. No production skip policy edits.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Bind closures

Target: src/api/checks/case_journey_browser_check.py.
Bind lambda lists with keyword-only defaults, threads(route, *, change=change,
held=held), and hold(route, *, held=held) with proper Route/list types. Playwright
passes route and request positionally; keyword-only binding prevents the request
from overwriting the captured default. Bind snapshot in route
fulfillment. Preserve later unroute using the same callback function identity.
Use pinned Ruff isolated check E,F,I,B,UP, py312, line length 100, and formatter
from src/api with checks/... paths, exactly matching the gate. Running isolated
Ruff from root changes inferred first-party import ordering and is not an
equivalent proxy. Retain the original playwright-before-checks import order.
Completed: zero nine original B023 findings, strict formatter/lint and real
journey execution with 87 axe scans and zero violations.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Capture adversarial fixture output

Target: tools/test_rpi_checks.py existing exact discovery/integration test.
Use contextlib.redirect_stdout and io.StringIO for the two deliberate
Runner.command calls only. Assert the transcript contains the fixture skip.
Existing runner.rows assertions and browser GateError remain unchanged.
Do not capture the whole real suite or modify check_skips. Zero added methods,
zero removals. Completion: full tooling tests pass and no skip transcript
appears as a parent test result in verbose output. Completed: 39 tooling tests
pass and captured transcripts remain asserted internally.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Validate and document

Use an external pip venv, installed src distributions and shared test fixture
paths with API tests first when selecting test_chat_panel (core has a same-name
module). Set PYTHONDONTWRITEBYTECODE and external Ruff/mypy caches. Actual
Chromium runs under flock -w 1800; the full gate uses its own lock.
Run three gate browser checks with pinned axe and exact chat selector, API
unittest discover with core/agents fixtures, configured Ruff/format and mypy.
Document baseline repair and unchanged chat scope in src/api/README.md.
Preserve original external logs; no historical receipt relabelling. Completed:
1430 API tests with 320 expected discovery skips, API Ruff/format/mypy,
three actual browser checks; journey 87 scans, regulatory 21 scans, zero
violations. Exact unchanged chat selector one executed, zero skipped.

<!-- rpi:phase id=P02 -->
## P02: Review and publication

No claim of production, hosted or human acceptance from local results.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Independent original Review

A fresh worker activates rpi-review, assesses source diff and reconciled plan,
changes and validation. Write only its original dated Review artifact.
Record execution separately from outcome and preserve every original finding.
No repeat Review or return to Implement in this task. Unresolved material
findings block publication and route to later work. An adverse final independent
exact-head assessment likewise blocks publication. Completed: one original
independent Review, execution Complete, outcome Conformant for P01. RV-001 and
RV-002 are Low non-blocking residual work, not implementation corrections.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Final gate and publication

Commit implementation plus original RPI evidence using gh-resolved noreply
author/committer email and Copilot trailer. Default to no deletion and prevent
outputs with external caches and bytecode controls. For necessary own generated
pip metadata cleanup, use a finite explicit selection with archive identity,
full tracking snapshot preservation, archive readback, restored byte equality,
protected-input checks and a removal journal before pruning; absent that
authorization/evidence, stop publication. Never delete historical records,
foreign outputs, original adverse evidence or active RPI artifacts.
Use fresh external --all --jobs 3 gate with reviewed current origin/main;
never outer-lock this self-locking runner. Wait for contention rather than
abandoning. Fetch main, verify exact receipt, obtain exact-head assessment,
push normally and create a main PR using Refs #572. Keep receipt external.
Any later source/base/tool/input drift requires fresh gate evidence. Incorporate
current main e64c6e6c9da407682de59b926944424f94f50671 by ordinary fast-forward;
#600 supplies stricter exact-chat execution verification, not the fixture stdout
repair. Preserve the historical a75bbdff failed reproduction. A later main
advance to 5198a1ff overlaps the API README; commit the current assessed work
first, then ordinary merge current main without stashing or rewriting history.
Final assessment will evaluate that committed candidate and current base.
Current main later advanced to 28fbe6b6 (#604), independently publishing the
same closure/fixture repairs. Preserve all incoming source and its added
outer-suite regression. Net source difference is two lines independently
asserting each captured command transcript; no case-journey source delta
remains. Original research, critique and Review remain unchanged history.
