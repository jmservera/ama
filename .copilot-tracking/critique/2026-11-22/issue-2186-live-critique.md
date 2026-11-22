# Issue 2186 live critique (2026-11-22)

Executed once on the final candidate plan. Verdict: proceed.

* Adding a test only is the right size; the feature exists since #2221. Re-implementing would duplicate it.
* The new test must use a real full-scope receipt through `verify()`, patching only `require_fresh_images` and tool identity so no Docker is needed. Direct disposition: applied.
* A full run (`--all`) is forbidden by the brief; record as unproven.
* Tier: focused (tools test only, no src change, no workflow or gate semantics change).
