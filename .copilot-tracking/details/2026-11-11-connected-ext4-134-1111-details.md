# Details: #134 extension E4

* Owned paths: src/api/checks/connected_home_browser_check.py, src/api/tests/test_connected_home_check.py, new ext4 tracking, handoff.
* Env: HOME=/tmp/z134/home, TMPDIR=/tmp/z134/tmp, venv /tmp/z134/venv after verifying python, module and distribution origins (distributions are editable installs of this worktree). No installs unless a chosen command fails for a missing dependency.
* Capture: fresh directory /tmp/z134/e4-<UTC> by mkdir (refuses if present), noclobber, name.out, name.err, name.exit written from the command's own exit before any display; new basename per attempt; no overwrite; /tmp/z134 originals untouched.
* Hashes of source, test and evidence files recorded in the handoff.
* Browser: local synthetic fixture only, flock -n -E99 /tmp/ama-rpi-heavy.lock; if held, record blocker, no queue.
