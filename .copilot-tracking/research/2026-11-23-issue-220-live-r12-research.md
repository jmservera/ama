# Research, issue 220, run r12 (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Only unticked criterion: "No retaliation, inferred refusal or delayed hazard response". Eleven earlier runs proved it live for the constructed case (see docs/reference/research/issue-220-live-r11-revision-0054-2026-11-23.md). This run looks for a code gap.

Finding: `challenges.reject_adverse_mapping` and `assert_no_adverse_challenge_effects` match forbidden keys exactly and case-sensitively. Probe on core: `Retaliation_Flag`, ` refusal`, `hazard-pause`, `HAZARD_PAUSE`, `priority penalty` were all ACCEPTED. A caller variant bypasses the fail-closed guard. Fix: compare keys after normalising (strip, lower case, spaces and hyphens to underscore).
Out of scope: live Azure (no change to deployed code is possible without a deploy, which is not authorised here).
