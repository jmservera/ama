<!-- markdownlint-disable-file -->
# RPI Phase Details: Live Azure verification

## Metadata

* Task ID: 3a44be57-db3a-46d1-b9e4-fe82bd7c74e7
* Task slug: live-azure-verification
* Related plan: .copilot-tracking/plans/2026-10-31/live-azure-verification-plan.md
* Evidence: .copilot-tracking/research/2026-10-31/live-azure-verification-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Execute live verification | Complete observations; employee blocked | P01-T01 |
| P02 | Record evidence | Complete | P02-T01 |
| P03 | Review and publish | Original Review ready; publication pending | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Execute live verification

<!-- rpi:task id=P01-T01 -->
### P01-T01: Prepare safe driver and run bounded checks

* Context: employee adapter is capture-free and local CLI is not live auth; resident mains are owned fixtures.
* Intent: actual live observations with the requested limits.
* Targets: dated driver/result under .copilot-tracking/changes/2026-10-31/; missing namespaces installed in external venv with pip.
* Dependencies: one critique; independent expected IDs before employee admission.
* Boundaries: no Azure changes, persistent browser state, raw console/body output, credential echoes, booking/consent/record updates or API mocks.
* Validation: health up to 120 seconds/request; first navigation up to 180 seconds, app stages 120 seconds. Health may be retried without signing in. Credential submission increments account counter before click; absolute maximum two, preferably one.
* Employee: directory resolution via captured subprocess output, or independently supplied expected IDs; never extract expected values from actual /api/me. If unresolved, zero employee sign-ins and blocked employee actions. Public login-shell assets remain measurable.
* Resident: internal credential parser, one login; observe existing account/content visibility, use existing assistant selectors and no-content geometry checks. Ask at most one generic advisory question only if safe and necessary; no callback consent/agenda.
* Assets: only public same-origin scripts/styles, SHA256 and byte counts, first-context load errors as counts; no raw login/auth URLs or identity claims.
* Completion: date/version/command, per-surface results, attempt counters and fixed reason codes in sanitized JSON.
* Unresolved: directory rights, exact credential format and runtime reachability measured internally.

#### Origin and attempt contract

| Account slot | Exact owner-supplied origin | Auth boundary |
| --- | --- | --- |
| Employee | https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io | Intended Entra flow on https://login.microsoftonline.com only; matches adapter APP |
| Resident | https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io | Same-origin resident login form only |

The single driver owns all credential submissions. Before any submit, persist
the account's incremented count in the sanitized result JSON and fsync it.
Use an exclusive file lock on that JSON throughout execution; never reset an
existing record. If a prior execution is interrupted, refuse further sign-ins
until its known consumed budget is reconciled; the planned implementation
conservatively refuses ordinary rerunning of a started driver. A narrowly
guarded employee-only continuation is permitted only from completed,
identity-matching, monotonically validated checkpoints with zero employee
submissions; resident observations and all prior checkpoints remain preserved.
Credential-free self-tests
exercise count==2 denial and interrupted-run denial without reading accounts.

#### Supplemental observation matrix

| Surface | Action/invariant | Projection and classification |
| --- | --- | --- |
| First assets | Attach response/requestfailed/pageerror observers before first goto; actual same-origin JS/CSS bytes, explicitly Leaflet/workspace scripts; no later fetch substitutes | Path, status, bytes, SHA256/local match, error counts; initial/retry distinction. Missing/failed required asset fails; version mismatch means deployed/source difference, not automatically a bug |
| Case tabs | On first case navigation observe one selected visible tab/panel, switch each offered tab, verify aria-selected and linked panel visibility | Count and booleans, no panel text; missing controls fail requested layout, identity absence blocks |
| Capacity | Observe both API responses on hash navigation, compare package/workorder counts with actual rendered sections or consistent empty wording | Status/count/render agreement; visible alert is failed with retry flag, unauthorized/identity absence blocked |
| Other manager pages | Read-only overview, progress, visits, funding, finance, closed; observe relevant request statuses and rendered expected container | Per-route boolean/error count, no records; no failure injection |
| Resident resize | 1280x900 and 390x844; open Chat, activate offered width/height controls, require meaningful geometry change and containment/no page overflow | Bounds, selected value, disabled state; absent controls fail, auth absence blocks authenticated content but public chat geometry remains testable |
| Resident dock | Toggle Dock to right edge on wide viewport; aria-pressed true, right edge within 2px, height control disabled; undock restores false/enabled | Booleans and bounds; no question/consent submission required for geometry |
| Metering | GET /api/ai/report?start=2026-10-31T00:00:00Z&end=run-start-UTC&as_of=run-start-UTC | Status and allowlisted coverage/token_cost/cost_per_accepted_proposal/field presence; unavailable/incomplete/held/Unknown distinct from success. No raw ledger records; no limit/billing/quality criterion inferred from schema alone |

<!-- rpi:phase id=P02 -->
## P02: Record evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update documentation and GitHub issues

* Context: #523/#524 live rows unchecked; #570 immutable identity and actual chat/map/case; #432 nine distinct economics criteria.
* Targets: docs/architecture/cutover-evidence-pack.md, docs/reference/README.md, append-only docs/reference/log.md, target GitHub issues.
* Dependencies: sanitized result.
* Boundaries: no retrospective alteration of historical verdicts; no passing unchecked metering criteria from source tests or chat. A plain recorded pending result meets #523/#524's literal live-record criterion but must clearly remain pending, not successful acceptance.
* Validation: re-fetch issue bodies immediately before checkbox edit, match exact criterion text, preserve all other body text, reread changed issue and comment URLs.
* Bugs: search existing open issue first; new title, exact route/control, viewport, reproduction, observed result and expected behavior; no identity/record IDs. Do not create duplicates for existing identity blockage.
* Completion: docs and GitHub agree on actual observed results and limits.

<!-- rpi:phase id=P03 -->
## P03: Review and publish

<!-- rpi:task id=P03-T01 -->
### P03-T01: Independent Review, commit, full gate and Refs PR

* Context: repository requires complete local gate for final RPI candidates.
* Targets: original review log and state; external final receipt; Git topic/PR.
* Dependencies: reconciled plan, details, changes, evidence; exactly one original post-implementation Review.
* Boundaries: no force push, rewrite, main commit, protection changes, cloud gate fallback or claiming hosted/human approval.
* Validation: privacy-safe changed diff; resolve gh account id/login and repo-local no-reply author/committer; Copilot trailer. Commit final candidate then fetch main, run tools/rpi-checks.py --all --base current-origin-main --out new-external-dir; verify default full receipt immediately before push and independent exact-head assessment.
* Completion: normal git push -u origin HEAD and main-targeted Refs PR with artifact pointers and truthful gate/live limits.
* Unresolved: missing gate prerequisites block publication; install trustworthy pinned missing tools only after actual failures.

## Implementation Evidence

* P01: executed 2026-10-31 15:42:51-15:45:41Z; one resident sign-in, zero employee.
* Resident geometry and actual first-navigation assets passed; independent
  employee directory lookup exit1/access denied, blocking authenticated checks.
* Initial append-mode journal and unsupported employee password-only format
  were corrected in the sole driver before any employee attempt; original
  checkpoints and resident observations remain in the result.
