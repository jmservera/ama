# Issue 1231 r32 root 9dad2aba propagation: research

Date 2026-11-07, same session b353a2c9. Historical R31 (c18f45f2 FULL failed, receipt 99db1c50, browser failure at workbench_browser_check.py:501, MSSQL blocked) and old FULL 799026a3 are preserved, not edited.

## Identities

* Child c18f45f23eca34ee960050027750597bd21d5dac / tree 1b465e7a..., ignored-clean, branch fix/ranking-archive-concurrent-writer-metadata, PR #1242 target feat/ranking-publication-runner-79.
* Root 9dad2aba7b10d28e567ccaae3da4453906748f5f / tree 9b20ae641f470e0cb7adb010fedf69f4007babf8, ignored-clean; 8010a486 is an ancestor.
* Declared main 7c6d135d is an ancestor of the root. Fetched origin/main is b284d0d3, one github-actions score-only commit (.github/rubric/scores/latest.json) after 7c6d135d. Recorded as drift; not merged here; the eventual FULL base must be rebaselined by the coordinator.

## Findings

* Root 9dad merged main 7c6d (normal merge 8598d06d) with its R31 fix for the browser check (workbench_browser_check.py), live-default tests (test_workbench_live_defaults.py) and the retrofit scenario manifest. Root ranking semantics (private staging, confirmed, written, committed_unconfirmed) are stated unchanged vs 8010.
* Root ranking blobs differ from the child because root uses its own helper (.publishing- stage) and the child keeps its own; the child's blobs are the intended source per earlier decisions. Expected conflicts: ranking README, helper, core tests, API wiring test, Store, server.
* Root's browser report used an unpinned Playwright 1.64.1; its correction is separate. This light stage runs no browser.

## Decision

Normal merge of exactly 9dad; child blobs win for ranking source/tests; adopt root checker, live-default tests, manifest, RPI and log. No design gap. Light checks only.
