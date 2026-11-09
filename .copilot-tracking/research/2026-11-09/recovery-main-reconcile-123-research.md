<!-- markdownlint-disable-file -->
# Research: recovery main reconciliation for adopted PR 1222 (#123), 2026-11-09

Refs #123, #128, #440. Seed: published head `cfd1bca86d8e3566ec0d43e87a9bf6f62203d4f9` on `feat/discovery-assurance-integration-123`; local branch `fix/demo-recovery-123-1109`.

## Findings (read-only, observed 2026-11-09)

* PR 1222 reports `CONFLICTING` against `main`; published-head hosted checks were green.
* Fetched `origin/main` = `b46a9ad9a9619db535368d1b2cbbddec8110e122`; merge-base with the seed = `f548b65f4aa31eb92a2cc9cb801130e422daed7f`; main is 24 commits ahead.
* `git merge-tree --write-tree` of seed and main produced a tree (`49879f4069fbe1a5fdb945bcf236f72c403a71e9`) with no conflict records, so no textual conflict is forecast. GitHub's CONFLICTING state may be stale or semantic; unresolved intent is a blocker.
* Main's delta since the merge-base touches `docs/reference/README.md`, `docs/reference/log.md` (both also appended by the topic), `src/core` (`doc_controls.py`, `test_chat_privacy.py`, `test_sensor_analysis_mssql.py`) and unrelated UX and company notes. The topic's own core delta is `paired_equity.py`, `test_paired_equity.py` and `src/core/README.md`.
* Original adverse evidence (`.copilot-tracking/reviews/2026-11-08/parent-refresh-123-review.md`, the failed `g123-f13-1108` receipt record, held #123/#128/#440 acceptance) is preserved and not edited.

## Planning readiness: Ready

Disposition: executed. Scope: bounded constructed-comparability diagnostic plus original tracking and KB checkpoint evidence. No production assurance, fairness policy, legal acceptance or new diagnostics. `fairness_evidence=False` and `activation_allowed=False` stay.
