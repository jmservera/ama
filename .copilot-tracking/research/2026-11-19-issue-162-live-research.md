# Research: issue 162 criterion 6 (2026-11-19)

* Task: issue-162-live. Mode automatic. Demo only, desktop, FOCUSED tier.
* Disposition: reused. Prior evidence: docs/reference/research/issue-162-live-audit-2026-11-18.md and chat-breakglass-live-proof-2026-11-18.md.
* Only unticked criterion: 6, "Administrator and break-glass access is audited, with purpose, and the policy is decided".
* Fresh local check: `python3 -m unittest tests.test_chat_isolation` in src/api, 35 tests OK (grant with purpose, refusals, audit rows covered).
* Remaining gaps: (a) live grant needs CHAT_BREAKGLASS_ROLES and CHAT_BREAKGLASS_REF on the shared demo app, a config change and new revision, outside the "no production changes" authorisation; (b) administrator Entra role, user notification and audit retention are owner policy decisions, not buildable; (c) DPO/Legal approval is not needed for the demo.
* Planning readiness: Ready for an evidence-only outcome. No buildable code criterion.
