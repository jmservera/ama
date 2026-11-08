---
title: Issue 530 focused-gate admission critique
ms.date: 2026-11-08
---

* Executed: once, on the new admission plan only, rubber-duck agent, before implementation. Verdict: proceed with changes. The original critique is unchanged and not rerun.
* Confirmed correct: groups `preflight`, `namespace`, `static`; the skip list; `--base`, `--out`, `--jobs 1`; no SQL service selected.
* Finding 1 (blocking): receipt inspection comes after execution. Disposition: accepted; plan now requires an inert-only changed-path check before invocation.
* Finding 2 (blocking): `static` also runs actionlint, pip installs and the runner's unit tests; preflight does not run ruff. Disposition: accepted and verified at `tools/rpi-checks.py` lines 1008-1041; research and plan corrected.
* Finding 3: Docker daemon, Python 3.12 and possible network for installs. Disposition: accepted and documented.
* Finding 4: verification needs `--required-scope partial`. Disposition: accepted and verified (default `full`, line 3079); details corrected.
* No conflict with a confirmed user decision; no user decision required.
