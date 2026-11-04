<!-- markdownlint-disable-file -->
# Details: Resident demo UX redesign (Refs #462)

Authoritative content, copy, states and IDs are in the approved specification
([resident-demo-redesign-2026-11-04.md](../../../docs/reference/research/ux/resident-demo-redesign-2026-11-04.md)).
This file records only implementation choices.

## Phase 1

* `core/resident_showcase.py`: add `stage`, `documents` (requests, presented with labels), `summary` (label, text, sources) to `showcase_view`.
* `web/index.html`: icon-only Account summary (inline SVG, tooltip, `aria-label`/`title` "Account"); `#page-nav` landmark.
* `web/demo.js`: `icon()` helper (DOM-built SVG), hide `#signin` on submit with `aria-busy` loading and 4s slow copy, restore on error with email kept; ordered sections `sec-summary`..`sec-help`, then sensors and limits; stepper; documents; funding; summary AI opt-in via `/demo/assistant`.
* `web/demo.css`: nav, stepper, badges, tooltip, spinner with reduced motion, `scroll-margin-top`.
* Tests: `test_resident_demo_script.py` (Node fake DOM), `test_resident_demo_api.py` (key set), core tests for the view, `resident_account_check.py` name "Account".

## Phase 2

* Core: `sensors.stale`, `sensors.forecast` (points, reason, note) deterministic from stored history and an injected reference time.
* `demo.js`: forecast series, divider, forecast table rows, stale badge, `#sec-sensors` after help.
* `infra/sql/resident-showcase.sql`: single `stock_id` expression `COALESCE($.home.stock_id, $.synthetic_stock_anchor_id)`; adjust source tests.
* Docs: `api/README.md`, knowledge-base index, `log.md`.
