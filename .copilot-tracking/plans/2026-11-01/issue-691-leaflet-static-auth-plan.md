---
title: Issue 691 follow-up plan
date: 2026-11-01
---

* Phase 1: For non-HTML static files on the trusted-proxy path, check only `provider.authenticate(headers)` (token validation, no store access). Keep the full `_user()` binding for `index.html`.
* Phase 2: Add a regression test that injects a store failure into `identity.bind` and requires a whole 200 `/vendor/leaflet.js`.
* Phase 3: Focused validation (unit tests, ruff, mypy), no `tools/rpi-checks.py --all`.

Critique (single pass, executed): compatible. Risk noted: unbound contractors can now fetch public JS and CSS; those files carry no data and still need a valid Entra token. Accepted.
