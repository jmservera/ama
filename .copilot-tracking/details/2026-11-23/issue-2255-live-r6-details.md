---
title: Details, issue 2255 run 6
ms.date: 2026-11-23
---

Edit `revert` in `infra/scripts/seed_demo_hazard_clock.py`: when `noticed_was` is a key in the marker, restore it, or pop `noticed` when it was `None`. Add one test in `infra/tests/test_seed_demo_hazard_clock.py`.
