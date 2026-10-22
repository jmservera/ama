<!-- markdownlint-disable-file -->

# RPI Phase Details: climate-paired-alt-source-178-attribution-corr2

## Metadata

* Task ID: 178-paired-alt-source-attribution-corr2
* Task slug: climate-paired-alt-source-178-attribution-corr2
* Plan: .copilot-tracking/plans/2026-10-22/climate-paired-alt-source-178-attribution-corr2-plan.md
* Research: .copilot-tracking/research/2026-10-22/climate-paired-alt-source-178-attribution-corr2-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Correct source-bound provenance | Complete, PC-001 resolved | P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct source-bound provenance

Context: Research C3-C6 traces a static wildcard through the report despite a precise
hash-pinned raw header. Keep source name/version distinct from licence verification.
Intent: dynamic attribution, demonstrably reproducible, no wider validation changes.
Boundaries: optional header.api metadata may be inspected safely; existing _object,
numeric, timestamp, geometry and CLI-error contracts are unchanged.
Unresolved correction decisions: none.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Carry optional metadata and render precise/unverified attribution

* Inspect optional header.api only after existing header validation; non-object API metadata remains optional, not a new parser rejection.
* Retain nonblank string name/version or explicit null fields under series.api and report source.api.
* Numeric dotted major.minor.patch with optional leading v qualifies for precise attribution; other formats remain explicit UNVERIFIED. No version inference.
* Include the actual per-source retrieval date in attribution.
* Replace the static wildcard; construct fresh nested attribution dictionaries instead of mutating LICENCE.
* Keep Open-Meteo provenance, all statistics and all approval flags unchanged.
* Dependencies: completed research and disposed one-time critique.
* Completion evidence: changed metadata propagates; missing/malformed optional metadata remains parseable and unverified; repeated builds isolated.
* Actual result: source.api carries retained fields; exact/changed metadata/date and repeated-build isolation tests pass, including explicit uncertainty subtests.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add focused tests, regenerate report and update related documentation

* Test owner and maximum additions are locked in plan; no existing tests removed.
* Add constructed exact/different metadata, metadata-uncertainty subtests, shared-state isolation and retained-fixture provenance assertions (at most four methods).
* Regenerate JSON with documented CLI, unchanged retained bytes/hashes, URLs, 2026-10-22 retrieval and Durham coordinates.
* Compare old/new report after removing attribution/source-api changes; every remaining field must be equal.
* Add concise source-metadata explanation to existing synthesis, revise index row and append knowledge-base log entry. Do not update memory or original case study.
* Run requested focused unittest, narrow Ruff lint, whitespace diff check and fixture-hash/structural checks.
* Formatting checks must be baseline-aware; avoid whole-file unrelated formatting.
* Completion evidence: actual command results and diff statistics in changes record; one independent Review follows.
* Actual result: three new test methods (within four-method cap), 30 total tests pass; CLI output byte-matches report; only API block and attribution differ from the original JSON. Existing fixtures and approvals unchanged.
* Publication order: preserve original implementation Review; commit correction and dated evidence; wait for shared-lock release; full gate in a new external directory; fetch main and official current-base verification; independent exact-head publication assessment retained externally; fetch/reverify immediately before push.
* Assessment failure or any changed candidate/base/input/tool/image blocks push and requires a new gate after correction. No repeat task Review, critique or acceptance checkbox changes.
