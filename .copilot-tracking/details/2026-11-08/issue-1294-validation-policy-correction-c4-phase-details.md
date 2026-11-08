<!-- markdownlint-disable-file -->
# Phase details: issue-1294-validation-policy-correction-c4

Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c4-plan.md. Research: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c4-research.md (evidence C1-C7).

<!-- rpi:phase P01 -->
## P01 Guide and log corrections

* P01-T01 src/README.md (evidence C1-C6). Edits: (a) selection bullet (~150-154) and the "Documentation under `src/`" example (~242): project steps skipped only for unselected projects, example limited to `src/README.md` or `src/<project>/*.md` alone, data guard `src-no-working-data` runs separately, accompanying non-src or unknown `src/` paths widen selection (this candidate's own paths would select all projects, namespace and mssql: static inference, unobserved); (b) ~611-612 sentence: unit, lint and type checks run for selected projects; (c) ~493-499: split full vs partial receipt rule; (d) ~244 SQL path and hosted note; chat example hosted note adds that an api change also selects mssql and namespace; (e) ~115-120 focused block with `git fetch origin main` and `BASE_SHA=$(git rev-parse origin/main)`, resume shown as a separate failed-receipt-only command. Completion: statements equal selector-probe.txt and the workflow; ASCII; links resolve.
* P01-T02 docs/reference/log.md: append one correction entry (C3 count-only probe qualified; C3 dirty pre-run status; report-4 tested boundary: bd63b22 plus the uncommitted C3 README and log patch, with the C3 outcome entry and tracking records not simulated) and, after the verdict, one outcome entry. Earlier entries untouched.

<!-- rpi:phase P02 -->
## P02 Independent static assessment and closure

* P02-T01 After P01, dispatch a fresh-context generic Medium-proxy static-review subagent (hve-builder static-review template) against the complete corrected targets: src/README.md section "Hosted CI versus local gate coverage" and the local gate guide, .github/copilot-instructions.md, .github/agents/ama-backlog-delivery-coordinator.agent.md. It receives known paths, purpose, requirements, requirements-catalog and review-rubric paths; no author reasoning or prior reviews. Lead writes the static review log with file sha256 and git blob IDs, executor identity (model not observable), verdict, status and scope. If Revise: apply the complete finding set once, then one targeted closure limited to original finding IDs. A static Pass or closed Revise precedes behavior. Historical report 1 self-assessment preserved.

<!-- rpi:phase P03 -->
## P03 Final-state behavior loop

* P03-T01 Full run (source changed since the Revise-free run 4 and report 4 was not on this wording, so no reuse; correction-run reuse preconditions do not hold). Fresh designer (topic checklist only; adds topics: selected-project hosted checks, data guard, widening, partial vs full receipt BASE RELAXED, SQL core path, focused command self-contained), executor `hve-core-all:hve-artifact-tester`, fresh grader confined to the issue contract; nonblocking cosmetic observations not defects. Sandbox 5 (retain), report 5. Terminal rule: Pass freezes (no later guide edit); confirmed contract defects are applied in one batch and attempt 2 (sandbox 6, report 6) runs fresh and full; after the last attempt no guide edit; Revise is reported as Revise with the exact blocker. Source identities (sha256 and blob IDs) captured immediately before executor dispatch and after grading to prove no edit.

<!-- rpi:phase P04 -->
## P04 Validation, Review, commit

* P04-T01 Checks: strict loader probes (done), selector probe (done), `git diff --check` over the five source documents, link scan, ASCII, append-only log, stale-phrase grep; raw-patch whitespace (`git diff --check base..HEAD` limited to .copilot-tracking sandbox files) recorded separately.
* P04-T02 C4 changes record with provenance corrections (F7: the C3 changes record line 37 called the pre-run status clean while sandbox 4 pre-run-status.txt lists two modified files and untracked C3 artifacts; F8: report 4 line 13 and 19 boundary); one Review via rpi-review; commit with Refs #1294 and trailer; verify clean tracked tree and report HEAD and tree.

## Critique corrections (PC-001..PC-008, applied)

* P01-T01: image-paths also gates project jobs; inert markdown means markdown directly in src/ or under a project directory; receipt paragraph cross-references the BASE RELAXED rule; resume command uses the failed receipt's recorded base.
* P01-T02: the correction entry also carries the F7 and F8 provenance corrections.
* P02-T01 / P03-T01: static label, executor type and rubric recorded; any later source edit requires targeted static closure before the next behavior attempt; final static hashes must equal committed targets; still-Revise is reported Revise.
* P04: selector run on the real candidate file list; probe script saved; tier basis recorded in the changes record.
