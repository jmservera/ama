---
title: Issue 220 research (affected-person challenge and correction route)
ms.date: 2026-11-17
---

# Research opening

* Issue #220 (Refs only unless all criteria proven). Criteria 1-4 ticked; criterion 5 (no retaliation, inferred refusal or delayed hazard response) unticked since 2026-11-16.
* Scope: assess against criteria, record gaps, minimal doc/test. No legal approvals, no store changes. Tier FOCUSED. Base eb51af5c9.
* Evidence read so far: issue comments (audits 2026-10-31, 2026-11-05, 2026-11-16); `src/core/README.md` sections at lines 4835-4894 and 4998-5030; `src/core/src/zava_forward/core/challenges.py`; `src/api/tests/test_challenge_non_retaliation_hazard_guard.py`; `src/core/tests/test_challenges.py`.

# Findings (measured)

* Measured at base: `src/core` `tests.test_challenges` 19 tests OK; `src/api` `test_challenge_non_retaliation_hazard_guard` 8 tests OK (run with the checkout-installed packages).
* Criteria 1-4: delivered and still ticked. Criterion 5: the guard covers `challenge_open` and `challenge_resolve` against protected state (hazards with clocks, decisions, ranks) and the writer-refusal path, but only with `hazard_concern` absent.
* Gap (measured by reading tests): no test opens a challenge with `hazard_concern=True` through the API on a case with a live hazard and asserts the hazard clock and protected state stay unchanged while the referral is recorded.
* Residual, not closable in code: actual hazard-response delay measurement, representative resident/staff acceptance, owner approval of the referral age limit. Criterion 5 stays unmet.
* Planning readiness: Ready.
