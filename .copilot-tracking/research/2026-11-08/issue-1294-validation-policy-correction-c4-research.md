# Research: issue 1294 validation policy, correction C4

## Brief

* Topic: independent C3 readiness findings F1-F8 (file readiness-findings.json, session files) for issue #1294; correction C4, the fourth and final cycle under the owner's four-cycle default (supersedes the C3 handoff statement). No fifth cycle.
* Start: HEAD 2f1aa2e4d42b79364b95622d6198975203c1417e, tree 97b940c4824d22ddb7bd9a6d54fc926beb960f77, base fa7ae0c9770e890f82482456bfcb8e97f1e05429; tracked-clean, only ignored tools/__pycache__.
* Posture: focused (bounded internal task, named targets, supplied failure evidence). Provenance: caller brief. No questions asked (inputs sufficient; automatic correction loop). Output mode: convergence.
* Scope: src/README.md wording; C3 changes record provenance; report 4 summary provenance; a read-only loader probe; HVE static assessment of the corrected behavior-bearing instruction targets; behavior stage under correction-run rules. Non-goals: workflow/tool/source change, fifth cycle, rewriting retained raw evidence or append-only history, native or hosted claims, ticking human box.
* Questions: Q1 F1 static evidence path; Q2 F2 hosted selection claims vs ci-affected.py and src-ci.yml; Q3 F3 BASE RELAXED vs unconditional rerun; Q4 F4 loader probe; Q5 F5 SQL path; Q6 F6 focused command example; Q7 F7/F8 provenance; Q8 behavior reuse eligibility.
* Extensions: hve-builder (selected, lifecycle), hve-builder-tester (selected for behavior), rpi-plan-critique later. Repository instructions apply.
* Prior attempt note: C1-C3 artifacts, sandboxes 2-4, reports 1-4 are historical and preserved.

## Wave 1 wider

Inline waves (no worker lanes: coupled, low volume). Evidence IDs are codebase C# with path:line.

* C1 .github/workflows/src-ci.yml:4 path filter; :17-30 `changes` job; :56-94 matrix steps each `if: matrix.run`; :281-290 `src-no-working-data` has no `needs` and no `if`, so it runs whenever the workflow starts; :293 mssql gated on `changes.outputs.mssql`.
* C2 tools/ci-affected.py:68-99 `select`: unknown path or unknown `src/<dir>` selects everything; `src/*.md` or `src/<project>/*.md` is inert; non-`src/` paths other than the NAMESPACE_ONLY tools select everything; any dependency manifest selects everything.
* C3 Read-only reproduction (PYTHONDONTWRITEBYTECODE=1, import by path): `src/README.md` alone selects no project, namespace false, mssql false; `src/README.md` plus `docs/reference/log.md` or any `.copilot-tracking` path selects all five projects, namespace and mssql; `src/core/src/zava_forward/core/mssqlstore.py` selects all five, namespace, mssql; `src/api/.../app.js` selects api, namespace and mssql (api is in MSSQL_PROJECTS); `src/newdir/x.md` selects everything; `tools/rpi-checks.py` selects no project, namespace true, mssql false. Output kept at .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-5/checks/selector-probe.txt.
* C4 src/README.md:150-154 (all-skipped example overbroad, omits data guard, unknown subdirs and accompanying paths), :242 (example row), :611-612 ("unit, lint and type checks still run for every project" contradicted by C1), :244 (SQL path), :115-120 (focused block), :288-297 (BASE RELAXED) versus :493-499 (unconditional rerun).
* C5 src/core/src/zava_forward/core/mssqlstore.py exists; src/api/src/zava_forward/api/mssqlstore.py does not (ls exit 2).
* C6 .github/agents/ama-backlog-delivery-coordinator.agent.md:509-511 and :759-770 permit an existing partial receipt when verification prints BASE RELAXED; :699-706 requires canonical HVE static and behavior evidence with source identity.
* C7 src/api/checks/employee_acceptance_check.py:498-510 loads three names through unittest.defaultTestLoader.loadTestsFromNames; a failed import yields a counted `_FailedTest`.

## Wave 2 deeper

