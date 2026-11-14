---
title: Epic 149 child UX contract verification research
ms.date: 2026-11-14
---

* Research disposition: executed. Planning Readiness: Ready.
* Sources read: `src/api/tests/test_design_system.py`, `test_content_standard.py`, `style.css`, `chat-widget.css`, `resident_demo/web/demo.{css,js}`, `resident_preview/web/resident.css`, `web/panels.js`, `web/app.js`, and the Epic #149 issue body.
* Findings: tokens (`--brand`, `--font`, `--sp-1`, `--focus`, `--motion`) and the `prefers-reduced-motion` hooks exist in four stylesheets; non-colour cues exist as `:before` glyphs on `.flag.danger`, `.status-line.*` and `.blocked-title`; resident demo has an optional, explicit, unchecked-by-default AI-summary checkbox stating it is not consent to works; staff finance and grant screens use explicit Approve buttons.
* Boundary: Epic #149 states child features are not accepted. Human assistive-technology evidence (#155) and staff comprehension evidence (#215) are not present and must not be fabricated. The module verifies automated wiring only and asserts neither sign-off is claimed.
