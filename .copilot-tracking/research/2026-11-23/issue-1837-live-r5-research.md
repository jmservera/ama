---
title: Research issue 1837 live r5 2026-11-23
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready. Base `d23b7c83e8`.

Findings: the form-transport fix and the 66-test regression set are already on main (see r2 evidence note). Gap found in `src/api/tests/test_nomination_api_routes.py`: criterion 3 names same-origin/CSRF boundaries, yet no unit test exercises the missing `X-ZF-CSRF` refusal (server.py enforces it only for the `trusted-proxy` provider) on the nomination write route. Live probes (revision 0000055, r2 note) showed 403 without the header but that is not a repeatable test.

Target: a test that, under the trusted-proxy provider name, refuses a nomination acknowledgement lacking `X-ZF-CSRF` with 403 and writes nothing, and accepts it with the header.
