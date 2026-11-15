# #129 AC1 research: journey learning-test bundles

* Task: 129-learning-bundles-1848 (Research disposition: executed; Planning Readiness: Ready)
* Finding 1: `governance.py` holds no learning-test bundle logic. The bundles live in `src/core/src/zava_forward/core/learning_test_bundles.py` (since #1015, #1027, #1374) with `tests/test_learning_test_bundles.py`.
* Finding 2: `BUNDLES` already defines story-once, pre-visit-pack, change-impact and handover-aftercare (plus funding-evidence) each with a non-AI comparator (manual re-asking, current visit preparation, manual dependency check, paper handover), a target-zero measure, validated closed-envelope input and a stop rule. Task keys with underscores map to these hyphenated keys; renaming would break the CLI and tests, so it is not done.
* Finding 3: O10 and O18 to O20 are excluded and tested. Atlas owner mapping confirmation and DPO retention remain open human gates (not closed here).
* Gap: no single test asserting each of the four AC1 bundles has a non-AI comparator and passes its own zero measure.
* Evidence label: constructed-case evidence only; saved minutes remain capacity until Finance validates.
