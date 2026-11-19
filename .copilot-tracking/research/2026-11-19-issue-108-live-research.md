---
title: Issue 108 live research 2026-11-19
---
Scope: synthetic demo, desktop only. Unticked criteria: model/version/quota in region; held-out freeze with independent labels; human detection; effort/cost comparison; hashes/denominators/serving version; actual-call authorization; real AI/SQL/Azure proof; one routing/caching lever on held-out cases.
Evidence reused: issue-108-live-r3-2026-11-18, ai-heldout-batch-432-live-2026-11-18, closure audit. Disposition: reused plus fresh Azure re-check.
Finding: no criterion is buildable as code: candidate_comparison already enforces one lever per candidate; a live caching lever cannot register (inputs ~73 tokens, below prompt-cache threshold; 0 cached tokens observed). Quota usages routes return empty; Microsoft.Quota provider NotRegistered (subscription change out of scope).
Planning Readiness: Ready (evidence note only).
