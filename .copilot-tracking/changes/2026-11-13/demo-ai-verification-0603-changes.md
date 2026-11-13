---
title: Demo AI verification 0603 changes and evidence
description: Observed result, BLOCKED before any test execution
ms.date: 2026-11-13
---

* Outcome: BLOCKED. Tests run: 0; skips: 0; pass: none claimed. No source modified: sha256 over `src/core` and `src/agents` files is `0f83416eb3cf74644c9bfcc364e5f25820f1e745b49ac976f69153128cf00138` before and after; worktree clean at start.
* Adverse attempts (external raw files in `/tmp/ai-verif-0603/out`, sums in `SHA256SUMS`): venv without setuptools -> `ModuleNotFoundError: _distutils_hack` (pip exit 2); with local Debian setuptools 68.1.2 copied in -> `pip install --no-index --no-build-isolation --no-deps .` exit 1 for core and agents, `invalid command 'dist_info'`; package requires `setuptools>=77` and no wheel/new setuptools is available offline. A pip-cache wheel set for `zava_forward_*` exists but is of unproven source and was not used. Import probes under `env -i`: system python and venv both exit 1 `ModuleNotFoundError` (the probe file shows 0 for the venv line because `tail` status was captured; true python exit is 1).
* Declined: running with `PYTHONPATH`/`.pth` to the snapshot, editable or primary-env runs, or network install. Timestamps UTC 2026-11-13T05:51Z to 05:55Z.
* Claimed vs observed: the 0548 expectation that a clean venv could be built offline was not observed; it needs a local setuptools>=77 and wheel.
* Not established: #891 failure-root attribution (owner hold, not addressed by unit checks), #531 live acceptance, assistive-technology, provider and human outcome proof. Full demo acceptance is not claimed.
* Next: supply offline setuptools>=77 and wheel (owner action), then rerun Increment A unchanged.
