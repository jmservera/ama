<!-- markdownlint-disable-file -->
# Changes: issue 1294 validation policy, correction C2

Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c2-plan.md
Details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c2-phase-details.md
Research: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c2-research.md
Critique (one run, Revise, all applied directly): .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c2-plan-critique.md
Base HEAD before correction: 7260826bcc4ba8688baccf75b651780ccd0b0d11 (tree 3d990a5a48aba65b8c07f9d3b71095d5b5ee780c); origin/main base fa7ae0c9770e890f82482456bfcb8e97f1e05429.

## Classification (PC-007)

* Tier: focused. Basis: guide wording only in src/README.md and an appended entry in docs/reference/log.md; no workflow, tool, dependency manifest, Dockerfile, source, SQL, infrastructure, deployment or security-control file changes.
* Allowed paths: src/README.md, docs/reference/log.md, .copilot-tracking C2 artifacts, .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-3, .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-3.md.
* Pre-edit status: `git status --short --ignored` shows only `!! tools/__pycache__/` plus the untracked C2 research, plan, details and critique files.

## Implementation evidence

### P01 guide corrections (src/README.md, docs/reference/log.md)

* Mixed rule: line 68 now "strictest applicable tier"; the classification paragraph says any such change and any doubt takes the full tier, and a mixed change takes the strictest applicable tier (two focused stay focused; any full component makes it full). Examples table has two labelled mixed rows (documentation plus infrastructure: full; documentation plus small chat change: focused). Doubt wording kept verbatim (PC-001, PC-002).
* Direct harness: removed "Use an --out within the 58-byte limit described above"; now states direct --out only receives axe-results.json with no evidenced limit, the 58-byte limit is the runner's (TMPDIR=<out>/tmp), scratch/state under ZF_BROWSER_SCRATCH (absolute, outside checkout, else error) or <checkout>/.venv when unset, short TMPDIR an unmeasured precaution (PC-004).
* docs/reference/log.md: appended a dated C2 correction entry; earlier entries untouched.

### P02 validation (outputs under .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-3/checks/)

* `git diff --check`: exit 0 (diff-check.txt, rerun after the post-grade batch: exit 0).
* Link/anchor scan of the three guides: exit 0, no broken links (links.txt). Pre-existing broken links in docs/reference/log.md are untouched.
* ASCII scan of added lines: 0 non-ASCII.
* Stale-phrase grep ("any mixed", "genuine risk", "within the 58-byte"): no matches (exit 1); every "mixed" hit reads strictest applicable.
* Read-only selection reproduction (selection.txt, exit 0): src/README.md alone selects local preflight, namespace, static and no Source CI project; README plus app.js selects project-api, browser, image-api and others locally and api in ci-affected; infra change adds infra; workflow edit selects the full matrix. These are local selector outputs, not hosted path-filter evidence, and no hosted CI was observed.
* Behavior: report .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-3.md. Full run, simulation, proxy (profile unresolved, models not observable), independent design/execution/grading, verdict Revise (9 Pass, 3 Revise; F1-F4). Findings corrected once in one batch after grading (patch post-grade-final-diff-readme.patch); NOT re-simulated; Revise stands and is flagged for the independent exact-head reviewer and owner. Sandbox retained; reports 1 and 2 and sandbox 2 untouched.
* Host validation of this wording-only change: no workflow, tool, manifest or Dockerfile change; the diff is limited to src/README.md and docs/reference/log.md plus tracking evidence.

### Deviations

* Plan P02-T02 intended a Pass-or-honest-verdict outcome; the honest verdict is Revise with unsimulated post-grade edits (PC-003 terminal-state rule). Recorded, not hidden.
* Hosted CI unobserved; nothing pushed.

Review: .copilot-tracking/reviews/logs/2026-11-08/issue-1294-validation-policy-correction-c2-review.md (execution Complete, outcome Residual work, RV-001 to RV-003).
