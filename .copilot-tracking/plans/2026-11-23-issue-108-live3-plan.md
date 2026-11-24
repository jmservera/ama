---
title: Issue 108 live plan, third 2026-11-23 round
ms.date: 2026-11-23
---

Refs #108. Tier: focused. Changes: one research-data JSON correction and one test under `src/agents/tests`; no runtime source, permission, package or deployment change.

Critique (executed once): verdict accepted. Do not edit Bicep (live capacity 10 is a portal or CLI drift, not an approved infra change); record it as an observation. Keep `quota_headroom` unavailable and keep the existing gate test. Add a test that each recorded deployment's rate limits equal capacity (rpm) and capacity x 1000 (tpm), so a stale record fails.

Steps: correct `resident-mini` capacity and rate limits in the serving record with a dated `observed_on`; add the test; run `tests.test_ai_eval` and ruff; update the attestation note, index and log; write changes and review.
