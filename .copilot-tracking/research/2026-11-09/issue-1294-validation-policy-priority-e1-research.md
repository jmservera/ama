# Research: issue 1294 validation policy, owner-authorized extra correction E1

## Brief

* Topic: what remains for #1294 after original cycles C1-C4 and the adverse independent exact-head C4 review. Extra cycle E1 of the two the owner authorized in this run (E2 only if a focused defect remains).
* Start: branch docs/demo-priority-validation-1294-1109, HEAD b085d7d3c (C4), clean tracked tree; origin/main b46a9ad9a; the C4 merge base was fa7ae0c97.
* Posture: focused, internal. Output: convergence. Extensions: hve-builder (loaded), hve-builder-tester (behavior), rpi-plan-critique.
* Non-goals: #1296, #1298, app source, deployment, AI calls, security hardening, workflow or tool edits, branch protection, push, PR, merge, issue ticking.
* Owner decision (this run): up to two extra focused cycles; a labelled proxy simulation with independent review and CI is acceptable when canonical behavior validation is unavailable. It is not native, intended-profile or qualified-human proof and does not waive independent exact-head review, hosted CI or human approvals.

## Evidence recovered

* Issue #1294 body: five unchecked acceptance criteria (AC1 reconcile CI versus local coverage; AC2 targeted tests and no blanket `--changed` for small/docs; AC3 retain full gate for major, SQL, infra, deployment, security, releases with stricter mixed tier; AC4 reconcile current wording and record/test five representative cases; AC5 dated RPI plus independent review and checks on the final candidate).
* Issue comment 2026-11-08T23:09:46Z (preserved, not edited): the proxy simulation limitation needs owner acceptance; the independent exact-head C4 review returned Revise (two High, three Medium, two Low); four cycles were exhausted; one more focused correction was requested for the omitted static-review scope, final-head local checks and receipt/SQL-selection guidance.
* Durable record of that independent review: none found. `.copilot-tracking/reviews/logs/2026-11-08/issue-1294-validation-policy-correction-c4-review.md` is the lead (non-independent) review of C4 with outcome Residual work RV-001..RV-004. A cloud and local session-store search returned no turn carrying the independent text. The seven findings are therefore known only through the issue comment's counts and themes; their exact text is missing evidence and is not reconstructed here.
* Retained, unchanged: C1-C4 research, plans, critiques, details, changes, reviews, behavior reports 1-5, sandboxes 2-5, static review C4 log.

## Current main changed the facts the guide cites

* origin/main moved fa7ae0c97 -> b46a9ad9a (#1299). Only `tools/rpi-checks.py` and its tests changed among gate files; none of the four policy files changed on main. A local merge with `--no-commit` was clean (no conflicts) and is staged, not yet committed.
* #1299 added a retained sensor analysis suite on the owned SQL Server: `SENSOR_MSSQL_SELECTOR` run in the SQL group with `ZF_SENSOR_MSSQL=1`, eight pinned required tests, exact count and zero skips; opt-in discovery skips tolerated only in `project-core`; local `--changed` now selects `mssql` for core paths containing `sensor` and three listed dependency paths.
* Hosted `src-ci.yml` mssql job: grep for sensor finds nothing, so the sensor MSSQL suite is local-only (hosted runs the store and assistant contracts only). The README local-only list and SQL example omit it. This is the receipt/SQL-selection guidance gap.

## Read-only selection probe (merged tools, bytecode disabled, /tmp/probe1294.py)

| Paths | Local `changed_groups` | `ci-affected.select` |
| --- | --- | --- |
| docs/reference/README.md, .github/copilot-instructions.md | preflight, namespace, static | all five projects, namespace, mssql |
| src/README.md only | preflight, namespace, static | no project, namespace false, mssql false |
| src/api web app.js plus employee_chat_browser_check.py | preflight, project-api, namespace, static, browser, image-api, logo-0600 | api, namespace, mssql |
| src/core mssqlstore.py | all projects, namespace, static, mssql, four images, logo | all five, namespace, mssql |
| src/core sensor_analysis.py | same as SQL (mssql selected via sensor rule) | all five, namespace, mssql |
| src/core/tests/dataset.py | all projects, namespace, static, mssql (listed dependency) | all five, namespace, mssql |
| infra/main.bicep | preflight, namespace, static, infra | all five, namespace, mssql |
| docs plus infra/main.bicep | same as infra | same |
| src/README.md plus app.js | same as chat | api, namespace, mssql |
| .github/workflows/src-ci.yml | full matrix | all five, namespace, mssql |
| tools/rpi-checks.py | preflight, namespace, static, tooling | no project, namespace true, mssql false |

The README examples remain accurate; the sensor-specific path is the only new fact. The probe was run by the lead, not claimed as a hosted observation.

## Remaining work (evidence-grounded)

* G1 README: add the retained sensor MSSQL suite as a local-only check (exact required tests, zero skips, `ZF_SENSOR_MSSQL=1`) and its local selection rule; note hosted mssql does not run it; extend the SQL example row and state that SQL-selection by `--changed` is an aid under the full tier.
* G2 Receipt guidance: restate in one place that for the full tier `--verify-receipt` runs against the actual current origin/main and a partial receipt or `--changed` run never satisfies it; the C4 guide already has the base rule, so only cross-check and tighten wording if a defect shows.
* G3 Static review scope: the C4 static review omitted the full set of current policy targets. E1 static review must read ALL current targets: `.github/copilot-instructions.md`, `.github/agents/ama-backlog-delivery-coordinator.agent.md` (whole tier, receipt, review, publication sections), `src/README.md` (local gate section, coverage section, receipt paragraph, CI paragraph), `docs/reference/method/tracking-retention-policy.md`, `.github/rubric/README.md` step 3 (dependent), the `docs/reference/log.md` 2026-11-08/09 entries and `docs/reference/README.md` index.
* G4 Dependent wording: `.github/rubric/README.md:353` still says every final-head validation is the complete local gate; it is a publication-lifecycle runbook for a full-tier candidate. Qualify as selected-tier (complete gate when the candidate is in the full tier). Retention policy already says selected-tier.
* G5 Instruction wording: the static C4 review L2 observation (tooling read as categorically focused) is cheap and in scope: say non-gate tooling.
* G6 Final-head local checks: run the planned focused checks (diff check, ASCII, link check, stale-wording search, selector probe, loader probe if cited) on the final frozen head and record command, count, exit. No `--changed` run.
* G7 Behavior: a fresh finite representative proxy simulation (docs, small employee-chat, SQL including sensor, Bicep/security, mixed, workflow/tool classification) after the final edit, labelled proxy, not native.
* G8 Provenance: append a supersession entry to `docs/reference/log.md` and a changes record stating the independent C4 review is only recoverable by issue comment; do not edit C4 bytes or the lead review.

## Disposition of the hosted/CI honesty requirements

* Hosted CI is not observed; the candidate is local and unpublished. For the real candidate paths hosted Source CI would select every project, namespace and mssql, but that is inference.
* The `mainprotect` ruleset retrieval claim in the README remains dated 2026-11-08 and is flagged for re-verification, not altered.

## Planning Readiness

Ready. Research disposition: executed (recovery). Questions closed: none requiring the owner.
