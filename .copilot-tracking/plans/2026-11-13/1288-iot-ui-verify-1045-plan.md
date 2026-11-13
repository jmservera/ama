# Plan: 1288-iot-ui-verify-1045

Details: [.copilot-tracking/details/2026-11-13/1288-iot-ui-verify-1045-details.md](../../details/2026-11-13/1288-iot-ui-verify-1045-details.md)

* [ ] Phase 1: copy dc1404abb tracking files byte-identically; verify sha256.
* [ ] Phase 2: create /tmp/venv-1288-1045; pip editable install core, agents, api with --no-deps; verify zava_forward.* __file__ inside worktree src/.
* [ ] Phase 3: run 9 unittest modules with env -u ZF_DATA; capture counts, skips, true exit codes.
* [ ] Phase 4: record in changes file; remove venv; no src/ or docs/ edits.
* [ ] Phase 5: independent review, state update, clean commit (Refs #1288, #109, #110, #111).
