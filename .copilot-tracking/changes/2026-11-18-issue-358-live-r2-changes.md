---
title: Issue 358 live changes, second pass
ms.date: 2026-11-18
---

No source change. Tier FOCUSED (docs and evidence only); `rpi-checks.py --all` not run. mypy and ruff not applicable: no Python changed.

Files: `docs/reference/research/issue-358-live-recheck-2026-11-18.md`, index row in `docs/reference/README.md`, log entry, RPI artifacts.

Validation (observed; raw output not retained): `python3 -m unittest infra.tests.test_setup_entra` 126 tests OK; throwaway `ca-358-throwaway` confirmed absent; demo API read-only GET shows one Key Vault reference intact. No Azure write.

| Criterion | Status |
| --- | --- |
| 1. Expired stored credential guard test | Observed; raw output not retained |
| 2. Rebuild preserves Key Vault references (non-production) | Proven for the component (live throwaway round-trip, earlier note; deletion check observed, raw output not retained) |
| 2b. Full setup-entra.py run on deployed demo app | Not proven (Graph/tenant admin, #349/#360) |
| 3. #352 conflict, delegating main() | Observed; raw output not retained |
