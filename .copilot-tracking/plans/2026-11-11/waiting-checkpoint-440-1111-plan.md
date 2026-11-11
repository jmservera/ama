---
title: Handoff waiting screen feature-wave checkpoint plan (Refs #440 #83)
description: One bounded observation and documentation checkpoint after PR 1444 (issue 83 staff handoff waiting screen) reaches main; plan only until Root admits
ms.date: 2026-11-11
---

## Objective

After PR 1444 is actually merged and Root supplies the actual fresh `origin/main` and matching tested feature tree, observe a small set of existing focused selectors once on that pinned main, then add ONE dated in-place section to `docs/architecture/cutover-evidence-pack.md` with actual results, a continue, fix or proposed-pivot recommendation, affected gates and independent lanes. Add an append-only entry to `docs/reference/log.md` and an index pointer in `docs/reference/README.md` only if required. No source, fixture, schema, role, test, workflow or manifest edit. Not a Quality campaign, not a full gate, not acceptance, not a new issue. It delivers the "recurring checkpoint after a completed feature wave" criterion of #440 for this wave only. #440 stays open.

## Validation tier (basis recorded)

Focused tier (owner decision D4, refined by #1294): documentation-only change plus existing targeted local tests. No workflow, gate-tool, dependency-manifest, Dockerfile, infrastructure, SQL, deployment or security-control edit; the one `pip` step installs into a private venv under `/tmp`, not a manifest. Doubt resolves upward: a source failure, a gate-semantics finding or a privacy finding is reported to Root as full-tier material and not fixed here. The documentation commit still needs independent exact-head review, human approval and applicable hosted CI, none claimed here.

## Execution dependency and admission

Planning is complete without it; implementation is not authorised until Root records, in an admission amendment committed before any test:

* PR 1444 actually merged (merge commit, method, time) and its closing references (expected none);
* the actual fresh `origin/main` SHA and tree; the `src` tree compared with candidate `441fd7ed` `src` tree `f82975dfc345f1a3705d62e08819383f6dd7bfd5` and the base `src` tree `b78627c004af2117469b1aac5a30e538395145af`; any other main movement since `7880b95b` (any `src` or `docs` movement beyond PR 1444 is recorded before the first test, never read as a merge defect);
* hosted check status of the merged head, read live, including the earlier failed API job and its re-run outcome (an absent, skipped or unobserved hosted check is not success);
* the independent exact-head review disposition of the merged 1444 head;
* Root's exact "81 affected tests" command list and which optional selectors (W9) are admitted;
* confirmation that issue 153's candidate `99f01d7` is not merged, or, if it is, an explicit statement that main moved and where.

Then an ordinary no-ff merge of that main into this topic, with no rebase, retarget or history rewrite. Prospective candidate `441fd7ed` is never treated as main. The pre-merge PR 1444 observations (69 at `dd3c3291`; the Root-reported 81 at `441fd7ed` with Chromium, no skips, JS, Ruff and mypy clean; hosted API 2850 tests, 603 skips, one failure 13 versus 12) are candidate history only.

## Phases

* [x] Phase 0, plan-only launch: research, readiness, plan, details, one independent critique, state, local commit. No test or probe ran.
* [ ] Phase 1, admission and integration (Root): amendment committed, main merged ordinarily; `git diff --name-only <main> HEAD` lists only `.copilot-tracking/` paths; `src`, `docs`, `infra`, `tools` and `.github` tree ids equal main's.
* [ ] Phase 2, preflight: cwd, branch, HEAD, tree, clean status; private venv; module origins under this worktree; Playwright and `node` present; pinned axe not needed (no axe selector); lock free and memory headroom; `ZF_DATA` unset, `~/.zava-forward` absent before and after.
* [ ] Phase 3, selectors one at a time, one run each, raw exit, ran, skipped and failure counts compared with the static expectation: W4 to W9 first without the browser variable, then W1, W2 and W3 with `ZF_BROWSER_TESTS=1` and no outer `flock` (the W1 and W3 browser classes take the heavy lock themselves without queueing and skip when it is busy, so an outer lock would force a skip; the W2 browser class takes no lock, so the preflight lock-free and memory check must pass before W2 and it never runs concurrently with W1 or W3).
* [ ] Phase 4, optional compact static checks: `node --check` of `app.js` and Ruff check and format check of the new test only, if Root admits them (they repeat Root's candidate checks on main).
* [ ] Phase 5, record: ONE pack section and the log entry from raw logs; document-qualified trace; recommendation; process record. Link and diff review only.
* [ ] Phase 6, native review once, strict tracking, commit, handoff to Root. No push, PR, issue or board write.

## Pack section contract (planned, not written)

Heading, dated in place after the last section, for example "Handoff waiting screen integrated-main checkpoint (2026-11-11, Refs #440 #83)". Required subsections:

* Trigger and pin provenance: trigger, merged PR identity and method, main SHA and tree, per-directory trees, `src` tree comparison with candidate `441fd7ed`, previous checkpoint link (PR 1440 at `b7d66e42`, ADR 0007 decision record `541e0f72` still Proposed), live issue and PR states, hosted checks read or not read, candidate history labelled UNMERGED and EXCLUDED.
* Opening statement adapted from the previous section: draft, not approved, local observed on constructed synthetic fixtures only, no acceptance, runs only the listed existing tests and changes no source, configuration, test, workflow or requirement. The five headings in this list are used as `###` subsections; the template's identities, evidence-class and process-record tables fold into them.
* Requirement-qualified traceability: the document-qualified rows of the research (PRD FR-011/AC-014/AC-036, FR-066/AC-120, FR-004; BRD FR-018/AC-024, BG-010, OD-09, NFR-009/AC-071; ADR 0003, 0006, 0007 status), the cross-feature contract (staff `#/handoff-waiting` versus personal card; guarded route and projection; valid zero versus unavailable, malformed, 403 and abort navigation; manual case links and recheck; existing CSV and JSON), with the classes `local observed`, `implemented but unverified`, `deferred`, `blocked`, `unknown` (Azure observed stays empty), the actual synthetic journey evidence and residual owners. The #83 BRD source-reference drift is recorded as a finding for #83, not corrected.
* Actual commands, environment and results: a raw command table with exit, ran, skipped and failure counts and each limit; the first raw failure preserved; the browser skip count stated.
* Exclusions and residuals: OD-09 times, operational acceptance, manual assistive-technology test, reflow and zoom, large-queue performance, urgency and next-update columns of AC-120, Azure, identity, human and resident acceptance, whole #83, #81 and #440; unmerged 441f and the 153 candidate `99f01d7`.
* Recommendation (proposed for Root, not a decision): continue, fix or proposed pivot; affected gates; independent lanes that continue (#153 only after Root's own admission, not by this record); exact resume point.

Use the existing log pattern for the log entry. Check Markdown style (ASCII, `*` lists, no em dashes, no bold-prefix lists), relative links, `git diff --check` and that `git diff --name-only <main>` lists only the pack, the log, an index row if needed and tracking files.

## Stop rules

* Busy lock, missing Chromium, Playwright, Node or venv: `blocked`, recorded raw, not a pass; no queue, retry loop, kill or service install. One repeat after Root says the resource is free.
* Any failure: preserve the first raw failure, stop that surface, continue only independent admitted selectors, map to owners #83, #81, #153, #440 as relevant, no new ticket, no source fix, no new test, no correction budget drawn. Unknown historical product-correction balances stay unknown; no new batch is granted. A failure in W1, W2 or W7 reproduces a PR 1444 area and returns to Root.
* A non-zero skip in W1 to W3 means browser cases did not run for that module: record not a pass for browser evidence, do not rerun to improve it. `timeout` exit 124 or a Chromium crash is recorded raw as failed or blocked.
* If the merged `src` tree differs from the candidate `src` tree, record the difference before the first test and say whether it is a main movement or a merge difference; Root decides whether to continue.
* A red, pending or absent hosted check on the merged head, or a reopened review, waits for Root before any test.
* An executed count of zero, a count differing from the static expectation without an explained cause, or a module origin outside this worktree is not a pass.
* No test is rerun to improve a result; a rerun after a failure needs Root's direction.
* Do not claim Root #83 criterion 3, whole #81 or whole #440 closure merely because all child PRs merge.

## Boundaries

* Local observed on constructed synthetic fixtures, owned temporary stores and loopback only. No SQL Server, Docker, cloud, scanner, model, provider, private or default dataset, new service, deployment or external message, and no full gate.
* No API, store, permission, architecture, ADR or requirement change. Draft or proposed documents stay draft or proposed; ADR 0007 stays Proposed. No approval, acceptance or consent is inferred. Earlier adverse and process records stay unaltered; any correction is an additive dated note.
* Canonical pack file, issue comments, ticks, board and publication are untouched until Root admits implementation.
