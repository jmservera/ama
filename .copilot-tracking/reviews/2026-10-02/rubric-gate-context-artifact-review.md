<!-- markdownlint-disable-file -->

# Plan, Changes and Review: rubric-gate-context-artifact

* Task ID: 2026-10-02-rubric-gate-context-artifact (child of 2026-10-02-rubric-gate-push-test-head-parent)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-score-gate-review.md (RV-002)

## Plan

* [x] P01-T01 `rubric_prepare` builds the agent context on the scored commit (same `--out` path the agent reads) and uploads it as artifact `rubric-context` when scoring.
* [x] P01-T02 Agent `pre-agent-steps` only download the artifact; the duplicate tool load and context build after gh-aw's `.github` restore are removed.
* Critique: not dispatched (the fix is RV-002's stated option 1).

## Changes

* .github/workflows/rubric-score.md and recompiled lock (gh-aw v0.89.21, 0 warnings).

## Validation

* Compile succeeded. Lock order: `restore_base_github_folders.sh` (line 577) then `Download rubric context` (587) then the Copilot CLI step (872); upload in `rubric_prepare` (2030).
* Context paths (`changes_diff`, `extracted_text`) stay valid because upload and download use the same `/tmp/gh-aw/agent/rubric` path; the agent container mounts `/tmp/gh-aw` read-write.
* Not yet run on GitHub.

## Review (one pass, inline)

* Outcome: Conformant with findings.
* RV-002 closed in design: the agent's context is computed from the same checkout, base ref and scripts as `rubric_prepare` and the gate, so the `.github` snapshot no longer affects it, and the setup PR can no longer fail on a missing `prepare.py` in the agent job.
* RX-001 (Info): the agent still reads `.github/rubric/rubric.json` from the restored snapshot for criterion titles; on the setup PR that file may be absent. The rubric guide in `docs/` covers the same criteria, so scoring is unaffected. Live confirmation pending.
* RX-002 (Info): compiler notes newer major versions of upload-artifact and github-script; deferred per the dependency curfew preference.
