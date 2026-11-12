<!-- markdownlint-disable-file -->
# Narrow engineering proposal for the #184 live demo: changes (2026-11-12)

Documentation only, per [the plan](../../plans/2026-11-12/issue-184-narrow-design-proposal-1112-plan.md) and [the details](../../details/2026-11-12/issue-184-narrow-design-proposal-1112-details.md).

## Added

* [IoT research plan](../../../docs/reference/research/iot-sensor-analytics-research-plan.md): subsection "Narrow engineering design proposal (2026-11-12, Refs #184)" before `## Constraints`; frontmatter `ms.date` set to 2026-11-12.
* [Reference index](../../../docs/reference/README.md): one pointer in the #110/#184 paragraph.
* [Log](../../../docs/reference/log.md): one appended 2026-11-12 entry.
* Tracking: state record, research, plan, critique, details, this file and the Review.

## Amendments and divergences

* Critique finding 8 corrected an overstatement in the author's own new research file (additive, recorded in the critique). No 2026-11-11 artifact was touched.
* The log entry was appended with a shell `printf` append rather than the edit tool; content is a pure append (earlier entries unchanged, verified by diff).
* Divergence: the rpi-* skill bodies were not loaded; the phase protocol was followed from the agent instructions. Recorded in the Review.

## Not changed

No source, test, infrastructure, guard, workflow or dependency file; no regulatory snapshot, case study, memory file or 2026-11-11 record. No push, pull request or issue edit.

## Validation (documentation tier)

Run: relative-link check of changed files (new links resolve; unresolved links in `log.md` are pre-existing older entries), `git diff --check` (clean), state JSON parse (ok), em dash check (none), spot check of cited source anchors. Not run: runtime, unit tests, complete gate, hosted CI (local candidate only).