* Q4: strict loader probe, run from src/api with a fresh `unittest.TestLoader` (sandbox 5 checks/loader-probe-runner.txt, loader-probe-unset.txt, loader-probe-exits.txt). With the runner path: loader.errors 0, the three flattened IDs equal the three names, exit 0. With PYTHONPATH unset: loader.errors 3, IDs are three `_FailedTest`, exit 1. This proves the reviewer's point that the C3 count-only probe could not distinguish success from three import failures (with an unset path the count would also have been 3).
* Q7: sandbox 4 pre-run-status.txt lists ` M docs/reference/log.md`, ` M src/README.md` and untracked C3 artifacts; the C3 changes record called it clean (F7 confirmed). Report 4 lines 13 and 19: the graded source was bd63b22 plus the uncommitted patch; the C3 outcome log entry was appended after grading, so "no source edit followed grading" and "last two log entries" overstate (F8 confirmed).
* Q8 whitespace: `git diff --check fa7ae0c..HEAD` reports 32 lines, all in retained raw sandbox files (policy-3 selection.txt, two policy-3 patches, policy-4 patch: trailing blank-context lines of patches and recorded output); the five source documents pass (exit 0). Raw files stay unchanged.
* Q1: the only retained static assessment is lead self-assessment at 8a5cab9 (report 1 lines 11-15). C1-C3 changed the targets since. Required: an independent fresh-context Medium-profile static-review subagent against the complete corrected candidate, then targeted closure if Revise, then behavior against the final state.

## Wave 3 contrarian

* Counter to F2 "unknown src subdirectories": the guide could keep the inert claim for exactly `src/README.md`; verified true by C3. Disposition: narrow the claim, not delete it.
* Counter to F3: the full-tier exact-base rule is intentional; the finding does not relax it. Disposition: distinguish full from partial; keep full exact-base.
* Counter to F5/F6 "cosmetic": the SQL path is a reproducible example that points at a nonexistent file and the focused block can pass an empty base (BASE_SHA set only in the earlier full block) and run resume on a successful receipt; both are contract-level accuracy defects for the policy examples, so fixed in the same batch.
* Counter to F1: could behavior simulation substitute? No; hve-builder contract: unavailable or other stages never convert to Pass; static must be an independent fresh-context assessment. Is an independent stage available? The host `task` tool provides general-purpose subagents (no model parameter), so run it as a proxy with honest labeling.
* Counter to "no fifth cycle": the behavior terminal rule must be bounded within C4; attempts are capped at two; a second Revise is reported as Revise with the exact blocker.
* F4 alternative (qualify only): the user requires the strict probe; do both: qualify the old record by a new provenance correction and add the strict probe.
* Hosted-claim risk: the actual candidate includes non-src paths, so hosted selection would widen once Source CI triggers; recorded as static inference, not an observed result.

## Synthesis and decisions

All eight findings confirmed against evidence; none inapplicable. Dispositions:

| Finding | Disposition | Action |
| --- | --- | --- |
| F1 High | Confirmed | Independent HVE static review (fresh general-purpose Medium proxy) of complete corrected targets after edits; targeted closure on Revise; record blob and file hashes, stage status, scope; report 1 preserved |
| F2 Medium | Confirmed | Fix README 150-154, 242 and 611-612: project steps run only for selected projects; no-project example limited to exactly `src/README.md`-style paths; data guard runs separately; accompanying non-src or unknown paths widen selection; fail-open; hosted results unobserved |
| F3 Medium | Confirmed | Fix README 493-499: full receipts exact-base and rerun on any change; partial receipts may remain valid with BASE RELAXED; other changes still need a new run |
| F4 Medium | Confirmed | Strict probe done (exit 0 / exit 1 evidence); README wording unchanged; new provenance correction qualifies the C3 count-only probe |
| F5 Low | Confirmed | Replace SQL example path with the core path; examples checked against ci-affected select and runner |
| F6 Low | Confirmed | Self-contained focused block with fetch and BASE_SHA; resume shown separately for a failed receipt only |
| F7 Low | Confirmed | New provenance correction in the C4 changes record; C3 record and raw status untouched |
| F8 Low | Confirmed | New provenance correction in the C4 changes record and the C4 report; report 4 untouched |
| Whitespace note | Confirmed | Record separate raw-patch whitespace finding vs source-document diff check |

Decision (convergence): one batch edit to src/README.md (+ the chat example's mssql note, a verified selector fact) and an append-only log correction entry; then HVE static review; closure; full behavior run; Review; commit.

Research disposition: executed. Planning Readiness: Ready. Posture focused. Re-entry: none; saturated.
