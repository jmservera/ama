---
title: Visible-demo integration checkpoint 440 C1 phase details
ms.date: 2026-11-08
---

## Edits

* F1: replace the closing manual-path sentence with accurate rules-only and workflow-only wording; model call at most once per stored turn.
* F2: recommendation lists each issue's actual outstanding criterion (#229 WCAG, #159 screen reader and turn accounting, #891 per-call conjunction, #149/#157/#81 epic checkpoint and named-human gates) and limits the IoT dependency to sensor-grounded Quality.
* F3: narrow the sensor row to the `Assistants.capture` Quality allowlist and say live activation was neither observed nor verified here; keep the Excluded row consistent.
* F4: split the evidence row into local assessment and hosted exact-head checks.
* Provider: add real generic model answer observed once; no real case-grounded answer or human acceptance proven.

## Validation

`git diff --check`; ASCII; anchor; bytes before the new heading identical to `HEAD`; log prefix; `git fetch`; `git status --short`.
