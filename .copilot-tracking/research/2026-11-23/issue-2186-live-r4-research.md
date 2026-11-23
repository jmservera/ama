# Research 2026-11-23 r4 (issue 2186)

Disposition: executed (prior r1-r3 reused). Planning readiness: Ready.

Criteria (issue has no checkboxes): relaxation recorded in verify output; code/tool/image changes still invalidate; test added. Earlier workers pinned lookalike prefixes, candidate overlap, binary docs and the matrix. New angle: `base_relaxation` judges the net `recorded..current` diff with `--no-renames`, so (a) an unread file renamed into code and (b) code added then deleted inside the moved range have no pinned behaviour.

Expected: (a) the new code path blocks; (b) the net diff is inert, so the relaxation is allowed (a conscious, fail-safe-by-content pin: the final tree equals an inert-only move).

Not applicable to a local gate tool: Azure, browser, billing, assistive-technology proof. End-to-end full receipt needs `--all` (forbidden).
