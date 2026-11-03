# Details: issue #232 resident-staff browser evidence

* Phase 1: `SCENARIOS["232s"]` signs in as sam@example.test, opens "Resident service issue queue", expects the issue id, summary, outcome wanted, Large print, SYN-SAFE-232, the "not a message" statement and the pointer that pause or withdrawal lives on the choice screen. Queue region "Open service issues by home" must list ZF-1 and have no tel, mailto or button.
* Phase 2: `STORY_RESIDENT` branch in `check_readonly_accessibility`; the readiness-blocked assertions stay 231-only.
* Phase 3: one README paragraph after the 231 engineering-check note.
* Phase 4: see changes file.
