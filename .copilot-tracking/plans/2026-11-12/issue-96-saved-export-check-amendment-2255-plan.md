---
title: Issue 96 saved export check prospective amendment and adoption plan
description: Prospective plan, written before independent critique, to adopt or correct the existing saved-export freshness check candidate
ms.date: 2026-11-12
---

## Status and honesty record

The original plan, critique and review of `issue-96-saved-export-check-2236` stay unchanged. Their critique and Review were author self-reviews, not independent, and are recorded as such in commit `05fa255dc`. They are not relabelled. This amendment plan is written at head `05fa255dc` before any new change. Its critique and the final Review are run by separate agent contexts, not by the author. The existing implementation (`bbe80e563`) is prior candidate evidence, not proof of prospective independent critique. This is one correction of the initial saved-check task, with no new budget pool.

## Objective

Decide, under independent critique, whether to adopt the candidate unchanged or correct it. Scope is unchanged: default-OFF synthetic-demo, read-only served freshness endpoint `POST /api/cases/{case_id}/form-review/{draft_id}/held-export/freshness`; no reviewed or approved state; no UI source; no core change; Refs #96 only.

## Facts already established (for the critic to verify)

* `do_POST` rejects any non-object body with 400 `Could not read that.` before routing, so the `isinstance(body, dict)` clause in the new branch is defence in depth, not a separate behaviour. Verified by the shared parser; the critic should confirm.
* The saved export digest `content_sha256` is tamper evidence for accidental edits. It is not a signature and does not authenticate provenance: a client can fabricate a self-consistent copy. The endpoint must therefore only return what the signed-in actor could already see about the current working review, and must never trust saved values.
* Administrator `view_only` accounts get 403 on every POST, including this read-only comparison. This is existing global behaviour.
* `export_freshness` binds the case through `draft_export(store, user, case_id, saved draft_id)`; a draft belonging to another case yields `Unavailable`, not a leak.

## Candidate decisions to test

* D1 Adopt the route, guard (same `held_download_enabled`, never trusted-proxy), 400 on draft id mismatch, 200 for Current, Stale, Invalid and Unavailable results, `Cache-Control: private, no-store`.
* D2 Body semantics: the redundant non-object clause may stay or be simplified; saved copy is untrusted input; oversized, malformed or empty bodies are refused by the shared parser and need no new code.
* D3 Auth semantics: unauthenticated 401, trusted-proxy CSRF header, view_only 403, role projection, and `forms._actor` per request. Decide which of these need a direct test on the new route.
* D4 Case and draft semantics: path case versus saved export draft; a saved copy for a draft in another case, a deleted draft, and a mismatched draft id must not disclose information or write state.
* D5 Provenance semantics: the response is a comparison, `reviewed: false`, no field values, no approval, no eligibility, no proof of C1, C5 or C6; text must not call the saved copy authenticated.
* D6 Possible corrections: add tests for malformed JSON, oversized body, unauthenticated, CSRF, view_only, cross-case draft, and a forged self-consistent copy; tighten README wording on digest versus provenance. A correction is made only if the critique finds a gap that the existing tests do not cover.

## Phases

* [x] Phase 1: independent critique of this plan in a separate agent context; record verdict and dispositions.
* [x] Phase 2: adopt unchanged or apply critique-approved corrections limited to `src/api/tests/test_form_held_download_api.py`, `src/api/src/zava_forward/api/server.py` and `src/api/README.md`.
* [x] Phase 3: focused verification with the owned pip venv (`files/venv-96-refill-2236`), no uv, no full gate.
* [x] Phase 4: independent final Review in a separate agent context of the exact head; record outcome and routed findings without repeating Review. Executed and recorded in commit `7f3386ddd` (marker ticked 2026-11-12 under the M1 correction 2 plan, assessment finding L3; the Review text is unchanged and its RV-A1 grade is superseded by the independent assessment M1).

## Validation (owner demo focused tier)

Core `test_form_export`, `test_form_dependencies`; API `test_form_held_download_api`, `test_form_staging_api`, `test_role_endpoint_inventory`; ruff and mypy on changed Python; `git diff --check`; README link and diff review. Not run: SQL Server, browser, hosted CI, full gate, axe, cloud or model calls.

## Boundaries

No push, PR, merge, issue creation, acceptance tick, human approval or shared cleanup. Coordinator publication is separate. Exhausted authority is not renewed.
