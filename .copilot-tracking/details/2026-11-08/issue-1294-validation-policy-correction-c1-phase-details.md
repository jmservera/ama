<!-- markdownlint-disable-file -->
# Phase Details: issue-1294-validation-policy-correction-c1

Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c1-plan.md
Evidence: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c1-research.md (C1-C23)

## Planning State

* Interpreted goal: wording-only correction of four review findings; HEAD 397ce435 is the baseline.
* Boundaries: only the files listed in the plan; read-only tool/workflow evidence.

## P01 Correct the guide and instruction wording

* P01-T01: in src/README.md replace the "Local-only"/"Both"/"Hosted-only" bullets and the direct-check paragraph. Local-only keeps the harness with its full contract (C1-C7), exact-count zero-skip selector (C8-C10), SQL selectors, probes, receipt binding. Shared lists chat-panel selector, Trivy gate, SPDX, Bicep, migration and working-data guard with the runner/CI locations (C11-C19), noting hosted `src-no-working-data` is its own job. Hosted-only lists artifact upload retention, hosted runners, matrix and path filter. Direct check: command with the pinned axe 4.10.3 whose SHA-256 equals the runner `AXE_SHA256` (verify with sha256sum), stdout must contain `PASS employee chat:` and no "skipped"; `<out>/axe-results.json` must be a list whose `state` values equal, in order, actual-model-unavailable, synthetic-cited-answer, demo-disclaimer-model-answer, each with `violations` equal to `[]`, `passes` a positive integer, and no "skipped" text. Selector run with `-v` and `ZF_BROWSER_TESTS=1` must show `Ran 1 test`, the named test passing, bare `OK`, no skips.
* P01-T02: instructions paragraph, README lead, coordinator tiers paragraph and table row "Gate tool or workflow": classify by actual impact. Full tier for big features, releases, infrastructure, deployment, SQL and security-sensitive impact, mixed, and genuinely unresolved risk. State that workflow, gate-tool, dependency-manifest and Dockerfile edits are classified by what they change; permissions, pinned actions, images, packages, secrets, deployment or security controls are full; a demonstrably non-security tooling or documentation edit stays focused with planned local checks; none is categorically safe.
* P01-T03: append a dated correction entry to docs/reference/log.md without editing earlier entries.

## P02 Validate and repeat behavior testing

* P02-T01: `git diff --check`, relative-link scan, ASCII scan of added lines, stale-phrase grep, read-only reproduction of changed_groups and ci-affected.select (bytecode disabled) for the table paths, and a check that each table example matches wording.
* P02-T02: invoke hve-builder-tester; independent design subagent, hve-artifact-tester executor, independent grader, profile resolved against what the task tool accepts, retained sandbox under .copilot-tracking/sandbox/, report at .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-2.md; report Deferred with the exact blocker if a mandatory stage fails.

## Critique dispositions applied (PC-001..PC-006)

* P01-T01 additions: three entries in order; `passes` an integer, not boolean, above zero; exit 0; marker in stdout and JSON present; fresh external `--out`. Selector Shared for execution, Local-only for exact-count, zero-skip and named-test verification; command from `src/api` with the runner's `PYTHONPATH` (`tests_env("api")`), `ZF_BROWSER_TESTS=1`, `python -m unittest -v test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log`.
* P01-T02 additions: record impact classification and basis; focused for these file classes needs a stated reason that permissions, pinned actions or images, packages, secrets, deployment or security controls and gate semantics are unchanged; doubt or mixed takes full; `--changed` selecting the full matrix is an aid, not a tier.
* P02-T01 stale phrases: "three states report no violations and no skip", "Hosted-only: the Trivy", "any workflow, gate-tool, dependency", "Gate tool or workflow | ... | Full"; also `git diff --name-only` limited to the plan scope plus tracking; `PYTHONDONTWRITEBYTECODE=1`; exits recorded; no `--changed` run claimed.
* P02-T02 rules: new sandbox path (not the removed policy-1), no reconstruction; designer receives no lead scenarios; grader receives the examples table and full contract; proxy or unresolved profile caps at proxy/Deferred; Deferred names the rerun condition; scenarios cover zero-pass, wrong-state, a skipped selector, categorical-tier phrasing.
* P03: repository-local noreply email; earlier review and behavior report preserved; no push; hosted CI not run; exact-head review and human/hosted approvals still required.

## P03

* Complete the changes record, run rpi-review once into a new correction review record preserving the existing review, commit with `Refs #1294`.
