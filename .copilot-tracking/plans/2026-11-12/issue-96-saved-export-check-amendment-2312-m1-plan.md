---
title: Issue 96 saved export check M1 correction 2 plan
description: Prospective plan, written before independent critique and before any source change, to remove the broad TypeError fallback from the saved export check route
ms.date: 2026-11-12
---

## Status and honesty record

This is correction 2 of the initial `issue-96-saved-export-check-2236` task, authorized by the coordinator for finding M1 only. Correction 1 (`ad37cb113`) is spent. No new budget pool and no scope or expired-grant renewal. The original self-review ordering defect (implementation `bbe80e563` before its plan, critique and review in `05fa255dc`), the author-only original critique and Review, amendment 2255 and the independent assessment `Revise` verdict (M1 Medium; L1 to L4) are preserved unchanged and not relabelled. The independent critique of this plan and the final Review run in separate agent contexts. Plan written at head `7f3386ddd`.

## Finding M1

The route catches every `TypeError` from `export_freshness` and retries with `{}`. A genuine internal `TypeError` (assessor probe: `draft_export` patched to raise) therefore answers 200 `Invalid` with a user-blaming "edited after export" reason, is not logged and never reaches the shared 503 path. The real forged-copy `TypeError` comes from `sorted(set(saved_rows) - set(stale))` when a digest-consistent copy mixes `str` and non-`str` field ids.

## Decision

Core stays frozen. Delete the `try/except TypeError`. Add one narrow route-level guard that runs before the core call and after the case, draft, role and switch checks (so precedence is unchanged): when the copy's `fields` is a list and any row is not an object with a string `field_id`, pass `{}` to `export_freshness`. The core already answers an unusable copy with the existing `Invalid` result, so the user message is unchanged and nothing is invented. A `TypeError` raised anywhere else propagates to the shared `_forms` handler: logged error and controlled 503 `Form storage failed`.

## Tests (failing first)

* New: with a valid saved copy, `form_export.draft_export` patched to raise `TypeError`, the check answers 503, logs at ERROR, never reports `Invalid`, and leaves state unchanged. Fails on `7f3386ddd` (returns 200 `Invalid`).
* Existing malformed-copy control (mixed `str` and `int` ids) stays and must pass with the guard.
* One added control: all-integer field ids (sortable, so the core alone would not report `Invalid`) answer `Invalid`.
* No general L1 test expansion.

## README

Replace the fallback description: malformed field ids are `Invalid`; an internal fault answers the shared 503.

## L3 qualification, same amendment

* Tick Phase 4 of the amendment 2255 plan with an annotation pointing at its recorded independent Review (tracking edit only, no Review text change).
* Install ruff 0.17.1 and mypy 2.4.0 with pip into an isolated venv under the session files folder (no uv, no source-package `PYTHONPATH`, `python -s`) and record actual results on the final tree, including the baseline.

## Phases

* [x] Phase 1: independent critique in a separate context: Revise, CR-1 and CR-2 accepted (see critique record); malformed copies are Invalid before case and draft binding, disclosed; the 503 claim is limited to faults escaping the frozen core.
* [x] Phase 2: failing-first test, then route fix, README and focused verification.
* [x] Phase 3: ruff, mypy, format and focused tests on the final tree; commit with the privacy-safe identity.
* [ ] Phase 4: independent final Review in a separate context of the local frozen head; record outcome without repeating Review.

## Boundaries

No push, PR, merge, issue, tick or approval. UI still waits. No private data, cloud, provider, production, spend or shared cleanup. C1, C5 and C6 remain unproven. Generated output stays under the session files folder.
