---
title: Issue 79 research, correction cycle 1 for the 357e842d assessment
ms.date: 2026-11-07
---

Task `issue-79-r18-357-assessment-corrections`, parent `issue-79-r17-align-post-891`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Start: branch `feat/ranking-publication-runner-79`, head `357e842d064296d4764f087f7a39006cc702f4ee`, tree `1d3f6ef1da280fc1e73aaeb56ff755912936387b`, ignored-clean; main `0f420dc9514db22081cb48fa733267d9d33a0d24` is an ancestor.
* Independent findings read in full: `/home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-79-357/functional-findings.json` (verdict approve_with_comments, three Medium, no High). The original r17 author Review is not edited.
* Finding 1 (runner `run`, policy selection): a caller-supplied `registry` is used as is. `ranking.load_policy` already verifies `ranking.policy_hash(p) == p["content_hash"]` at load, but `run` never repeats it for the selected policy, so a signed policy edited without recomputing the hash passes `signoff_problems`, is ranked and archived under the stale hash, and `ranking_publication.verify` accepts it against the same registry (it only compares the registry hash with the snapshot hash).
* Finding 2 (runner `run`, verify and schedule): `overdue`/`due` use `latest < today`; a valid archived `published_on` after the run day gives overdue false and due false. `ranking_publication.verify` only checks calendar validity, and the date is not covered by the snapshot hash.
* Finding 3 (runner `main`): status `blocked` falls through to `EXIT_OK`. Existing documented codes: 0 ok, 1 problem, 2 refused. The README does not document a blocked exit.
* Existing helpers to reuse: `ranking.policy_hash`, the existing `_refusal` shape, `_verify`, `EXIT_REFUSED`. Existing tests: `test_ranking_publication_runner.py` (`RunnerBase.go`, `cli`, `registry_patched`, `signed_registry`, `MalformedArchivedDateTests`).
* Test import path: runner tests use `/tmp/zf79venv`, which installs the `zava_forward` namespace from this worktree. Import path and source hash are recorded before the checks.

## Conclusions

* Finding 1: validate the selected registry key equals `policy["version"]`, required fields exist, and `policy_hash(policy) == policy["content_hash"]` before sign-off; refuse with code `policy_invalid`, a message naming the mismatch and a next action to restore the registry file. It applies to schedule, publish and exercise because all three report the policy. Verify does not select a policy and is unchanged.
* Finding 2: when the verified latest date is after `today`, add a problem to verify and schedule, report the window state as unknown (`overdue`/`due` null, `next_window_start` null, like the unreadable case) and refuse a non-exercise publish with code `archive_date_future`. Exercise stays no-write and unaffected. Historical (earlier) dates are untouched. No data-age tolerance is invented.
* Finding 3: map `blocked` to `EXIT_REFUSED` (2), the documented refusal code, keeping the JSON; the README states it.
* Scope excluded: helper (`ranking_publication.py`), store, ranking algorithm, policies, archive names and bytes, #1231 child lane.

## Limits and unknowns

* Whether a future-dated record should be a hard `archive_unverified` in the helper is a helper/child question; this cycle detects it in the runner only.
* No FULL, browser or SQL runs here; the combined child FULL and independent exact-head assessments stay mandatory.
