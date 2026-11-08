---
title: Issue 530 focused-gate admission changes
ms.date: 2026-11-08
---

* Start: HEAD `ed19cb941e9e562a28eea91285aa4490f23244e2`, tree `d9129d4378fd1ad0b2613cfe85a959019704a22a`, Main `f548b65f4aa31eb92a2cc9cb801130e422daed7f`. Only `.copilot-tracking/` records are added; the original seven records are byte-unchanged and the original blocked Phase 4 is not relabelled.
* Executable inputs: git tree ids of `src`, `tools`, `infra` and `.github` at this candidate equal those at `ed19cb94` (`a59e4c48becd662a178a56b3329da3cfbb3fee66`, `4e21fc7440c39c7d67728a938938c0f47751034d`, `c1c120a8fdb14b2620a981597a3e333e29c4091a`, `8b0afca00f621ae3422640d8befe85ad8109e5d2`). The original 71-test unit result (exit 0, 0 failures, 0 errors, 0 skips, in-process worktree-only origin assertions, no installation) therefore stays qualified to these unchanged blobs. No unit test was run again; this is not a new execution claim.
* Executed in this continuation: read-only inspection of `tools/rpi-checks.py` and git. Not executed: the runner, dry runs, Docker/Trivy or other probes, SQL, browser, services, images, scans, installs, lock polling, tests.
* Result: admission plan, details and prospective selection recorded (`preflight`, `namespace`, `static`; skips and reasons in the research record); critique corrections applied.
* Prospective command (NOT YET ADMITTED): `python3 tools/rpi-checks.py --changed --jobs 1 --lock-timeout 0 --base <fetched-origin-main-sha> --out /tmp/rpi-530-focused-<new> < /dev/null`, one attached bounded invocation, only after the canonical lock is free and the inert-only path check passes.
* Still unmet: #530 criterion "Local unit, browser and SQL checks pass" (SQL role matrix and cost ledger tests, browser/axe checks); live sign-in, private-runner, model price and budget, authority and human approvals; live employee-site verification. Unit evidence is synthetic and stubbed.
* Divergences: none.
