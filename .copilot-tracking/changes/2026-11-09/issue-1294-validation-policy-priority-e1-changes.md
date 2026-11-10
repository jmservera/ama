<!-- markdownlint-disable-file -->
# Changes: issue-1294-validation-policy-priority-e1

* Plan: .copilot-tracking/plans/2026-11-09/issue-1294-validation-policy-priority-e1-plan.md
* Details: .copilot-tracking/details/2026-11-09/issue-1294-validation-policy-priority-e1-phase-details.md
* Critique: .copilot-tracking/plans/critiques/2026-11-09/issue-1294-validation-policy-priority-e1-plan-critique.md (executed once, Revise, applied)
* Tier classification: focused. Basis: Markdown guides and instructions only; no permission, pinned action or image, package, secret, deployment path, security control or gate semantic changed by this work; main's tool change arrived by merge, not authored here. No blanket `--changed` run.

## Operations (in order)

* P01 research written (2026-11-09); plan and details written; critique executed; merge of origin/main b46a9ad9a committed (clean, no conflicts; tools unchanged versus main) with the research, plan and critique evidence.
* P02 edits: `src/README.md` (retained sensor MSSQL suite local-only bullet, SQL example row, verification date line, scoped-skips receipt-scope sentence); `.github/copilot-instructions.md` ("non-gate tooling"); coordinator agent (step 8 focused-candidate refresh, BASE RELAXED exception to the base-change rule, receipt-verification qualifier, hosted-checks-after-push); `.github/rubric/README.md` steps 1 and 3 selected tier; `docs/reference/research/delivery-bottleneck-analysis-2026-10-31.md` D4 supersession note; `docs/reference/log.md` appended entry.
* P03 independent static review of all targets (two passes), P04 behavior proxy simulation: `.copilot-tracking/hve-builder/2026-11-09-issue-1294-validation-policy-static-review-e1-log.md`, `.copilot-tracking/sandbox/2026-11-09-issue-1294-priority-e1/`.

## Divergences and amendments

* Critique PC-1 changed the order of final checks and Review to follow the commit. The behavior run graded the pre-commit working tree whose five policy files are the committed bytes of commit A except for later edits recorded below; static pass-2 fixes were applied BEFORE the behavior run, so the behavior run saw the post-fix tree.
* Static finding 1 (stack tip receipt) not accepted: pre-existing #470 design, not changed here.

## Preserved

* C1-C4 research, plans, critiques, details, changes, reviews, reports 1-5, sandboxes 2-5, static C4 log, the C4 lead review (Residual work) and earlier log entries are byte-unchanged. The independent C4 exact-head review (two High, three Medium, two Low) has no durable copy; only its issue-comment summary exists.

## Not run

* Full or `--changed` local gate (not applicable at this tier), browser, SQL, hosted CI (unobserved; unpublished).
