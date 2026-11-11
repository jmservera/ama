---
title: Resident-choice CSV feature-wave checkpoint research (Refs #440)
description: Read-only prospective research for the next bounded integrated-main checkpoint after PR 1435 (issue 1420) reaches main; plan-only launch
ms.date: 2026-11-11
---

## Status and disposition

* Research disposition: `executed` (read-only git, source, diff and GitHub queries). Planning Readiness: `Ready` for a plan-only freeze. Nothing here is an observed result: no test, browser, install, Ruff, mypy, push, PR, issue or board write ran, and no source, fixture, schema or role file changed.
* Prospective: the planned work consumes PR 1435 only after it is actually merged. The PR diff was read as candidate-policy and source evidence only. It is not pinned main and is never described as observed on main.
* Reused, not re-derived: the closure-wave research, plan, details, critique and pack section of 2026-11-11 (`closure-wave-main-440-1111-*`, pack section "Closure-wave integrated-main checkpoint"), and the inventory and staff intake checkpoint. Their method (private venv, once-each selectors, raw outputs outside the repository, document-qualified trace, additive pack section) is valid and reused. Their observed results stay historical.

## Identities read (2026-11-11)

| Item | Identity |
| --- | --- |
| Pinned main (planning base) | `1b169fe7d4f9b5a005123c8eb1825028ea431612`, tree `a80e8fcce38ec95f8dd77126c20ae8561a19ce7a`; `src` `6a9c5ec36fdcf2ca56eec9c21588fe0ae830c27b`, `docs` `9a33d2472abf34966bc8090c57b8b281461caed5`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `.github` `8ee2281991f0a0bbabac6a46806f45ef211ea87d`. `git fetch` showed `origin/main` still equal to this pin at research time |
| Topic branch | `docs/demo-choice-wave-checkpoint-440-1111`, created at the pin, clean at start |
| Main log since the last pack record | `1b169fe7d` rubric score, `064f42f83` PR 1432 (inventory-held QA tests), `a853cce16` PR 1433 (the last closure-wave pack record), `e0dec207d` rubric |
| Dependency PR 1435 | OPEN, base `main`, MERGEABLE, no closing references, head `1febb4b0b143937f6854075e5acf119031f1fd74`. Hosted checks read as mixed: eight completed SUCCESS, `src-api`, `src-core`, `src-namespace`, `mssql` and `detection` in progress, `rubric/score` pending. Pending is not success and no hosted result is claimed |
| PR 1435 source | `src` tree `87ea0ed8db9f180aec258eed42ca6232a7c97b6a`, source-equivalent to tested implementation `07041ce04c11a4d88c0fd5123704c5736390e8d8` (C1 correction; four of five correction cycles remain). The same pinned base `1b169fe7d` |
| Independent review of the candidate | Functional Pass (zero findings) on `07041`, same-head confirmation on `1febb4b`. The earlier High finding (an unrecognised review status downloaded as "None recorded") was reproduced by execution, corrected in C1, and its original report is retained as historical. Both reports state their own limits (no reviewer test run; reliance on Root's source-equivalence evidence) |
| Issue states (read live) | #1420 OPEN; #1432 MERGED (PR state); #80, #73, #440 OPEN. Nothing is ticked, closed or opened here |

## What PR 1435 changes (candidate, from the published diff)

Four source files and four tests plus tracking records; `src/api` only. No Core, schema, role, registry, shared serializer, sidebar or per-home change.

| File (in the candidate) | Change | Why it matters to a post-merge checkpoint |
| --- | --- | --- |
| `src/api/src/zava_forward/api/resident_choice_export.py` (new) | Eight-column serializer of the current portfolio page; closed display allowlist of the five `quality.CHECKLISTS` keys; unrecognised names become `Measure name withheld`; review status limited to `Needs human review` and `Reviewed with supplied acceptance`, anything else is `Unknown (evidence unavailable)`; no free text or nested private fields | Contract and privacy-minimisation surface; the C1 High finding lived here |
| `src/api/src/zava_forward/api/server.py` | `get_kind` and `do_GET` dispatch for `GET /api/resident/choice-queue.csv`, attachment `resident-choice-queue-page.csv`; reuses the JSON queue's four roles and query parsing; JSON errors without a CSV attachment | Shared dispatch surface; role and error boundaries |
| `src/api/src/zava_forward/api/web/role-screens.js` | Plain attachment anchor beside a loaded overview, current-page note, no link in blocked or failed state | UI and copy surface |
| `src/api/tests/test_resident_choice_export.py` (new) | `Serializer` and `Http` classes; 30 test methods (27 original plus 3 C1 regressions) | Primary selector |
| `src/api/tests/test_resident_choice_screen.py` | One added link test (`test_download_follows_the_loaded_page_and_never_a_bad_or_failed_one`) beside 8 existing | UI selector |
| `src/api/tests/test_role_endpoint_inventory.py` | One endpoint-inventory entry for the new route | Role matrix selector |
| `src/api/checks/role_screens_browser_check.py` | Story 232 gains attachment and link checks | Browser selector |
| `src/api/README.md` | One paragraph | Documentation |

Candidate-only observations (author evidence, independently read, not rerun by a reviewer, and not on main): 127 focused tests OK, the four merged intake tests OK, one real Chromium 156 story 232 run (42 PASS lines, axe 4.10.3, zero violations, empty incomplete list), pinned mypy and Ruff clean for changed code. These establish the candidate's state before merge. They are not the future main observation.

## Existing selectors derived from source (pin `1b169fe7d`, plus the candidate diff where marked)

Static counts were derived by reading class bodies (AST count of `test*` methods) and the diff, and are expectations to compare with actual runs, not marks to force.

| Id | Selector (existing) | Static expectation | Source basis | Affected-surface reason |
| --- | --- | --- | --- | --- |
| C1 | `src/api`: `tests.test_resident_choice_export` (classes `Serializer`, `Http`) | 30 | Candidate diff (new module); `Http` has 13 and `Serializer` 17 | New serializer and HTTP route |
| C2 | `src/api`: `tests.test_resident_choice_screen.ResidentChoiceScreen` | 9 (8 on pin plus 1 in the candidate) | Pin file and candidate diff | New link and failure-state behaviour, Node vm DOM double, no browser |
| C3 | `src/api`: `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 24 (14 own plus 10 inherited from `Matrix`; prior critique PC-001) | Prior critique; the candidate adds a table entry, not a method | Four-role access and signed-out refusal for the new route |
| C4 | `src/api`: `tests.test_list_export_api.ListExportApi` | 11 (prior record) | Prior pack record | Shared `get_kind` dispatch changed; guards the shared list-export registry |
| C5 | `src/api`: `tests.test_role_screens_conformance.RoleScreenConformance` | 11 | Pin file; `resident-choice` screen block is scanned | `role-screens.js` changed |
| C6 | `src/api`: `tests.test_content_standard.CopyAudit` | 18 (prior record) | Prior pack record | Plain-language audit of the changed UI copy |
| C7 | `src/core`: `tests.test_resident_choice_queue.ResidentChoiceQueue` | 4 | Pin file | The unchanged JSON queue projection that the CSV serializes; guards the page and order semantics the CSV copies |
| I1 | `src/api`: `tests.test_staff_intake_api.StaffIntakeApi.test_inventory_hold_after_capture_is_not_cleared_by_acknowledgement_or_qa` and `...test_inventory_hold_after_acceptance_refuses_handover_and_a_later_capture_stays_held`, and the same two names on `JsonStaffIntakeApi` | 4 (2 names times 2 store classes) | PR 1432 diff (`064f42f83`, +53 lines, two methods in the base class; `JsonStaffIntakeApi` subclasses it) | The four inventory and QA regressions merged in 1432. They are independent of the CSV; the combined gap was previously unverified. `MssqlStaffIntakeApi` is not selected |
| B1 | `src/api`: `python3 -m checks.role_screens_browser_check 232` with `ZF_AXE_JS` set to the pinned axe | exit 0; the candidate run printed 42 PASS lines, recorded as the candidate's output, not a required count | Checker `run_browser` story `232` block and `STORY_ACCESSIBLE`, `STORY_RESIDENT`; the harness has no self-lock | One bounded real browser story on the integrated main: resident-choice screen, download link beside the loaded overview, attachment check, axe |

Why this is small and affected-surface only: C1 to C6 cover the changed files. C7 covers the projection the export copies. I1 is the explicitly requested merged inventory set. B1 is the one real-browser story for the changed screen. Not selected, with reasons:

* The 209 prior cases, whole Capacity, `capacity_browser_check`, whole importer, full gate, SQL Server, Docker: PR 1435 touches none of Capacity, importer, store or SQL; no concrete affected-surface reason.
* `test_case_journey`, `test_task_queue_api`, `test_resident_service_screen` and story `232s`: they run other queues or screens that the diff does not change. The candidate's 127-case set included `test_case_journey`; it is omitted here as a deliberate, recorded scope choice, reversible by Root.
* Real model, provider, cloud, deployment, actual or private data, default dataset: out of scope by the owner's demo policy.

## Source-qualified requirement, architecture and contract links

Revisions and status read at the pin (unchanged since the last pack section):

* BRD `BRD-2026-AMA48-001`, `docs/brds/agentic-retrofit-programme-brd.md`, v0.21.0, status `draft`, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`.
* PRD `PRD-2026-AMA48-001`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, v0.21.0, status `in-review` (`author-complete-unsigned-pending-review-and-owner-acceptance`), blob `c788b917bafaede215f326f0efc71e071a687f1c`. In this note "PRD" always means this file.
* A second document, `docs/prds/proper-warm-retrofit-programme-demonstrator.md` (same `prd_id`, v0.13.0, `in-review`, `candidate-pending-review-and-owner-acceptance`, blob `f7f9b7675e60e49006127a374e1106ff18aae282`), reuses FR and AC numbers with different meanings. It is not cited here, so the path, not the `prd_id`, is the qualifier.
* ADR 0001 Proposed (`d42fa5c46`), ADR 0006 Accepted 2026-10-15 (`956da1a3b`), ADR 0007 Proposed (`abb21088a`). Only ADR 0006 is approved. Drafts are not approved by this plan.

Candidate trace anchors. Identifiers collide across documents (for example BRD AC-018 and PRD AC-018 are different), so every one is document-qualified. Issue 1420 itself cites none of these identifiers; they are proposed trace links of this plan, for human confirmation:

| Anchor | Statement summary | Relation to the CSV and its limits |
| --- | --- | --- |
| PRD FR-046, AC-037, AC-056 | Apply a supplied resident pause or withdrawal only to its identified measure; other choices unchanged; no refusal or sanction inferred | The CSV shows paused, withdrawn and retained human review per measure; it is a read-only copy of existing state, not a decision. Constructed fixtures only |
| BRD FR-013 and FR-014 (BRD ids) | Residents agree, decline, defer or withdraw per measure; disputed or withdrawn consent or a requested pause holds affected non-urgent activity | Display of recorded state only. Consent, readiness and approval are never inferred; unknown stays unknown |
| PRD FR-048, AC-065 | Offered versus confirmed commitment; named update owner | Weak, partial link for human confirmation: the CSV carries only a bounded update commitment status, no owner or detail, so it cannot show the named update owner these requirements ask for. The trace class stays at most local observed (partial) |
| ADR 0006 (Accepted) | `src/` layout and cut-over | Route and tests sit in the existing `src/api` project |

Classes at the end of a future observation would be, at most, local observed (partial) on constructed synthetic fixtures, owned temporary stores and loopback. Azure observed stays empty. MSSQL variants, deployed behaviour, actual-record export, retention, privacy review, resident acceptance and assistive-technology behaviour stay implemented but unverified or unknown. This checkpoint is not a domain acceptance authority and not a legal audit.

## Execution dependency (not a research blocker)

Implementation of the observation needs, in order: Root consumes this plan; PR 1435 is actually merged by its owner; Root supplies the actual merge commit and fresh `origin/main`; ordinary integration of that main into this topic (no rebase, retarget, history rewrite or guessed future merge); then new focused observations on that pinned main. If main moves for other reasons first, Root names the pin. If PR 1435 merges by squash or merge commit, the new `src` tree must be compared with the candidate `87ea0ed8` and any difference recorded before reading any result as the same code. If a hosted check on 1435 fails, or review reopens it, the plan waits.

## Boundaries retained

* Whole #80, #73 and #440, production, privacy and retention, human review, resident consent and assistive-technology acceptance remain open and separate. Axe results, fixtures and loopback runs do not infer WCAG conformance.
* No actual-record export, privacy, retention, resident or production approval is implied (the 1420 admission says so itself).
* Reused versus new: reused the method and the earlier cases; new are C1, the C2 link test, the C3 entry and B1's download checks, which have only candidate-side evidence today.

## Planning hazards found

* The candidate used two shell wrappers that failed before any test ran (wrong module paths; missing Playwright in a private venv; a private `HOME` hiding the user-site install). The details plan therefore preflights module origins and Playwright before the heavy lock.
* The browser story checker has no self-lock; one nonqueued `flock -n -E 99` is needed (exit 99 without a story line is a busy lock, recorded blocked).
* The observed Chromium build depends on the installed Playwright; a missing browser is blocked, not installed here without Root's say.
* The count of 30 for C1 matches the PR body (27 plus 3) and the AST count of the candidate diff. Counts for C4 and C6 are carried from the prior pack record and must be re-read at the actual main.
