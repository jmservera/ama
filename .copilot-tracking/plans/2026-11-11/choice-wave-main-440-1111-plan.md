---
title: Resident-choice CSV feature-wave checkpoint plan (Refs #440)
description: One bounded observation and documentation checkpoint after PR 1435 (issue 1420) and the merged 1432 tests reach main; plan only until Root admits
ms.date: 2026-11-11
---

## Objective

After PR 1435 is actually merged and Root supplies the actual main, observe a small set of existing and newly merged focused selectors once on that pinned main, then append ONE dated section to `docs/architecture/cutover-evidence-pack.md` and an append-only entry to `docs/reference/log.md` (index pointer only if materially needed) with actual results, a continue, fix or proposed-pivot recommendation, affected gates and independent lanes. No source, fixture, schema, role, test, workflow or manifest edit. Not a Quality campaign, not a full gate, not acceptance, not a new issue. Delivers the "recurring checkpoint after a completed feature wave" criterion of #440 for this wave only; #440 stays open.

## Validation tier (basis recorded)

Focused tier: documentation-only change plus existing targeted local tests. No workflow, gate-tool, dependency-manifest, Dockerfile, infrastructure, SQL, deployment or security-control edit; the one `pip` step installs into a private venv under `/tmp`, not a manifest. Doubt resolves upward: a source failure, a gate-semantics finding or a privacy-minimisation finding is reported to Root as full-tier material, not fixed here. The documentation commit still needs independent exact-head review, human approval and applicable hosted CI, none claimed.

## Execution dependency and admission

Root must record, in an admission amendment committed before any test: PR 1435 actually merged (merge commit and method); the actual fresh `origin/main` SHA and tree; the `src` tree compared with candidate `87ea0ed8db9f180aec258eed42ca6232a7c97b6a`; any other movement since pin `1b169fe7d4f9b5a005123c8eb1825028ea431612`; hosted check status of the merged head, read live; and which optional selectors are admitted. Then an ordinary no-ff merge of that main into this topic, with no rebase, retarget or history rewrite. Planning is complete without this; implementation is not authorised.

## Phases

* [x] Phase 0, plan-only launch: research, readiness, plan, details, one independent critique, state, local commit. No test or probe ran.
* [ ] Phase 1, admission and integration (Root): amendment committed, main merged ordinarily, `git diff --name-only <main> HEAD` lists only `.copilot-tracking/` paths and `src`, `docs`, `infra`, `tools` and `.github` tree ids equal main's.
* [ ] Phase 2, preflight: cwd, branch, HEAD, tree, clean status; module origins under this worktree; Playwright import; `node`; pinned axe sha256; lock free and memory headroom; `ZF_DATA` unset and `~/.zava-forward` absent before.
* [ ] Phase 3, non-browser selectors C1 to C7 and I1 from the details table: one run each, raw exit, run, skip and failure counts compared with the static expectation.
* [ ] Phase 4, one browser story B1 under one nonqueued `flock`.
* [ ] Phase 5, record: ONE pack section and ONE log entry from raw logs; document-qualified trace; recommendation; process record. Link and diff review only.
* [ ] Phase 6, native review once, strict tracking, commit, handoff to Root. No push, PR, issue or board write.

## Stop rules

* Busy lock, missing Chromium, Playwright, Node, axe asset or venv: `blocked`, recorded raw, not pass; no queue, retry loop, kill or service install. One repeat after Root says the resource is free.
* Any failure: preserve the first raw failure, stop that surface, continue only independent admitted selectors, map to owners #1420, #80, #73 and #440, no new ticket, no source fix, no new test, no correction budget drawn. A failure in `test_resident_choice_export` or story 232 reproduces a PR 1435 area and goes back to Root, who owns the #1420 budget (four of five cycles remained on the reviewed head).
* A red, pending or absent hosted check on the merged head is a Root decision before any test; a failed or reopened review of 1435 also waits for Root.
* `timeout` exit 124, a Chromium crash or a lock wait is recorded raw as failed or blocked, never retried. If `tests.test_resident_choice_export` is absent on the admitted main, C1 is `not run`, not a failure, and the cause is recorded.
* A different `src` tree from `87ea0ed8`, or any `docs` movement beyond the pin, is recorded as main movement before the first test; it is not read as a merge defect.
* Unexpected skip in a browser selector, an executed count of zero, a count that differs from the static expectation without an explained source cause, or a module origin outside this worktree: not a pass; record the divergence.
* No test is rerun to improve a result; a rerun after a failure needs Root's direction.
* If the merged `src` tree differs from `87ea0ed8`, record the difference before the first test and say whether it is a main movement or a merge difference; Root decides whether to continue.
* The four inventory and QA cases are observed as the merged regressions they are; this plan makes no combined-journey acceptance claim for #132.

## Boundaries

* Local observed on constructed synthetic fixtures, owned temporary SQLite or JSON stores and loopback only. No SQL Server, Docker, cloud, model, provider, private or default dataset, new service, deployment or external message.
* No consent, Legal, identity, QA, privacy, retention, resident, production or accessibility acceptance is inferred. Whole #80, #73 and #440 stay open. Earlier adverse and process records stay unaltered; any correction is an additive dated note.
* Candidate observations in PR 1435 (127 focused, story 232 with 42 PASS lines, mypy, Ruff) are cited only as candidate history, never as main evidence.
