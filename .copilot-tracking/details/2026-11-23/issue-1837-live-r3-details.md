---
title: Details issue 1837 live r3 2026-11-23
ms.date: 2026-11-23
---

Phase 1: from `src/api`, `python3 -m unittest tests.test_nomination_api_routes tests.test_accessibility_baseline tests.test_content_standard tests.test_nomination_screen tests.test_challenge_no_retaliation_api_220 -q`, then `python3 -m checks.{nomination_route_forms,challenge,nomination}_browser_check --axe <axe 4.10.3>`.

Phase 2: `probe_negative.py` from the 2026-11-18 record with `DEMO_API_URL` set from the Container App FQDN; credentials read at run time by the helper, never printed.

Phase 3: write the evidence note under `docs/reference/research/`, append a log entry, record changes and review.
