# Changes: issue 227 building safety lead and repairs hazard screens (2026-11-01)

* Added: `safety-lead` ("Building safety referral queue", safety roles) and `hazard-triage` ("Repairs and hazard triage", Retrofit Coordinator, Resident Liaison Officer, Quality Inspector) read-only screens appended to `src/api/src/zava_forward/api/web/role-screens.js`, sharing one renderer. No server change.
* Added: `src/api/tests/test_safety_screens.py` (5 node-vm tests).
* Validation: new, role_screens, asset_board_screen, design_system, accessibility_baseline tests pass (29); ruff check, ruff format --check clean; mypy clean for the new test file. Run with PYTHONPATH to source trees (system pip is externally managed). Browser/axe checks not run locally; CI is the evidence.
* Review amendment (PR #653 threads): hazard tables bypass the 50-row cap via an optional `limit` argument on `screenTable` (other tables keep 50); pending acceptance names the projected `follow_up` owner (falls back to sender); legacy referrals with `referred` but no `sent_at` show a verify-external-record message instead of "No referral sent". Tests: 51-record regression, Rex follow-up, legacy referral (7 tests).
* Divergence: none from plan.
