# Changes: issue 462 fifth pass

Status: implemented. Tier FULL (src change); the coordinator runs the gate; rpi-checks.py --all was not run.

Changes

* src/api/src/zava_forward/api/resident_demo/app.py: the _body() Content-Length guard requires isascii() as well as isdigit(); a non-ASCII digit used to raise ValueError and drop the connection.
* src/api/tests/test_resident_demo_api.py: test_non_ascii_digit_content_length_is_a_generic_denial (failed before, passes after).
* docs/reference/research/resident-showcase-live-r10-2026-11-23.md, docs/reference/README.md, docs/reference/log.md.
* Evidence: .copilot-tracking/evidence/2026-11-23-resident-showcase-live-e/ (36 live checks, five desktop screenshots).

Validation: 82 targeted tests pass; mypy clean (375 files); ruff check and format pass. No Azure change; nothing deployed.

Per-criterion table (unticked criteria 1, 2, 6, 7, plus ticked ones re-observed)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 1. RPI artifacts and threat model | Proven for the demo | Dated artifacts, threat model note; October independent review not re-derived |
| 2. #444/#455 dependency and failed rubric | Partly proven (hosted history, local previews) | r7 note; preview tests pass |
| 3. Login and denial paths (ticked) | Proven live | 36 Playwright checks on revision 0000028 |
| 4. Secrets, HTTPS, abuse controls (ticked) | Proven live and locally | Same run; new regression test |
| 5. SQL parity, Docker, full gate (ticked) | Unproven here | Targeted checks only; coordinator gate pending |
| 6. Pre-spend record | Proven for the demo | r3 note; USD 700 owner decision |
| 7. Deployed showcase browser proof | Proven, desktop only | Live run, screenshots |
| 8. Identity and plan record (ticked) | Partly | Digest prefix known; source commit unconfirmed |

Unproven: live HSTS, Server header and Content-Length fix (need a redeploy); the full gate; owner ticking.
