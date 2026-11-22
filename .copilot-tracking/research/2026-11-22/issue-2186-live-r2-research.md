# Issue 2186 live research, second run (2026-11-22)

Goal: full gate receipt stays valid across docs-only main moves in `tools/rpi-checks.py`, with tests. Focused tier (tools only; no src change).

## Evidence

* The feature is on main: 8c27b4940c (#2221) added full-receipt relaxation and cd687ef558 (#2272) added the verify-output test. `validate_receipt` calls `base_relaxation(..., inert_only=receipt["scope"] == "full")`; `verify()` prints `BASE RELAXED (kind)`.
* Prior run artifacts (`issue-2186-live-*`) are tracked on main; this run writes separate `-r2` files.
* Issue state is OPEN with no comments; its four criteria are unticked.

## Gap

An end-to-end verify of a real full receipt needs `rpi-checks.py --all`, which is forbidden here. Azure, browser and credentials do not apply to a gate tool.

Disposition: reused (existing evidence plus a fresh test run). Planning Readiness: Ready.
