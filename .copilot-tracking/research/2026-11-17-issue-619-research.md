---
title: Issue 619 research - production AT, consent and Fluent/WCAG acceptance
ms.date: 2026-11-17
---

## Scope

Record what is automatable locally and prepare checklist docs for #619. No live
claims, desktop-only, demo-first. Disposition: executed (opening file; findings below).

## Starting evidence

* Protocol exists: docs/reference/research/ux/production-ux-acceptance-protocol.md (2026-11-02, updated 2026-11-03).
* Open human gates: every record row `Not run`.

## Measurements (2026-11-17, local, synthetic, Chromium via Playwright 1.64.1)

* `checks.production_config_a11y_browser_check` at base eb51af5c9 with pinned axe-core 4.10.3
  (sha256 880970c0...a68bb) reproduced: all assertions PASS (case view axe, tab keys, focus
  indicators, chat launcher/open/Escape). Command in the changes artifact.
* Gap found by reading the check: no 400 percent zoom equivalent (1280 px window at 400 percent is
  320 CSS px wide) or reflow assertion in the production configuration, and no reduced-motion check.
  Protocol Script A/B step 7 and 8 name these; only the 2026-11-03 text says "does not cover zoom to 400 percent".
* Not automatable: screen reader speech (NVDA/VoiceOver), real resident consent journey, owner O-1/O-3.
* Resident consent refusal is already covered on synthetic data by chat_widget_browser_check and
  test_resident_chat_api (per protocol); out of scope to duplicate.

## Planning Readiness

Ready. Disposition: executed. Smallest change: add a 320x256 reflow and reduced-motion step to the
production-config check, plus a pure-unit regression test of its helper; update protocol and README
records. FOCUSED tier (docs and a non-gate check tool; no workflow, SQL, security or deploy change).
