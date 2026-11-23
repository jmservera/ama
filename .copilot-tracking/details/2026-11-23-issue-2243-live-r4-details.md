---
title: Issue 2243 details r4
ms.date: 2026-11-23
---

1. `assistant.py`: `expiry_configured(env=None) -> bool`, true only when `expires_at` would parse the setting.
2. `aoai.py`: the two entry checks choose `expiry_not_set` or `expired`.
3. Test: unset and malformed env give the "not set" label; a valid past date gives "ended"; a valid future date answers.
