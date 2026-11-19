# Research: issue 215 live, 2026-11-19

Disposition: reused. Planning Readiness: Ready.

Unticked criteria: (3) WCAG 2.2 AA with no colour-only status, keyboard operability and plain-language mode; (5) comprehension tested with staff.
Existing evidence: docs/reference/research/regulatory-ux-live-215-2026-11-18.md and issue-215-live-rerun3-evidence-2026-11-18.md. The plain-language mode announcer (`regulatory-mode-state`, aria-live) exists in src/api/src/zava_forward/api/web/chat.js and is covered by tests/test_regulatory_a11y_cues.py; only the deployed build predates it.
Conclusion: no buildable gap remains. (3) as a whole needs assistive-technology testing, waived by the owner for the demo, so no conformance claim; (5) needs staff participants.
