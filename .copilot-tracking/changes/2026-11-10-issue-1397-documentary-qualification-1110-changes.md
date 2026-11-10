<!-- markdownlint-disable-file -->
# Changes: issue 1397 documentary qualification

Status: prospective plan written before implement-start, then completed below. Post-implementation: no divergence. The research edit kept the original sentence verbatim and added the dated qualification bullet after it; the README edit is one line; `git diff --check` exit 0; no non-ASCII or em dash; diff is 3 insertions and 2 deletions in two files (two reworded lines, line 66 sentence retained). No runtime check was run.

Planned changes:

* Modify `.copilot-tracking/research/2026-11-10-issue-1397-rubric-incident-1110-research.md`: additive dated superseding qualification after the first-schema-valid-call sentence, and a cross-reference on the single-call shorthand.
* Modify `.github/rubric/README.md`: one-line wording change from "became the only judged call" to "is deduced to have been the only judged call".
* Add new correction records under `.copilot-tracking/` (state, research, plan, details, critique, changes, review).

Not changed: scorer, workflow, prompt, adapter, tests, config, `docs/reference`, the original handoff and the other original `ac4177b5` records.
