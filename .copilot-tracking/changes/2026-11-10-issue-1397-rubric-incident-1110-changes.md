<!-- markdownlint-disable-file -->
# Changes: issue 1397 incident documentation

Date: 2026-11-10. Status: implemented, pure documentation. The prospective record written before implement-start named the same single source file; no divergence.

## Changes

* Modified `.github/rubric/README.md`: 89 added lines, none removed, one new subsection `### Run 42838857558 criterion-set rejection (2026-11-10, Refs #1397, #1383)` after the #1383 process qualification and before `## Files`. The #1383 section is untouched.
* Added dated RPI records under `.copilot-tracking/` (research, plan, details, critique, changes, review, state).

## Validation (documentation tier, no runtime gate)

* `git diff --check` exit 0; the diff is additions only; added lines are ASCII with no em dashes.
* Source binding: commit, blob, run, job count, pull request and timestamp values come from the supplied run, artifact, job-log and `safeoutputs.jsonl` files and were re-derived from git (`git rev-parse <commit>:<path>` at `901fea60`, `6cc59776`, `eff05737`; `latest.json` at `6cc59776` and `c66370042`) and read-only `gh` metadata.
* Not run, by design: scorer, adapter, gate, tests, linters, workflows, installs, browser, SQL, image or cloud tooling. No blanket `rpi-checks` receipt exists or is claimed.

## Not changed

Scorer, gate, adapter, prepare, workflow source and lock, prompt, tests, rubric registry, baseline, shared knowledge base, index, log and `docs/reference/`.

## Amendments and divergences

None.
