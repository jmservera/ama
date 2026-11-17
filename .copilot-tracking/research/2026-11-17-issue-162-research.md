# Issue 162 research (2026-11-17)

Scope: chat and memory user isolation on main eb51af5c9. No Core store change. Disposition: executed.

Measured: `PYTHONPATH=../core/tests:../agents/tests:tests python3 -m unittest test_chat_isolation test_regulatory_chat_api -q` from src/api: 44 tests OK.
Criteria 1 to 5 delivered (PR #286). Criterion 6 is a DPO/Legal decision (OD-46); not inferred.

Gap hunt in `_chat` routes (server.py) versus `test_chat_isolation.py`: a second user's access to another user's
live memory item (`/memory/{id}/edit`, `/memory/{id}/delete`) is untested; the existing delete test only
covers the owner. Also untested: cross-user `/threads/{id}/ask`, `/proposals` (ask covered in test_chat_panel).
Planning Readiness: Ready. Smallest slice: one regression test for cross-user memory edit/delete (and thread ask/archive spoof).
