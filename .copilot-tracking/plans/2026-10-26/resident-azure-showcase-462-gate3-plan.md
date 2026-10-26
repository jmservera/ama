# Issue 462 final gate 3 prospective plan

Written 2026-10-26T00:15Z before the run. Gate 1 (581ebda0) and gate 2 (323d955e) receipts are FAILED and retained unchanged.

## Admission (observed 00:13Z)

* Disk 12 GB free (threshold 10 GB), memory 11 GB available, heavy lock free, no other heavy runner, output dir absent.
* origin/main c8d16059 is an ancestor of HEAD; no merge needed.

## Plan

* Commit this plan only (no source change), freeze a new clean detached worktree at that exact head.
* Run `python3 tools/rpi-checks.py --all --base c8d16059c0c0a22c4ffba88c6b65ac068f64accc --lock-timeout 0 --out /tmp/ama-462-local-final-gate3` attached in the background; record the actual Python PID and log.
* Afterwards run official `--verify-receipt` from the clean candidate against fresh origin/main.
* Targeted SQL 18 / browser 55 / image 22 results exist for c79f8731 only (source head). The plan commit changes only .copilot-tracking, so source blobs are compared to c79f8731 to prove equality; the targeted run is not claimed on the plan head.
* A failure is not waived by targeted passes; no automatic fix (cycle 2 limit).
* No push, PR, cloud work, receipt or environment cleanup.
