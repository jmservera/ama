---
title: Issue 358 live changes
ms.date: 2026-11-18
---

No source change. Tier: FOCUSED (documentation and evidence only; `rpi-checks.py --all` not run).

Files: research note, evidence folder, index and log entries, RPI artifacts.

Validation: `infra/tests/test_setup_entra.py` 126 tests OK; mutation run 8 failures; Azure throwaway deleted.
mypy/ruff not applicable (no Python source under src/ or infra/ changed; `roundtrip.py` is an evidence script).

| Criterion | Status |
| --- | --- |
| 1. Expired stored credential guard test | Proven |
| 2. Rebuild preserves Key Vault references (live ARM, throwaway app) | Proven for the component |
| 2b. Full setup-entra.py run on deployed demo app | Not proven (Graph/tenant admin, #349/#360) |
| 3. #352 conflict | Not re-tested; delivered by #374 |
