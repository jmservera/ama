# Research: issue 230 programme queue paging

Disposition: executed (reused prior 230 research). Planning Readiness: Ready.

Merged for #230: #496, #662 (criteria 1-3), #781 (browser keyboard and axe proof), #818 (withheld panel), #854 (design-system class guard), #931 (check hardening). Closed unmerged: #489.

Evidence: `programme-queue` overview in `src/api/src/zava_forward/api/web/role-screens.js` loads one `GET /api/cases?view=all&limit=50&offset=0` page. The server accepts `limit` 1-100 and `offset` (`server.py`). Cases beyond the first 50 were unreachable from the screen, so returned work on later pages was invisible (criterion 1 gap named in #931 as "portfolio-level returned work").

Smallest slice: Previous page and Next page buttons (native buttons, keyboard operable, GET only), URL scope unchanged, scope filter stays per page and says so. A true portfolio-wide returned-work endpoint is a later slice (server change).

Unmet after this slice: criterion 1 portfolio-wide returned work (paging only reaches pages one at a time) and planner role (owner decision); criterion 4 WCAG 2.2 and assistive-technology acceptance (#151, #155); criterion 5 Fluent adoption (#150). No AI feature touched; no approval or consent boundary changed. Not security, infrastructure, SQL or deployment: focused tier.
