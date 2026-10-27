---
title: Resident account control implementation evidence
ms.date: 2026-10-27
---

Task #467, parent #466. Implementation scope: P01. P02 remains review/publication.
Plan/details/research/critique are dated 2026-10-27 with the same task slug.

## P01 Implementation

Implemented authorised own-email projection and native header account disclosure.
One critique executed (Revise); PC-001 directly resolved before source edits by
locking safe test commands/targets. No second critique.

## Environment and Validation

System import lacked project distributions; system pip correctly refused the
externally-managed environment. Created `/tmp/ama-467-venv` and installed core,
agents and api[dev] with pip successfully. No dependency manifest changes.
Passing:

* Focused API: from src/api, `PYTHONPATH=../core/tests:../agents/tests
  /tmp/ama-467-venv/bin/python -m unittest discover -s tests
  -p test_resident_demo_api.py -q`: 39 tests, 29.266s, OK.
* Focused core: from src/core, `/tmp/ama-467-venv/bin/python -m unittest discover
  -s tests -p test_resident_showcase.py -q`: 39 tests, 3.206s, OK.
* Changed-file Ruff check and format: app.py, test_resident_demo_api.py and
  resident_account_check.py pass (browser format uses isolated 100-character rule).
* Mypy on those three files: Success, no issues.
* `node --check src/api/src/zava_forward/api/resident_demo/web/demo.js`: pass.
* From src/api, `PYTHONPATH=tests /tmp/ama-467-venv/bin/python
  -m checks.resident_account_check`: pass. Actual local HTTP server health=200;
  Chromium verifies anonymous hiding, own identity, reload, native summary
  accessible name, Enter/Space toggle, Tab logout, Escape focus, outside dismissal,
  logout focus/revocation, second account isolation, failed logout privacy/
  message/focus and retry, long email at 320/390/1280px, right-edge placement,
  reduced motion and expired-session hiding; no JavaScript errors.

Initial browser run failed because Chromium's native summary is not selected by
Playwright's button-role query. Corrected the test to native summary locator plus
accessible-name assertion (no custom role added). Initial format check required
formatting. Initial mypy run found duplicated namespace imports; followed the
existing checks' top-level test fixture import pattern with PYTHONPATH=tests.
All these final checks then passed. No failure is represented as a pass.
Full API discovery finished: from src/api, `PYTHONPATH=../core/tests:../agents/tests
/tmp/ama-467-venv/bin/python -m unittest discover -s tests -q`: 1069 tests in
577.664s, OK (skipped=308). Repository optional/integration skips are not passing
SQL tests. Raw output is retained externally at `/tmp/ama-467-api-tests.log`.
Final Ruff check and mypy cover all four changed Python files, including the
compatibility SQL harness: all pass / no issues in 4 source files. Ruff format
passes for both source/test files and both browser scripts (isolated 100-column
format for checks). Compileall of both check scripts and git diff --check pass.

## Web Guidelines Check

Current source fetched before implementation and refreshed before Review on
2026-10-27. Changed web files read against all fetched rules, with repository
Fluent/WCAG/plain-ASCII content standards taking priority over generic copy.
Existing immediate logout is intentionally preserved; no destructive data write,
custom ARIA menu or URL-synchronised account disclosure is introduced.

### src/api/src/zava_forward/api/resident_demo/web/index.html

Pass for changed account markup: native details/summary/button, accessible name,
text-only identity, decorative logo unchanged, no inline event handler.

### src/api/src/zava_forward/api/resident_demo/web/demo.css

Pass for changed rules: tokens, visible inherited focus, hover, 44px target,
wrapping, bounded panel and reduced-motion behavior confirmed in Chromium.

### src/api/src/zava_forward/api/resident_demo/web/demo.js

Pass for changed behavior: textContent, native keyboard toggle, Escape focus,
outside dismissal, account reset and existing honest async messages.
No new substantive file:line finding. This is not a full-site or screen-reader
conformance claim.

## Amendments, Divergences and Blockers

No material divergence. Owner's explicit focused-check direction supersedes
the repository full local gate for this task only. No Azure/SQL/private data/
secrets/environment files/verifier files used. Core cap remains untouched.
Directly relevant current-state update: the existing SQL-backed browser check
expects immediately visible logout at four sites. Open the disclosure before
those accesses to preserve it for later/hosted execution. No SQL harness run.
This additional existing-file edit is reflected in plan/details and static targets.
The only new browser file remains the no-SQL account check.

## Review Handoff

P01-T01/T02/T03 complete, plan and phase details reconciled. Exactly one
independent post-implementation Review is next; P02 publication is still
pending. No active implementation blocker or substantive open finding.

## Independent Review Result

One independent Review completed: execution Complete, outcome Conformant, no
substantive findings. Original critique and Review preserved unchanged.
Reviewer independently reran 39 API and 39 core tests, static checks and JS
syntax; full API/Playwright results are explicitly attributed to parent evidence.
No repeat Review, source correction, deployment or merge. P02-T02 publication
is the remaining approved action; hosted CI/rubric and human review are pending.

## Publication

Implementation and original dated RPI evidence committed as fab2d93d with the
Conventional Commit style and required Copilot trailer. Author/committer email
resolved from gh api user into the account's noreply address and configured only
locally. Normal non-force topic push succeeded.

PR #471: https://github.com/jmservera/ama/pull/471, base
`feat/resident-interactive`, head `feat/resident-account-control`; body explicitly
declares stacking dependency and uses Refs #467 / Refs #466 only. No merge.
This publication-receipt update changes only tracking evidence, not reviewed
source. Hosted CI/rubric and owner approval remain pending, not local passes.
No task-specific follow-up established and no child task started.
