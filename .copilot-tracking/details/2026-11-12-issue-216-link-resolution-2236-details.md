---
title: Details for #216 citation and card link resolution regression
ms.date: 2026-11-12
---

## P01

* Test-only change in the existing API loopback class (`call` helper, cookies, `Fixture`).
* Scenarios: base; `self.f.source(2, text=long)` plus `self.f.card(pid="synthetic@v2#0001")`; conflict via `self.f.source(2, text=...)`.
* For each citation with a `link` (facts have none): GET link must be 200 and `id`, `version`, `hash`, `status` equal the citation; resolved text starts with the quote; sha256 of resolved text equals hash; `excerpt_truncated` equals `len(text) > 350`.
* For each card: GET `link` must be 200; the version named by the card id suffix exists; its `provisions` are all cited ids.
* Negative controls reuse the same helper: swapped provision link and a nonexistent card link must raise `AssertionError`.

## P02

* From `src/api`: `PYTHONPATH="$PWD/../core/tests:$PWD/../agents/tests:$PWD/tests" python -m unittest test_regulatory_chat_api -q` in a pip-installed venv; ruff on the file.

## Critique disposition (one independent critique, executed; verdict revise, all compatible findings applied directly)

* PC-001 applied: resolved card_id must equal the id before the final `@v`, version equals the suffix, plus a same-version wrong-card negative control.
* PC-002 applied: assert expected kind and exact citation and card counts per scenario (conflict emits two citations and no cards); compare citation text to `resolved_text[:350]`.
* PC-003 applied: limitation recorded; coverage is for the staff principal sam@example.test only.
