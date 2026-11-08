---
title: Issue 530 C1 chat checker lint and ignored-input hygiene review
ms.date: 2026-11-08
---

* Execution: authored Review once after implementation. Outcome: conformant for the bounded C1 LIGHT scope. Earlier records are retained, not regraded.

## Assessment

* The original gap Review called the candidate conformant for LIGHT scope while the planned chat-checker lint integration was unfulfilled and the ignored-input freeze had failed. That limitation is recorded here; the original text stands.
* C1 fulfils the lint integration: both contracts include the checker, the checker is lint and format clean under the gate profile, and a regression fails when either tuple omits it.
* The checker change is behaviour-preserving by AST proof, with the keyword-only `denied` binding verified against Playwright dispatch.
* Ignored inputs were relocated with a hash journal; no owner or unknown input was touched.

## Residual gaps

* No actual MSSQL or Chromium/axe execution; the lint proof is static and the checker has not been run in a browser after formatting.
* Hosted CI does not run the chat browser check (workflow edits out of scope).
* Future FULL 17-group gate (current Main, fresh images, `--jobs 1 --lock-timeout 0`, canonical lock free, external verified receipt, independent exact-head review, hosted CI) is not admitted.

## Still unmet

* Real employee sign-in, private-runner authority, model price and budget, real-model grounded answer and serving attestation, named bounded-agent confirmation, and screen-reader, voice-control, resident, legal and professional approvals. #530 stays open.
