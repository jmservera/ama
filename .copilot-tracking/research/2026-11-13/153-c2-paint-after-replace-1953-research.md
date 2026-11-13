---
title: 153 c2 painted-after-replace research
---

Disposition: reused (review finding in `/home/azureuser/source/ama-demo-wt/review-153-btns-1921/.copilot-tracking/reviews/2026-11-13/153-btns-closure-review-1921-review.md`).

Evidence: `paint()` in `src/api/src/zava_forward/api/web/app.js` sets `painted = true` before `content.replaceChildren(...)`. A throw inside paint on first load leaves `painted` true with empty content, so the catch skips rendering "Try loading briefing again" and the notice names "Refresh briefing", which is not rendered.

Fix: set `painted = true` after `replaceChildren` succeeds. Test: a node run of the extracted `paint`/`load` catch logic with a throwing `paint` on first load.

Planning Readiness: Ready
