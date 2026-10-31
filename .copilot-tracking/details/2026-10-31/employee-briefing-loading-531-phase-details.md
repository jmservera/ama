<!-- markdownlint-disable-file -->
# RPI Phase Details: Employee briefing loading assurance

## Metadata

* Task ID: 531
* Task slug: employee-briefing-loading-531
* Related plan: .copilot-tracking/plans/2026-10-31/employee-briefing-loading-531-plan.md
* Evidence: corresponding research C1-C7/W1-W5; existing API browser runner.

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Strengthen local outcome evidence | Partial; validation blocked | P01-T01 implemented, P01-T02 blocked |

<!-- rpi:phase id=P01 -->
## P01: Strengthen local outcome evidence

Existing UI already delivers source/time/type labels and safe feedback.
Do not rewrite it to manufacture new implementation. Add evidence for successful
real UI-to-API round trips within the existing constructed-data runner.
No runtime source, case fixture authority, external traffic or live site changes.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Successful reviews and guide

* Context: existing runner exercises required reasons, failed edit and history barriers, but successful outcomes deserve direct local proof.
* Intent: one independent browser context using current server and real endpoints; sequential fresh briefings for accept/edit/reject.
* Targets: src/api/checks/loading_briefing_browser_check.py and src/api/README.md.
* Dependencies: existing main/briefing_data; inspect exact report/review contracts before assertions.
* Expectations: capture record identity before action; observe actual 200 response, exact status/reviewer_action/reviewer_reason/override_text/review_evidence. Separately sign in a constructed Programme Manager and GET /api/continuity/export, select ai_records by id and compare full review fields. No aggregate report is used. After a same-ID second review returns 400 already-reviewed, export again and confirm retained record unchanged. Compare permitted case detail projections before/after, not full raw case/ledger data.
* Boundaries: one scenario/call, no existing test removal or runtime change.
* Completion evidence: diff and actual successful local run, precise README description and disclosed UX return.
* Unresolved items: live/specialist/human acceptance remains outside local completion.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate and reconcile

* Context: execute current candidate, do not recycle old reported passes.
* Commands from src/api in isolated pip venv:
  `PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`,
  `ruff check`, `ruff format --check`, focused mypy and
  `python3 -m checks.loading_briefing_browser_check --axe <pinned-file> --out <fresh-external-directory>`.
* Heavy commands: existing shared lock, wait 600 seconds; no unlocked fallback.
* Outputs: external session files, concise command outcomes in dated changes. Existing browser main owns synthetic.json/server.log under a repository .venv TemporaryDirectory and cleans it on exit; ordinary unit fixtures own temporary scratch. These are allowed parent operations, not retention deletions. The shared /tmp lock is permitted and retained.
* Completion evidence: Ruff check/format and focused mypy passed. Both first required checks and a second serial attempt timed out on shared flock before execution. No API counts, browser results or axe state outcomes exist. P01-T02 remains incomplete; only blocked-candidate assessment is supported.
* Post-Review publication: local privacy-safe commit, fetch main and reconcile the reviewed base, then `tools/rpi-checks.py --all --lock-timeout 600 --base <reviewed-current-main> --out <fresh-external-directory>`. This gate owns its lock: no outer flock. Fetch/verify receipt against current main before a separate independent exact-head assessment; verify again immediately before push. Drift requires a new gate, without silent rebase/history changes. Missing prerequisites block publication.
