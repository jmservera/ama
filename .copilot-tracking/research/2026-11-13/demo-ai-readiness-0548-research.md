---
title: Demo AI readiness research for #891, #107, #108, #531 and #159
description: Literal acceptance criterion dispositions at main 15bfee2d7, documentation only
ms.date: 2026-11-13
---

## Scope and boundaries

* Existing issues only: #891, #107, #108, #531, #159. Read-only research at main `15bfee2d7`, tree `ae86f25e4317801cc0bee6f1066024280ee6b0ec`.
* No source change, new issue, model, cloud, provider, scoring, private dataset, `.env`, push or PR. Research disposition: `executed` (bounded), reusing prior same-scope ledger results.
* Read: current issue bodies and the last two comments of each issue; prior `demo-run-ledger.md` entries (lines 13970-13981, 14015, 14060, 14136, 14277, 13812); source `src/core/.../chat_panel.py` (receipt, bounds, fallback), `assistants.py` (usage envelope, model-mismatch), `src/agents/tests/test_candidate_comparison.py`, test names in `src/core/tests/test_ai_consumption.py` and `test_chat_panel.py`.
* Not read: the two specifications and `docs/reference` index and memory in full (time budget); the `github-backlog-manager` agent was not invoked as a separate review pass. These are disclosed reading gaps, not evidence of absence.
* Not executed: no test. The editable installs of `zava-forward-*` point at the primary checkout `/home/azureuser/source/ama`, not this worktree, so running them would test a different tree and a `PYTHONPATH` substitution is prohibited. Zero tests run is not proof of anything.
* Known pending inputs, not main and not rediscovered: #184 `e904ba4c0` (static functional Pass, metadata Partial, SQL unrun, format FAIL), #74 `f50c5c7fd` display plus evidence `6c86e1dc` (local-ready, no criterion 2 acceptance). Spent correction history for #891 is UNKNOWN, not zero or exhausted.

## Literal criterion dispositions

Legend: DELIVERED = ticked and source present; IMPL-UNVERIFIED = source/tests exist, not run by this task; HUMAN/CLOUD = needs live Azure, serving, human or approval evidence; MISSING = source-backed gap; UNKNOWN = not determinable here.

### #891 (chat demo activation)

* AC1, AC3, AC4, AC5, AC6: ticked on the issue; AC6 live check is human/cloud and already recorded. DELIVERED.
* AC2 per-call gate, token/cost admission, privacy refs, retention, refusal stay in force: unticked. Merged #1339 (transport witness) and #1468 (settlement) exist per issue comments. The only identified gap is intentional #602/#432 behavior: a dispatched failure root stays unjoined and reports Unknown (prior research handoff `8c735ae5`, NOT_READY). Changing it needs a deliberate accounting decision (failure-envelope meter fields, fallback `eligible=False`, `chat_panel` ownership) and a finite correction scope. Spent correction history: UNKNOWN. Disposition: prior same-pin analysis already proves it; stop this lane.

### #107 (five assistants)

* Seven RAI and four base criteria ticked. Of the unticked RAI criteria: release record persistence, serving-version attestation with quarantine, independent SQL race tests and the matching-exercise record all depend on actual SQL, release/serving-version and Azure evidence (HUMAN/CLOUD plus actual SQL unrun). `model-mismatch` handling exists in `assistants.py` (around line 1575) and the clamp regression #1271 and process revocation tests #1268/#1489 are merged: IMPL-UNVERIFIED for the engineering part, not a new slice.
* Tokenomics usage per assistant and per accepted proposal: unticked, but `ai_consumption.py` and `test_ai_consumption.py` (lines 356-369, 527-589) already define `tokens_per_accepted_proposal` and `cost_per_accepted_proposal` with Unknown handling. IMPL-UNVERIFIED; the remaining unknown is whether telemetry excludes raw case content in every path, which needs a run, not new source.

### #108 (evaluation harness)

* Ticked criteria delivered. Region/quota (#1417 metadata only), held-out freeze, five-assistant coverage, human detection, effort comparison, actual-call authorization, serving attestation: HUMAN/CLOUD.
* Cheaper candidate that raises critical misses is a failure, one lever at a time on the same cases: `test_candidate_comparison.py` lines 95, 144, 183, 190 cover them. IMPL-UNVERIFIED (not run here). Comment 2026-11-13 already establishes no distinct local increment to raise the six-versus-seven family count.

### #531 (loading and HAX)

* Criteria 1-6 delivered by merged PRs listed in the 2026-11-04 comment. Criterion 7 live verification is HUMAN/CLOUD (owner-run employee sign-in on the current build). No code slice. Prior same-pin disposition holds.

### #159 (conversation panel)

* Five engineering criteria ticked; authenticated 400 receipts delivered by #1320. Keyboard, screen-reader and announcement acceptance: HUMAN (named assistive-technology acceptance).
* Tokenomics criterion: `ChatPanel._receipt` records `model_calls`, `tokens`, `provider_outcome`, `outcome`, `context_limit_chars`, `history_limit_chars`; `LIMIT_REACHED` fallback is tested in `test_chat_panel.py` around line 391. IMPL-UNVERIFIED. Anonymous 401 and other 400 branches remain unproven but are a separate no-actor policy decision, not an engineering gap proven here.
* Dependencies #158, #105, #107 not re-read beyond issue body.

## Planning readiness

Ready for one verification-only increment; no source-backed missing initial engineering slice was found. See the plan.
