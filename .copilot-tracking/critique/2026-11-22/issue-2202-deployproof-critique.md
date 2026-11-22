---
title: Issue 2202 deploy proof critique
date: 2026-11-22
---

# Critique (executed once)

Verdict: approve with direct dispositions.

* Risk: restarting the AI suspension to obtain a generative answer would be an unauthorised control change. Disposition: do not lift it; report item 2 employee side as unmet with cause.
* Risk: resident AI cap (5 per hour) could make a fail look like a defect. Disposition: poll across the window and record each attempt's label; do not alter the ledger.
* Risk: regex counts double count repeated text. Disposition: use per-case parsing and the API totals; state parse limits.
* Risk: credentials in outputs. Disposition: every probe asserts the values are absent from the saved JSON.
* Scope: docs only; no src change; focused tier; no push.
