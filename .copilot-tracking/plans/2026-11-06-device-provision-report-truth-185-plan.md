---
title: Plan for #185 truthful action report (corrective)
ms.date: 2026-11-06
---

* Step 1: write regressions first and capture RED on 117d: applied provision, applied teardown with the original manifest, and unchanged dry-run (no writes, no secret value in output).
* Step 2: `report()` takes the action and mode and returns a `credentials` string by outcome, type unchanged (str), built only after the underlying call succeeds:
  * dry run: "none created or stored; dry run only"
  * applied provision: "stored by the injected credential store; references only, no secret values"
  * applied teardown: "revoked by the injected credential store; none remain"
* Step 3: clarify the module docstring: the command line supplies no adapters; injected trusted adapters may write.
* Step 4: update the one dry-run assertion; README sentence stays accurate.
* Step 5: light checks (device tests, ruff, mypy as CI), then a dedicated Review, changes record, state record, commit locally. No push.
* Critique (single pass, self): do not catch more or suppress failures; failures raise before any report. Dry-run text must not imply a prior store. Applied.
