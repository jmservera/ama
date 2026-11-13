# Details
* P1: for f in ac6527569 files: git -C ../demo-infra-readiness-0548 show ac6527569:<path> > dest; compare sha256 with git hash-object/sha256sum of the source worktree files.
* P2: python3 -m venv /tmp/venv-136-1045; pip install -e src/core; python -c print(zava_forward.core.__file__).
* P3: run with output to /tmp log file, status captured directly (no pipeline).
* P4: use `bicep build --file F --stdout >/dev/null 2>/tmp/err` (same local CLI az bicep wraps); az bicep build equivalent; if restore of remote modules needed, record failure, do not use network workarounds.
