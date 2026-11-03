---
title: Issue 217 research, Foundry query minimisation slice
date: 2026-11-03
---

* Disposition: executed. Planning Readiness: Ready.
* Merged delivery: #353 (synthetic audit, injection and cross-role tests, role/purpose allowlisting offline), #506 (content-free usage), #642 (DPIA scope pinned), #695 (readiness gate and criteria matrix).
* Proven criteria: audit logging; injection and cross-role tests.
* Human or tenant gated, not claimable: DPO DPIA, DPO retention periods, Entra role assignments, Art 22A to 22C named human and reasons, metering DPIA scope.
* Gap with a code-only slice: no purpose-scoped field allowlist for a Foundry query (criterion 3, partial).
* Slice 1 (this PR): `minimise_query` in `regulatory_privacy.py`. Later slices: wire to a live Foundry call once tenant evidence exists; check/alert retention simulation.
* Security-sensitive tier: no. Offline pure function; no infrastructure, SQL or deployment. Focused validation applies.
