---
title: Issue 1262 correction cycle 1 manifest pin research
ms.date: 2026-11-07
---

* Task: `issue-1262-r2-manifest-pin`, successor to the original (preserved, not edited). Research disposition: `executed`. Planning Readiness: Ready.
* Trigger: PR 1263 hosted src-core run 42414829290 / job 128530646078 FAILED (2341 tests, 228.917s, errors=2, skipped=226): `test_needs_inventory...test_scenario_scope_keeps_full_application_evidence_unavailable` and `test_scenario_manifest...test_current_iteration_is_complete_and_honest`, both `ValueError: Scenario manifest: stale source hash: src/api/checks/workbench_browser_check.py` (log lines 3190-3216 of the sanitized hosted log). Not baseline or flaky. The original local partial receipt and independent review passed because the focused scope did not select Core scenario tests; they remain historical.
* Mechanism: `validate_manifest` (`src/core/src/zava_forward/core/synthetic/scenario_manifest.py` lines 98-101) compares each `sources[].sha256` in `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` with the SHA-256 of the literal current bytes. The manifest row `id: recipe` (line 47) pins `src/api/checks/workbench_browser_check.py` at `dea58169...6f0`, which equals the main checker bytes (`git show f0afa8d76`). Corrected checker bytes are `4bd825e9b340f3842771e19e8fa4d4770da4004653162cadbf5c93446bdfa320`.
* Dependents searched (`grep` of the checker path and of the old digest outside `.git` and tracking): the old digest appears only in the manifest; `perspective_walkthroughs.py`, `journey_acceptance.py` and the other checks reference the module name or import it, with no recorded hash. Precedent: `docs/reference/log.md` line 8033 records an earlier stale recipe SHA correction in the manifest.
* Red on current head `eb17f9f50` reproduced locally with the two exact tests: exit 1, errors=2, same ValueError (`/tmp/zf1262/core_red.log`).
* Knowledge base: the manifest lives in `docs/reference/research/`; a digest-only change to a provenance pin needs a log append (materially changes a maintained knowledge-base file) and no index change.
* Boundaries: digest value only; version 0.2.1, case IDs, unavailable profiles, approval statuses and validator unchanged; unrelated hashes untouched; no new SHA-constant test.
