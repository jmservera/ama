# Plan: issue 144 queue-slice recovery (2026-11-09)

Critique: not run separately (bounded recovery, no design choice); direct disposition recorded in review.

* P1 Merge current origin/main locally into the seed.
* P2 Apply the surviving `f7cb6dea4` poison-size correction only.
* P3 Run owner-selected demo-targeted tier (details file), no `rpi-checks --all`.
* P4 Record evidence and freeze candidate. No push, PR or retarget.
