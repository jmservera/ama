---
title: Issue 217 metering wiring plan
date: 2026-11-04
---

* Slice 1 (this PR): projection of offline usage onto the closed metering schema, validated on read in `summarize`.
* Later stacked slices: wire `record_human_decision` into the approval path; simulated check and alert retention review; Foundry guard after tenant evidence.
* Critique executed once: compatible; no model call, no storage change, no stored shape change, no approval claimed. Manual path unchanged (no AI feature touched).
* Tier: focused; no security, infrastructure, SQL or deployment change.
* Details: [details](../details/2026-11-04-issue-217-metering-wiring-details.md)
