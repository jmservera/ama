---
title: Resident chat document correction changes
description: Execution and validation evidence for task 520-documents-correction
ms.date: 2026-10-28
---

## Execution

Full approved plan in scope. Research Ready; one independent critique Revise
preserved with PC-001/002/003 directly disposed in the plan. P01/P02 implementation
starting; P03 Review/publication remains pending. No source changes before this
record. Existing source distributions were missing in system Python; restored
existing pinned dev dependencies in /tmp/ama-520-documents-venv (exit 0).

## Boundaries

No Azure, secrets, .env or private datasets. Only constructed fixtures and local
services. No acceptance/compliance inference, no upload capability or model prose.
Original first-pass evidence is untouched. No test removals or manifest changes.

## P01/P02 implementation and completion

New typed core resident_documents helper parses bounded request/document/issue
facts and renders per-request/document citations, provision instructions, all
recorded warnings/errors and distinct scan explanations without approval.
ShowcaseRow and fixed read-only SQL view/reader carry the projection. Strict
source-valid markers prevent SQL scalar coercion/truncation from laundering
invalid metadata. Private filenames, staff/scan detail and bytes stay unprojected.
Unknown and empty are distinct; generated placeholders do not satisfy presence.

The HTTP assistant reads the authorized row once for its answer and rechecks
authorization afterward. CaseProgress carries document facts through the existing
mandatory rules base and guidance-ID-only advisor. Typed document questions route
before generic status and allow provision explanations, not sending actions.
No web assets changed. API README records the source contract and separate
authorized view-application requirement.

## Validation evidence

* Focused core from src/core:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests
  /tmp/ama-520-documents-venv/bin/python -m unittest test_resident_documents
  test_resident_assistant test_resident_showcase test_resident_showcase_sql -q`:
  82 tests, OK, 22 opt-in SQL skips. These are not integration evidence.
* Focused API from src/api with `PYTHONPATH=tests:../core/tests:../agents/tests`:
  `python -m unittest test_resident_chat_api test_resident_assistant_api
  test_resident_aoai test_resident_demo_api -q`: 70 tests, OK, no skips.
  Includes exact rules/AI/failure facts and citation parity, typed questions,
  cross-case non-disclosure and revocation during inference.
* Real disposable loopback SQL, constructed cases only, shared heavy lock held
  nonblocking: 32 showcase SQL tests, OK, no skips. Source-through-view strictness,
  exact limits, own-case filtering, private-field exclusion and unchanged grants
  exercised. Owned container removed. First harness subprocess lacked source
  distributions; pinned external-venv interpreter fixed the harness. First actual
  SQL run exposed known-empty lists becoming null; explicit empty-array SQL result
  correction made the same regression pass. Original failures are not passes.
* `python -m checks.resident_assistant_browser_check --axe
  /tmp/ama-520-documents-browser/axe-4.10.3.min.js --out
  /tmp/ama-520-documents-browser-final`: exit 0. Real Chromium, pinned axe 4.10.3,
  missing/provision/warning/error text and citations, rules label, other-session
  unknowns, existing callback and auth flows, narrow/reduced-motion/200% text checks.
  Document citations scroll into the viewport at 320 CSS px/200% text with no panel
  horizontal overflow. Browser reports and screenshots retained externally.
  Human/AT/native browser zoom acceptance remains Not run.
* Targeted Ruff check/format at line length 100, core mypy (156 files), API mypy
  (94 files), git diff --check: pass after local formatting/type annotation fixes.

## Reconciliation and remaining work

P01/P02 markers and details now complete; 11 added methods, one new test file,
no test removals. No material divergence or new user decision. Original critique
is preserved, not repeated. Original independent Review is next.
P03 committed clean candidate, remote-topic rebase, nonblocking locked full gate,
receipt verification, independent exact-head assessment and normal push remain
pending. Pending publication evidence cannot be committed as a future pass.
Human/resident/content/AT, operational view application and real-model acceptance
remain separate; no whole-issue approval or closing keywords are justified.
