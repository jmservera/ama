# Details
P1: `git apply /tmp/184.patch` (diff of candidate, excluding tracking). P2: new src/api/tests/test_sensor_handover_verify_guard.py using tempfile CSV and mock.patch on run. P3: edit main() in sensor_handover_verify.py. P4: venv /tmp/venv-184, editable installs of core and api, verify paths in worktree; env -u ZF_DATA -u ZF_TEST_MSSQL.
