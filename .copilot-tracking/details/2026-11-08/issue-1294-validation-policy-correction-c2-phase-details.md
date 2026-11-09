<!-- markdownlint-disable-file -->
# Phase details: issue-1294-validation-policy-correction-c2

Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c2-plan.md
Evidence: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c2-research.md (C2-C9)

## P01 Correct README wording

### P01-T01 Mixed rule and examples (F2)
* In the classification paragraph (src/README.md, "Any such change, any doubt and any mixed change takes the full tier") restate: a focused classification needs the recorded reason; a change with any permission, pinned action or image, package, secret, deployment path, security control or gate-semantic impact, or genuine risk-based doubt, takes the full tier. A mixed change takes the strictest applicable tier of its components: only full-tier components (SQL, infrastructure, deployment, security-sensitive, major, release, or an unresolved-risk edit) make it full.
* Also change the lead ("strictest tier" to "strictest applicable tier"), keep "doubt takes the full tier" verbatim, and inspect every "mixed" hit.
* Examples table: keep the documentation-plus-Bicep row (full) and add a focused-plus-focused row (for example documentation plus a small employee-chat change: Focused, union of the planned local checks, never claim a full receipt was needed or that CI covers the harness).
* Completion: AC1; grep for "any mixed change" returns nothing.

### P01-T02 Direct harness out and scratch (F3)
* Replace "Use an --out within the 58-byte limit described above" (and the other mention near the Local-only bullet if any) with the FR3 statement: direct `--out` only receives `axe-results.json` and has no evidenced length limit; 58 bytes is runner-specific (runner sets TMPDIR to `<out>/tmp`); the direct run's temporary and state directory (ZF_STATE, server log, synthetic data) is under `ZF_BROWSER_SCRATCH` (absolute, outside the checkout, else ValueError) or `<checkout>/.venv` when unset; Chromium inherits the caller TMPDIR, so a short TMPDIR is an unmeasured precaution.
* Completion: AC2.

### P01-T03 Log
* Append a dated correction entry to docs/reference/log.md; earlier entries untouched.

## P02 Validate and fresh behavior cycle

### P02-T01 Checks
* git diff --check; relative link and anchor scan; ASCII scan of added lines; stale phrase grep ("any mixed change", "58-byte limit described above"); reproduce changed_groups and ci-affected select read-only with PYTHONDONTWRITEBYTECODE=1 saving outputs under .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-3/checks/ (workspace only); git diff --name-only allowed set.

### P02-T02 Behavior run 3
* Invoke hve-builder-tester via the host skill tool. New sandbox .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-3 with run-state.md. Full run; fresh designer (no lead scenarios, no prior reports or reviews) is given only this required-topics checklist, not scenarios or expected answers, and must cover (add a runner-versus-direct `--out` and TMPDIR scenario): focused plus focused mix, focused plus full mix, documentation-only, small employee chat with complete direct evidence (digest, order, passes, marker, skips, selector one test) and direct `--out` behavior, SQL, Bicep or security, comment-only versus permission-changing workflow edits, CI absence and path filtering, corrected shared coverage (working-data guard as hosted src-no-working-data and local static; Trivy, SPDX, Bicep, migration shared; only artifact upload and hosted execution hosted-only). Executor hve-core-all:hve-artifact-tester, then a fresh grader given the examples table and contract. Model: host disallows override; label proxy. Write report 3.
* Any defect found is corrected once in one batch; a post-grade edit makes the verdict stay as graded (record honestly; no self-reuse).

## P03 Changes, Review, commit

* Changes record; one rpi-review; commit with Refs #1294 and trailer.

## Critique dispositions applied

See the plan's Critique Disposition table (PC-001 to PC-007, all applied directly).

## Terminal state (PC-003)

Any post-grade edit leaves report 3 at Revise with an unsimulated post-grade change flagged for the independent reviewer; no Pass claim, no self-reuse, no silent second run.
