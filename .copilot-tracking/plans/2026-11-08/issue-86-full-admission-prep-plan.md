---
title: Issue 86 prospective FULL admission preparation plan
description: Plan for a later admitted normal Main integration and final FULL of the issue 86 child candidate
ms.date: 2026-11-08
---

Scope: issue #86 only. Tier FULL (lifecycle, SQL and security-sensitive candidate); rationale: store and access boundaries plus inherited gate and capacity hunks cannot be downgraded. This phase is tracking-only. Every step in the future sequence that mutates source, merges Main or runs a gate waits for a separate explicit NOW admission and does not happen in this continuation.

## This continuation (tracking-only)

1. Research, this plan, details and one independent critique before any other step; commit them alone.
2. Changes and author Review of the prospective plan. No source, tools, infra, `.github` or old incoming tracking blob change; no gate, lock, runner probe, Docker, install or polling.
3. Freeze clean; prove `git diff --name-only 4da357c0 HEAD -- src tools infra .github` is empty and tracking changes are new files only.

## Future admitted sequence (not performed now)

A. Pre-merge verification with explicit exits; stop on any drift. Run an explicit `git fetch` and re-resolve the remote parent ref, the PR #1243 head and base, and `origin/main` at every decision point (before the merge, before receipt verification, before publication); a locally stored ref alone is not current remote state: child clean ignored-inclusive at the admitted head; PR #1243 base unchanged; fresh `git fetch origin main` and resolve current `origin/main` (do not assume `2e0c676a`); #1269 merged or no longer active; ancestry of local `e888a499` and published `c5edb320`; heavy-lock holder absent and a coordinator-admitted non-queued window.

B. Inspect the INCOMING delta, defined as the verified merge base of child and fresh Main versus fresh Main (never a direct child-versus-Main diff, which contains the child's own production changes), by blob and mode for every changed path; separately inspect the prospective merge result. Stop conditions: any changed `src` production, `tools`, `infra` or `.github` workflow path other than inert records and the rubric JSON; any conflict beyond append-only records; a changed test or tool blob not covered here; unparseable rubric JSON; any need for private data.

C. ONE normal `--no-ff` merge of the freshly resolved Main object, only after A and B, with records committed first. Keep both entries of append-only logs. Never choose a whole side blindly. No rebase, force or retarget.

D. Post-merge proof: both merge parents; Main ancestor; `e888` and `c5ed` ancestry with explicit exits; executable byte proof against the pre-merge child except the declared Main files (`assistant_process_worker.py` and `test_assistant_release.py` expected); original RPI and log prefix preserved; rubric JSON mode, blob and parse. Add changes and author Review; freeze.

E. FULL on the frozen head from the repository root, derived from the maintained runner and README, not from receipts: `python3 tools/rpi-checks.py --all --jobs 1 --lock-timeout 0 --base <fresh origin/main SHA> --out <fresh new external path of at most 58 bytes> < /dev/null`, attached and foreground, stdin `/dev/null`, real console and exit file outside the receipt directory, pipeline exit preserved if `tee` is used. Expected selection: all 17 groups, fresh images, no shards, disposable MSSQL, Chromium and axe, scanners and SPDX. Group skips are reported separately from unit skips.

F. SQL proof: the `mssql` group must show the actual OK and log for each SQL selector, including `test_assistant_release.MssqlUnleasedRevocation` from Main. Ordinary conditional API skips are not SQL proof. All original skips and failures are retained.

G. `--verify-receipt <receipt.json> --base <current origin/main>`. If Main moved, the receipt is stale and the tool's own base rule applies; it is never waived by hand.

H. Coordinator verification and independent exact-head assessment of BOTH deltas, after final normalization: child versus local `e888a499` and the published-target delta versus `c5edb320`, including the inherited #1226, #1228 and #1229 hunks and the later Unknown branch. In addition the assessment covers a Main-versus-final-head review of ALL named inherited hunks and their tests (`gates.py`, `procurement.py`, `quality.py`, `store.py`, `appointments.py`, `test_gates.py`, `test_hazard_referral.py`, `test_quality_procurement.py`), because neither parent delta alone includes `gates.py` or `procurement.py`. Publication is a separate explicit coordinator step: the exact assessed head is pushed once so hosted checks can run on it; the hosted head SHA and results are verified against that head before any later acceptance, merge or ticking action. Nothing is published or treated as accepted before then. A squashed child into the parent needs a genuine new parent #81 integrated FULL; no receipt survives it.

## Boundaries

No #1238 policy relaxation, no resident, legal or professional approval, no live receiver or provider, no deployment, no closure, no criterion ticks, no cleanup or hook override, no private data. Pins here are observations, not authority; each must be re-resolved at admission.
