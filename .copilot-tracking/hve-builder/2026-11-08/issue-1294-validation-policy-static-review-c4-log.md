# Static review C4: issue 1294 validation policy

## Executor

Fresh-context static reviewer, read-only. Applied the hve-builder review rubric and requirements catalog (cited by category). Did not read `.copilot-tracking/` (other than this log), run tests or edit other files. Hosted CI claims were checked against files only.

## Files reviewed

* `src/README.md` lines 61-260 (local gate, hosted-versus-local section, direct checks, classification rule, policy table)
* `.github/copilot-instructions.md` (validation tiers paragraph, diff vs main)
* `.github/agents/ama-backlog-delivery-coordinator.agent.md` (tier, receipt and evidence rules, diff vs main)
* `docs/reference/log.md` (tail entries, 2026-11-08 validation-policy series)
* Read-only verification sources: `.github/workflows/src-ci.yml`, `tools/ci-affected.py`, `tools/rpi-checks.py` (grep), `src/api/checks/`

## Verified claims (no defect)

* Matrix jobs always start with `run` false for doc-only `src/*.md`; steps are `if: matrix.run`, namespace and mssql are gated, `src-no-working-data` is unconditional (`src-ci.yml` 70-94, 206, 284-290, 294; `ci-affected.py` 80-90, 102-107).
* `src-api` runs the employee acceptance check, design-system, regulatory UX, case journey checks and the chat-panel selector (`src-ci.yml` 102-118); the employee-chat harness is not run hosted.
* `AXE_SHA256`, `--required-scope`, `--exact-base`, `BASE RELAXED`, resume with `relax_base=False` exist (`rpi-checks.py` 82, 3229, 3225, 3149, 2776). The focused command example and resume example are executable as written.
* Tier statements agree across README 62-72, instructions 72-95, coordinator "Local validation tiers" (strictest-tier mixed rule, impact-based classification, doubt is full, absent/skipped CI is not a pass, partial receipt never full).

## Findings

### Medium

M1. Overclaim on selector widening. `src/README.md:166` says selection widens for "a non-`src/` path other than the gate-tool paths". In `tools/ci-affected.py:49-55` only `rpi-checks.py`, `test_rpi_checks.py`, `install-actionlint.py`, `test_install_actionlint.py` and `rename-zava*` are namespace-only. `tools/ci-affected.py`, `tools/test_ci_affected.py`, `tools/backlog-sync.py` and `tools/test_backlog_sync.py` pass the workflow path filter (`src-ci.yml:5`) but select everything. Category: Evidence fidelity (coverage claims must match actual files). Confirmed defect (a reader could expect a lighter hosted run for a `ci-affected.py` edit). Smallest fix: replace "the gate-tool paths" with the four named paths (or "the runner, installer and rename tools and their tests") and note the selector and backlog-sync tools select everything.

### Low

L1. Cosmetic, confirmed. The same section's path-filter bullet says "the gate tools and their tests"; the filter also includes `install-actionlint`, `backlog-sync` and their tests. Fix: "the listed tools and their tests".

L2. Cosmetic. `.github/copilot-instructions.md` "Small issues, tooling and documentation-only candidates take the focused tier" can be read as tooling being categorically focused; the following sentences make gate-tool edits impact-classified, so it is not contradictory. Optional fix: "Small issues, non-gate tooling and ...".

L3. Observation, no action. The first 2026-11-08 reconciliation entry in `docs/reference/log.md` (line 10942) still says gate-tool, workflow and Dockerfile changes take the full tier categorically. Later C1 entry supersedes it; the log is append-only, so this is acceptable. Not a defect.

L4. Unverified (not contradicted): README statements that the infra what-if runs only after Source CI when `infra/` changed with a repository variable, that the rubric workflow ignores only `.copilot-tracking/**`, and the `mainprotect` ruleset result were not checked in this review. README already labels hosted claims as inferred and tells readers to re-verify.

## Dimension notes

Workflow contract, evidence fidelity, safety (human/hosted gates retained), reference discipline (guide is single source, others link) and portability pass. Tool configuration was not assessed per the rubric.

## Verdict

Pass. No Critical or High findings; stated purpose met and tiers internally consistent. Recommend fixing M1 (one-line wording) before publication.

## Targeted closure (M1, L1)

* M1: Closed. src/README.md Selection bullet now names the namespace-only tools matching NAMESPACE_ONLY in tools/ci-affected.py and states ci-affected.py and backlog-sync.py select everything.
* L1: Closed. Path filter bullet now says "listed tools and their tests", consistent with src-ci.yml line 5.
* New findings: none (see checks recorded in the final response).
* Overall closure verdict: Pass
