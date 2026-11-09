<!-- markdownlint-disable-file -->
# Critique: discovery parent reconciliation plan (#123), 2026-11-07

Single pass by a read-only rubber-duck agent before any merge. Dispositions:

* PC-001 (blocking): an inherited core source change makes `--changed` select all five projects, four images and `logo-0600` (tool selection at `tools/rpi-checks.py`), which conflicts with this admission's stop rule on image groups. Accepted: the plan now computes the actual selection from the tool's own selection logic read-only, with no execution, before running anything. If it includes excluded groups the gate is not run, the exact blocker is returned and no partial or fabricated success is claimed.
* PC-002: compare remote refs (`ls-remote`) with the pins immediately before each merge. Accepted, applied.
* PC-003: compare inherited tracking files with the pinned parent and enumerate intended new records separately. Accepted, applied.
* PC-004: distinguish the intended inherited source-line replacement from loss of main evidence. Accepted, applied.

Not repeated.
