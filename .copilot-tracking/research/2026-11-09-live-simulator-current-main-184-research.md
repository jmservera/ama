---
title: "#184 current-main validation research: main 1f28d0913 delta, import proof and check selection"
ms.date: 2026-11-09
---

Prospective third recovery record, written before the merge, any check or any edit of this pass. It does not rewrite the C1 to C5, recovery or post-policy records, and does not reset the correction counts (this is an unchanged-source validation continuation).

## Start identity (observed 2026-11-09)

* Branch feat/demo-recovery-sensors-184-1109, clean, HEAD e0bb2bc0a06d9b7bf3b431bdd54d80c5670986bf, tree a6349582852b9583d182c76508a09cd287fd3ea0, local only.
* Freshly fetched origin/main 1f28d09130c8e058a0436d468e6a22f3c4c24f47 (unchanged since the last known value). Merge base with HEAD is 76db469b16e7ac0ae862e8c9b19873fc66b04f0e, the pin already merged. Main is two commits ahead: d4d6827fe (#1222 discovery assurance diagnostic and checkpoints) and 1f28d0913 (rubric score).
* `git merge-tree --write-tree HEAD origin/main` completes without conflict (tree 3b8567e0ae2c271b1716b824d118f1bd5b73052a).

## Evidence carried in (not rerun for original review)

* Independent FULL source assessment of e0bb2bc0a: approve_with_comments, zero Critical/High/Medium, one carried Low (exact-grant live_receiver.main, rejected data-quality under receiver grants, replay SQL test coverage). The Low stays open; no evidence in this pass closes it.
* API mypy: original 53 errors in 48 files (log retained, not waived) was environmental (declared playwright==1.64.0 absent from venv-184); after restoring it, configured and cache-free mypy are both zero errors in 199 files on the same source.
* Owned disposable SQL: default 70 tests and analysis 10 tests, zero skips; offline Bicep and unit selections pass at e0bb2bc0a.

## Delta of main since the validated merge base 76db469b1 (non-tracking only)

* src/core/src/zava_forward/core/paired_equity.py (+79/-1), src/core/tests/test_paired_equity.py (+135), src/core/README.md (+4/-1 paired-equity paragraph), docs/architecture/cutover-evidence-pack.md, docs/reference/README.md, docs/reference/log.md, .github/rubric/scores/latest.json, and 40-odd tracking records. No infra, tools, workflow, dependency manifest or Dockerfile path changes.
* The brief called this "Core discovery diagnostics/tests"; the actual changed Core module is paired_equity (fairness-pairing evaluator), which is not part of the IoT surface by name. Relevance is to be proven, not assumed.
* Overlap with the parent's non-tracking paths: docs/reference/README.md, docs/reference/log.md, src/core/README.md (textual; merge-tree clean).

## Relevance proof plan

* Source grep shows paired_equity referenced only by its test and src/core/README.md.
* After the merge: a Python import closure check importing every IoT module changed by the parent and asserting `zava_forward.core.paired_equity` is absent from `sys.modules`; blob hashes of all 31 parent-changed non-tracking source paths equal at HEAD and after the merge; the core package has no `__init__.py` that could pull paired_equity in.
* If proven independent, SQL and transport evidence at e0bb2bc0a is reused only with identical source blobs, test selectors, dependency and tool versions; the paired_equity test is the one genuinely impacted selected test of this merge.

## Planning readiness

Ready. Research disposition: executed.
