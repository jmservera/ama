---
title: Issue 131 read-only diagnostics phase details
ms.date: 2026-11-10
task_id: 131-readonly-diagnostics-1110
---

## Phase 1: functional probes

* Script: external `run/probe131.py` under the owned evidence directory, importing the candidate `zava_forward.core.resident_decisions` and the existing test fixtures; asserts and records the module origin lies under the worktree `src/core`. Synthetic `ZF_DATA` under the evidence directory; stores live in test-owned temporary directories.
* Probe A (finding 1): valid inventory via the supported action (control), report-trigger staleness and a re-recorded valid revision (controls), then three labelled corrupt-store injections: version-99 singleton, malformed earlier dict, blank and duplicate latest refs. Record writer outcome, view status, gate, scope outcome and hold presence.
* Probe B (finding 2): supported path Verified plus stored `Ambiguous` identity with full current links, then injected Unknown route on a linked Verified report, then an open-trigger control. Record reasons, gate and scope outcome.
* Both run on the JSON base and the inherited SQLite class. Observations are saved as JSON with raw stdout and exit code. Unreproduced claims are recorded as such.

## Phase 2: baseline comparison

* Export the base tree with `git archive fe59ef56a0084dd975fd7e5c342670bb8f788fb0 src/core` into an owned external directory.
* From its `src/core` run configured `mypy` (no file selectors, own cache directory) and `ruff format --check .` with the pinned venv tools, saving raw output and exits.

## Phase 3: candidate same-tool re-run and source equality

* Re-run the same two commands unchanged on the candidate `src/core` (own cache directory) so counts compare under identical tools; Root logs remain the authority for the first run.
* Source equality: `git diff 7f8af9b -- src README` empty, HEAD unchanged, and the working tree clean apart from the new RPI records.

## Phase 4: close

* Single Review, commit new `.copilot-tracking` records only with the privacy-safe identity and trailer, `commit-complete` witness with the commit claim, remove owned scratch (export copies, caches) but keep raw logs and probe output, write the handoff.
