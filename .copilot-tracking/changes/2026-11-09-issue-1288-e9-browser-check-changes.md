---
title: Issue 1288 E9 browser check changes and review
ms.date: 2026-11-09
---

# Issue 1288 E9 changes and review

## Changes

* `src/api/checks/quality_sensors_browser_check.py` only. The stale expectation "Proposal stored as unapproved" is replaced by assertions that the guarded-off production route shows "Not sent (real-provider-route-unavailable)", "nothing was sent to a model" and the manual-route pointer, and that no proposal is stored. The existing `seed` helper then inserts a clearly synthetic stored proposal (model "seed", cited reading from the public simulation fixture) so every later supplied-versus-cited assertion still runs. No assertion removed or weakened; `send_fence_supported` and product code untouched.

## Evidence (existing `.venv-1288`, in-worktree, gitignored, azure-storage-blob present; Chrome at /usr/bin/google-chrome; axe 4.10.3 read-only from a local gate copy, identical sha256 880970c0... across 5 copies)

* O1 observed in the 440 checkpoint (preserved, not edited): exit 1, same failure.
* Red here before edit: exit 1, same assertion (logs-1288-e9/red.*).
* Green after edit: exit 0, 30 checks passed including all axe scans (logs-1288-e9/green.*). Run under one non-queued `flock -n /tmp/ama-rpi-heavy.lock`, acquired.
* `ruff check .` 0, `ruff format --check .` 0, `mypy` 0 (211 files) from src/api.
* Not rerun: Core, API unit, SQL, Agents, 861 suites (check-only delta; earlier results historical).

## Review (original, direct)

No findings. Residuals unchanged: real-provider route OFF, ordinary-dispatch post-fence risk, local-only cancellation, final-head SQL audit persistence unproven, whole #1288 open. E1-E9 spent; E10 remains.
