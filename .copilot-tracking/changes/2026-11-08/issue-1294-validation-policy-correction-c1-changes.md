# Changes: issue 1294 validation policy, correction C1

Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c1-plan.md
Details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c1-phase-details.md
Research: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c1-research.md
Critique (one run, verdict Revise, all findings applied directly): .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c1-plan-critique.md
Base HEAD before correction: 397ce435ae4dddfcf9279179656049b8b670b720 (tree 3a1faa5dc109c8deecf546cec6c3e4077cca2bc6); origin/main base fa7ae0c9770e890f82482456bfcb8e97f1e05429.
Tier: focused (guide and instruction wording only). Impact classification basis: no workflow, tool, source, SQL, infrastructure, deployment, dependency, Dockerfile or security-control file changed; only the four files below.

## Implementation evidence

* P01-T01 src/README.md: Shared, Local-only and Hosted-only sections rewritten (Trivy gate, SPDX, Bicep, migration and working-data guard are shared; only artifact upload and hosted runner, matrix and path-filter execution are hosted-only; the exact-count, zero-skip, named-test verification is local-only). Direct employee-chat check now states the runner contract: pinned AXE_SHA256 (verified with sha256sum), exit 0, `PASS employee chat:` marker, no `skipped` (case-insensitive), `<out>/axe-results.json` with exactly three ordered states, empty violations, integer non-boolean positive passes, the named chat-panel selector command with ZF_BROWSER_TESTS=1 giving Ran 1 test, named test passing, bare OK, no skip, and the 58-byte out limit. Contract sources read, not changed: tools/rpi-checks.py lines 82, 134-139, 1555-1624, 2336-2352, 2403-2406; src/api/checks/employee_chat_browser_check.py 381-404.
* P01-T02 impact-based classification in .github/copilot-instructions.md, src/README.md (lead, classification rule, examples row) and .github/agents/ama-backlog-delivery-coordinator.agent.md. Full tier kept for big features, releases, infrastructure, deployment, SQL, security-sensitive, mixed and unresolved changes; workflow, gate-tool, dependency-manifest and Dockerfile edits are classified by impact with a recorded basis and none is categorically safe or categorically full by file name.
* P01-T03 docs/reference/log.md: appended a dated correction entry; earlier entries untouched.
* Post-grade correction (behavior run 2, finding 1-3, Medium and Low): the working-data guard placement (hosted `src-no-working-data` job, local `static` group), the Local-only wording, and the case-insensitive skip and out-path notes in src/README.md. These edits were made after grading and not re-simulated.
* Divergence from plan: the plan expected the README table row to cite `--changed` selecting the full matrix for any workflow or gate path; reproduction showed tools/rpi-checks.py selects only preflight, namespace, static and tooling, so the wording was narrowed to match.

## Validation (focused tier; no blanket --changed run is claimed; hosted CI not observed)

* git diff --check: exit 0.
* Relative links and anchors scan of the four changed files (PYTHONDONTWRITEBYTECODE=1): no new broken link; docs/reference/log.md reports pre-existing historical broken links in older entries, untouched.
* ASCII scan of added lines: 0 non-ASCII lines (no em dashes).
* Stale-phrase grep ("three states report no violations and no skip", "Hosted-only: the Trivy", "any workflow, gate-tool, dependency"): no matches.
* Read-only reproduction of tools/rpi-checks.py `changed_groups(paths, [])` and tools/ci-affected.py `select`, outputs saved at /tmp/c1-evidence/selection-local.txt and /tmp/c1-evidence/selection.txt (the first attempt used a wrong call signature and printed TypeError for the local side; the second run, selection-local.txt, is the valid local result). Results: docs-only and src/README.md local groups preflight, namespace, static; hosted select for src/README.md gives no projects, namespace false, mssql false; a workflow path selects the full matrix locally and hosted; tools/rpi-checks.py selects preflight, namespace, static, tooling locally and hosted namespace only; infra/main.bicep adds infra. (ci-affected for docs/reference/README.md reported all projects selected, which differs from the guide's statement that other documentation is outside the Source CI path filter; the path filter is a workflow `paths:` filter evaluated by GitHub before ci-affected runs, so ci-affected output for an arbitrary path is not evidence that Source CI starts. Recorded as an unverified-hosted-behavior note.)
* git diff --name-only: .github/agents/ama-backlog-delivery-coordinator.agent.md, .github/copilot-instructions.md, docs/reference/log.md, src/README.md only (plus untracked .copilot-tracking evidence). No workflow, tool or source file changed.
* HVE behavior test run 2: .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-2.md (verdict Revise, proxy profile, simulation; one Medium correction applied after grading; not re-simulated). Raw evidence retained at .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-2. Run 1 report and log preserved.
* Containment: ignored tools/__pycache__ preserved and untouched; no deletions.

## Open items and follow-ups

* Re-execute the behavior test at the intended Medium profile when the host allows an explicit subagent model; re-simulate the post-grade wording.
* Owner or policy follow-ups (not changed): rubric workflow applicability to documentation PRs; whether a disabled what-if is applicable CI; approved-control-change procedure; whether the focused tier requires shared local checks; a single wrapper for the direct employee-chat check or hosting the harness in CI.
* Hosted CI unobserved; human review checkbox of the behavior report unchecked.
