---
title: Personal handoff HTTP guidance checkpoint plan (Refs #440 #153)
description: One bounded observation and documentation checkpoint after PR 1449 (issue 153 personal pending-handoff HTTP guidance) reaches main; plan only until Root admits
ms.date: 2026-11-11
---

## Objective

After PR 1449 is actually merged and Root supplies a pinned-main amendment, observe the smallest justified set of existing selectors once on the freshly resolved merged `origin/main`, then add ONE dated in-place section to `docs/architecture/cutover-evidence-pack.md` with actual results, a continue, fix or proposed-pivot recommendation, affected gates and independent lanes, plus an append-only `docs/reference/log.md` entry (an index pointer in `docs/reference/README.md` only if genuinely needed). No source, fixture, schema, role, policy, ADR, test or manifest edit. Not a Quality campaign, not a full gate, not acceptance, not a new issue, branch, PR, remote or board action. It delivers the "recurring checkpoint after a completed feature wave" criterion of #440 for this wave only. #440 stays open. No canonical addition is made in this planning phase.

## Validation tier (basis recorded)

Planning tier now: Markdown, link and diff review only; no runtime, gate or test. Later admitted observation: focused tier (owner decision D4, refined by #1294), because it is existing targeted local tests plus a documentation record, with no workflow, gate-tool, dependency-manifest, Dockerfile, infrastructure, SQL, deployment or security-control change. Doubt resolves upward: a source failure, gate-semantics finding or privacy finding is reported to Root as full-tier material and not fixed here. Independent exact-head review, human approval and applicable hosted CI remain required and are not claimed.

## Execution dependency and admission (exact resume condition)

Implementation is not authorised until BOTH hold: PR 1449 is actually merged into `main`, AND Root records a pinned-main amendment, committed before any test, giving:

* the merge commit, method, time and closing references (expected none, since #153 stays open);
* the actual freshly resolved `origin/main` commit and tree, and the per-directory trees `src`, `docs`, `infra`, `tools` and `.github`;
* the comparison of the merged `src` tree with the frozen candidate `2db08d8e2141d60a52d688b731f192972ca8293b` candidate `src` tree `bb7a461f0acc9ccff0cde8ddb16df3717c552c50` (the candidate root tree `e328d3eb18d69cc58293e2200eb9a0b51f377322` is expected to differ from main's root tree, because the candidate predates the PR 1448 documentation, and a root-tree difference is not a defect) and with base `ab44d42fa` (`src` `f6d487b51ce3314d732cab87a91844fe221a6e38`): equality of the merged runtime tree to the tested candidate is a separate statement from any command executed on main; any other main movement since the base is recorded before the first test and never read as a merge defect;
* hosted check status of the merged head, read live (absent, pending, skipped or unobserved is not success), and the independent exact-head review disposition;
* the admitted selector list (this plan's table or a named change) and the explicit authorisation of any optional item;
* confirmation that no other source touches `app.js` `pendingHandoffs` between the base and the pin.

Then an ordinary no-ff merge of that main into this topic, no rebase, retarget or history rewrite. Candidate observations (Root's raw 149 with 13 skips, 15 with zero skips, 16 with zero skips, and the 153 native counts) stay candidate history and are never relabelled as main execution.

## Smallest justified selection (resolved from existing tests, never guessed)

| Id | Selector | Static expectation | Lock ownership | Why it is in scope |
| --- | --- | --- | --- | --- |
| H1 | `tests.test_handoff_read_guidance` (`ZF_BROWSER_TESTS=1`) | 15 ran (8 Node, 7 Chromium), 0 skipped | OUTER non-queued shared heavy lock held around this module only | New surface: personal card 403, other HTTP, malformed and recovery states |
| H2 | `tests.test_unaccepted_handoff_download_ui` (browser) | 6 ran, 0 skipped | Internal non-blocking lock; NO outer lock | Adjacent personal-card CSV links must stay unchanged |
| H3 | `tests.test_handoff_waiting_view` (browser) | 10 ran, 0 skipped | Internal non-blocking lock; NO outer lock | The staff screen shares `Served`, `SAM` and `app.js`; waiting versus personal card |
| H4 | `tests.test_handoff_api` | 7 ran | none | Roles, refusal and projection of the read the card consumes |
| H5 | `tests.test_unaccepted_handoff_csv_api` | 13 ran | none | CSV projection of the same rows |
| H6 | `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 24 ran | none | Role matrix includes the touched routes |
| H7 (optional, off by default) | `tests.test_content_standard.CopyAudit` | 18 ran | none | The audit reads `app.js` and PR 1449 adds user-facing copy; runs only if Root explicitly admits it |
| S1 | `node --check` of `app.js`; Ruff check and `ruff format --check` of `tests/test_handoff_read_guidance.py` with repository configuration | exit 0 | none | Applicable static checks for the two changed files |

Prior counts 7 + 13 + 24 for H4 to H6 are re-derived on actual main. The default total is 75 tests (7 + 13 + 24 + 15 + 6 + 10); H7 adds 18 only if admitted. H1 to H3 are one browser group in this order, never concurrent; the plan does not add `test_accessibility_baseline` (no table or inventory change), `test_workbench`, `test_role_screens`, the 149-module set or any whole-gate run, and `CopyAudit` unless Root admits it, because no new concern justifies repeating them.

## Preflight (before the first test)

Record: cwd, branch, HEAD, tree, clean status; a controlled owned `HOME` (an `mktemp -d` that reaches the existing user-site Playwright and the existing Chromium cache by explicit paths, never by installing); `ZF_DATA` unset and `~/.zava-forward` absent before and after; explicit worktree imports with `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests` from `src/api`, and proof that `zava_forward.api.server`, `zava_forward.core.store` and `zava_forward.agents` module origins lie under THIS worktree (host editable installs point at another checkout); `import playwright`, `node` and `ruff` present with the interpreter that runs the tests (a missing tool is a pause before the first test, not an install); memory headroom; the shared lock holder state. No install, SQL, Docker, provider, cloud, private or default dataset, acceptance testing, service or full gate.

## Pause rule (explicit, no automatic recovery)

Any adverse result, unexpected skip, busy lock or tool failure PAUSES for Root, including a missing Playwright or Chromium, a nonzero exit, a count that differs from the re-derived expectation without an explained cause, a module origin outside this worktree, `timeout` exit 124 or a Chromium crash. On a pause the raw output is preserved and the affected surface is recorded as failed or blocked. There is NO automatic rerun and NO assertion repair, format fix, `PYTHONPATH` or environment repair and no source change; a rerun, if any, requires Root's explicit direction naming the command. This rule closes the retry recovery that earlier native runs took without a pause. No source-correction budget or additional diagnostic campaign is granted; unknown historical product-correction balances stay unknown.

## Phases

* [x] Phase 0, plan-only launch: research, readiness, plan, details, one independent critique, state, local commit. No test or probe ran.
* [ ] Phase 1, admission and integration (Root): pinned-main amendment committed; ordinary merge; `git diff --name-only <main> HEAD` lists only `.copilot-tracking/` paths and the five directory trees equal main's.
* [ ] Phase 2, preflight as above; first test only after it passes.
* [ ] Phase 3, H4 to H6 (and H7 only if admitted) without the browser variable, then H1 under the outer lock, then H2 and H3 with no outer lock, once each, raw exit, ran, skipped and failure counts compared with the expectation.
* [ ] Phase 4, S1 once.
* [ ] Phase 5, record: ONE pack section and the log entry from raw logs with the pin identities and the pack contract below; link and diff review only.
* [ ] Phase 6, original Review once, strict tracking, commit, handoff to Root. No push, PR, issue or board write.

## Pack section contract (planned, not written)

A dated in-place section after the last section, for example "Personal handoff HTTP guidance integrated-main checkpoint (2026-11-11, Refs #440 #153)", with `###` subsections:

* Trigger and pin provenance: trigger, merged PR identity and method, the freshly resolved merged `origin/main` commit and tree, per-directory trees, the separate statement whether the merged runtime tree equals tested candidate `2db08d8e2`, previous checkpoint link (PR 1448 waiting checkpoint), live issue and PR states, hosted checks read or not read, source and document blob identities (`app.js`, `test_handoff_read_guidance.py`, the other selector files, BRD, PRD, ADRs 0003, 0006, 0007, re-read at the pin).
* Opening statement adapted from the previous section: draft, not approved, local observed on constructed synthetic fixtures only, no acceptance, runs only listed existing tests, changes no source, configuration, test, workflow or requirement.
* Requirement-qualified traceability limited to the affected card, waiting, API, CSV and residual-backlog paths: document-qualified rows only, with classes `local observed`, `implemented but unverified`, `deferred`, `blocked`, `unknown` (Azure observed stays empty). BRD stays draft, PRD in-review, ADR 0007 Proposed; named-human wording review, OD-09, operational and assistive-technology acceptance, reflow and zoom, large-queue performance, remaining AC-120 columns, and whole #83, #81, #153 and #440 gaps stay open; no whole acceptance or approval is invented.
* Actual commands, environment and results: a raw table; the first raw failure preserved; the skip count stated; the Browser 403 and 500 labelled constructed route responses, not backend permission status or live acceptance.
* Exclusions and residuals; process record (candidate native retries, the waiting checkpoint history, fresh Root verification authorised separately); recommendation (proposed for Root, not a decision) with affected gates and an exact resume point.

Log entry follows the existing append-only pattern. Check Markdown style (ASCII, `*` lists, no em dashes, no bold-prefix lists), relative links, `git diff --check`, and that `git diff --name-only <main>` lists only the pack, the log, an index row if needed and tracking files.

## Stop rules and boundaries

* Local observed on constructed synthetic fixtures, owned temporary stores and loopback only. No API, store, permission, architecture, ADR, requirement, product or test edit; draft and proposed documents stay so; no approval, acceptance or consent is inferred; earlier adverse and process records stay unaltered (any correction is an additive dated note).
* A red, pending or absent hosted check on the merged head, or a reopened review, waits for Root before any test.
* Do not claim #153 slice C2, C3 (universal) or C5, #83 criterion 3, #81 or #440 closure merely because child PRs merge. No issue, PR, branch, remote or board action by this work.
* Canonical pack file, issue comments, ticks, board and publication are untouched until Root admits implementation.
