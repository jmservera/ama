---
title: Chat grounding and provenance review
ms.date: 2026-11-14
---

## Review

Execution: self-review once after implementation. Outcome: conformant for the focused tier.

* Chat still cannot approve, book, record consent or mutate records; refusal tests pass.
* Generative output is labelled only when `generative-grounded`; rule and fallback replies are
  labelled deterministic; unsupported figures stay withheld (core test).
* Labels are plain text, not colour only. No `aria-invalid` changes.

## Open items for later

* The live failure was not reproduced locally; confirm in the demo environment.
* Independent exact-head review, hosted CI and browser check remain required.
