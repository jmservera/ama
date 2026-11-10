<!-- markdownlint-disable-file -->
# Plan: issue 1288 H2 matching-context observation

Readback `date -u` 2026-11-10T00:21Z. Research: `.copilot-tracking/research/2026-11-10-issue-1288-h2-matching-context-research.md`. Details: `.copilot-tracking/details/2026-11-10-issue-1288-h2-matching-context-details.md`. Verification only; ONE H2 experiment; no retry-until-green; no correction cycle.

## Steps

* [ ] 1. Record research, plan, details; run ONE critique before any observation.
* [ ] 2. Ordinary-merge `origin/main` (`ddeebd01`) into this tracking-only branch; stop on any conflict; verify product bytes equal main.
* [ ] 3. Write an external disposable harness with one H2 test (not shipped, not a test edit).
* [ ] 4. Build a fresh worktree-owned external venv from the hash-locked requirements, prove import and source identity.
* [ ] 5. ONE non-queued `flock -n /tmp/ama-rpi-heavy.lock` admission after inspecting the holder; if busy record the block and stop with the exact unexecuted step.
* [ ] 6. In that single SQL container run, in this order: the H2 test first, then the existing affected Quality MSSQL selectors (same list as the H0 run, minus the H0 and H2a/H2b harness tests).
* [ ] 7. Record changes and review; commit records only; write the handoff.

## H2 test (one test, new database)

1. `ready()` then `proactive()`: first service, first store; observe `first` (as H1 `observe`), snapshot `raw0` (all `assistant_releases` id, status, body SHA, revision; task row; controls).
2. Fresh store: `store_b = open_store()`; independent `CapturingProvider()`; `model_version`, `model_version_strong` = `test-model`; `provider.release = store_b.release_context`; no `install`, no writes, no default `Ai` call. Service B from `Assistants(store_b, ta.config())`.
3. Snapshot release rows through a fresh raw connection after each of: construction, `detail`, `release_reference`, `sensors` (per role), and record the binding digest, release reference, `release_denial`, `epoch_current`, `actionable`, `stale`, `suspension` before and after.
4. Second fresh store and service C (independent provider, same recipe) to show a repeated reopen; record the same snapshots.
5. Prove independence: `store_b is not first store`, `store_b.ai is not first provider`, different connection objects; the first store's provider and connection are never used for B or C.
6. Zero-call proof: all provider `calls`/`prompts` counters equal their value before the observations; stub-peer bytes are not used.

## Pass and fail definitions

* Confirmed: for B and C, flag `review-suggested`, actionable, equal cited IDs, pairs, role projection, task state and task body hash to `first`; release rows identical to `raw0` after every call; binding digest equal to `first`.
* Contrary: record exact differing fields and any row revision change with the call that preceded it; no defect classification beyond observation; no E12.
* Existing MSSQL selectors: report actual counts and skips; any failure is preserved as observed, not retried.
* Harness error is inconclusive, never a pass.

## Amendment after the one critique (readback 2026-11-10T00:22Z)

* Snapshots are taken through a fresh raw connection separately before and after each of: `open_store()`, provider attach, `Assistants(...)` construction, `detail`, `release_reference`, and each `sensors` role call, for B and C. `detail` is never called only to collect a "before" value; the first release-assessing call on B follows a baseline snapshot.
* The H2 test runs in its OWN unittest process first and writes `h2.json` (atexit) with the verdict before the second process starts the existing selectors, so later fixtures (which drop tables and reinstall releases) cannot overwrite H2 evidence. Both processes share the one admission and one container.
* Prerequisite gate before B's first release-assessing call: `fx-quality-evidence` active revision 1, first flag `review-suggested`, actionable, non-empty cited IDs, and B's runtime binding digest equal to the first provider's. A failed prerequisite is recorded as inconclusive, not as a matching-context failure.
* The wording is "independent same-process reopen": the first service and connection stay alive; B and C use new stores, connections, providers and services. It is not a process restart and is not claimed to be one.
* Capture task state, body hash and controls after B and C. Record each provider's `calls` and `prompts` count before and after the observations, separately (the first provider legitimately serves `proactive()`). No stub-peer is used in the H2 test, so stub-peer bytes are not measured and no byte claim is made for H2; the existing selectors report their own peer results.
