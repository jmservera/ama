---
title: Research - #1297 correction C2 (Ruff format violation)
date: 2026-11-09
---

## Brief

* Purpose: verify and correct the C1 full-gate infrastructure failure, a pinned Ruff format check on tools/rpi-checks.py. Posture: focused, inline, no delegation (single named failure).
* Start state verified: HEAD da9ae74b42ae1b591b17a51816458253e5050efd, tree e9bcd953054a627711ac2af08845625facb8cd4f, base fa7ae0c97. `git status --short --ignored` shows only ignored tools/__pycache__/ (retained, not deleted).
* Adverse evidence preserved: /mnt/ama-gates/g1297-c1-1109/0142-infra.log, receipt.json (SHA-256 be4c663da6aca58bbbd7165e34fc0b6e9137a1f00feb0c1af716294bc735cc0f, verified unchanged), /tmp/rpi-g1297-c1-full-1109.log. Historical, not proof for a new head.
* Non-goals: any change to C1 sensor selection semantics, #184 items, speculative dependency selection.

## Findings

* C1: The gate runs `ruff format --isolated --line-length 100 --check` on the tools files (tools/rpi-checks.py lint helper, `Runner.lint`), with ruff pinned at ==0.17.1 (tools/rpi-checks.py pip install lines).
* C2: The log reports tools/rpi-checks.py:746 would be reformatted: the C1 multi-line `if (...)` condition must be collapsed to `if any(...) or (` followed by the second operand and `):`.
* C3: Local ruff is 0.17.3, not the pin. A scratch venv /tmp/ruff1297-c2 with ruff==0.17.1 and mypy==2.4.0 (external, installed because the pin was missing) reproduces the identical diff, exit 1.
* C4: Running format without `--isolated --line-length 100` yields many unrelated diffs; that is not the gate command and is not used.
* C5: C1 ran only 0.17.3 lint and no format check; the format step was omitted from my C1 validation (adverse, own miss).

## Alternatives

* A. Apply `ruff format` (pinned 0.17.1, gate flags) to tools/rpi-checks.py. Selected; semantics identical.
* B. Restructure the condition (helper variable). Rejected, unnecessary.

## Decision state

Research disposition: executed. Planning Readiness: Ready. Residual from C1 review (RV-002, RV-003: over-selection and non-sensor-named shared dependencies) unchanged and not addressed here.
