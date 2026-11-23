---
title: Critique for #2302 (third live run)
date: 2026-11-23
---

Executed once. Verdict: proceed with changes.

* Gating all costs on `price_source` text would break the existing zero-string test; gate on the server flag `price_source_configured === false` instead. Applied.
* A missing accepted-outcome count must also give Unknown for per-outcome costs. Applied.
* Keep the change to `app.js` plus one test; no backend change.
