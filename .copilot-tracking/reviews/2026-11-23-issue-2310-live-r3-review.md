# Review (executed once)

Outcome: conformant with limits. Diff is additive: anonymous /api/ PUT/PATCH/DELETE now 401, everything else unchanged (signed-in still 501, pinned by test). No secrets read. Limits: live edge 302 unproven/unchanged (owner); no hosted CI or rpi-checks run. Follow-up: owner decision on edge 401 vs 302.
