---
title: Details for issue 619 automated accessibility slice
ms.date: 2026-11-03
---

* Harness: `main(..., env_overrides=...)` merges after the defaults, so the existing checks are unchanged.
* Principal: base64 JSON with `auth_typ` aad, tenant, object id and the `ZavaForward.Coordinator` role, accepted by `TrustedProxyProvider`.
* Run: `python -m checks.production_config_a11y_browser_check --axe <4.10.3> --out <new dir>` from `src/api` with the README PYTHONPATH.
