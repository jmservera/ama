<!-- markdownlint-disable-file -->
# Storytelling Review, Iteration 6, AMA Mentor Progress Review Deck

## Audience and Outcome

The primary audience remains the AMA mentor. The communication job is to make
the evidence-led change from five end-to-end agents to agent-led modernisation
easy to challenge, while preserving enough time for discussion. The intended
outcome is targeted mentor feedback on the four decisions on slide 14.

The deck should continue to combine:

* Scientist framing for the evidence, method, limits and traceability.
* Therapist framing for resident agency, colleague accountability and the
  explicit absence of real resident or staff evidence.
* Sergeant framing for the recommendation, pilot gates and mentor questions.

## Verdict

The storyline and substantive project content remain current against the
addendum, knowledge-base log, memory and company research. No slide needs to be
added, removed, merged or reordered.

Three changes are required before republishing:

* Update Git evidence from 41 to 42 non-merge commits through 27 September.
* Update the appendix to distinguish the 42 non-merge commits through
  27 September from five pull requests merged by 28 September.
* Repair clipped citation footers on slides 4 to 12. The exported images omit
  the opening characters, and potentially the ending characters, on the
  longest source lines.

Main speaker notes are 1,967 words. The changes should not increase the main
notes and must keep them below the 2,000-word budget.

## Findings

### SR6-01: The Git commit count is stale

* Severity: Medium
* Slides: 3 and 15
* Evidence: `git rev-list --count --no-merges HEAD` returns 42. The same command
  limited to commits before 28 September also returns 42. The deck and primary
  research currently say 41.
* Exact proposed change:
  * Slide 3 source: change `41 commits` to `42 non-merge commits`.
  * Slide 15 Git card: change `41 commits` to `42 non-merge commits`.
  * Update the matching evidence row in `research/primary-research.md`.
* Rationale: the deck should state what was counted and remain reproducible.

### SR6-02: The merged pull-request count is stale

* Severity: Medium
* Slide: 15
* Evidence: `gh pr list --state merged` reports pull requests 1 to 5 as merged.
  Pull requests 4 and 5 merged on 28 September. The current card says three
  merged pull requests because iteration 5 was built before those merges.
* Exact proposed change: use `42 non-merge commits, 10 to 27 Sep, and five
  merged PRs by 28 Sep; the log records what changed and why`.
* Rationale: the wording preserves the research window while making the later
  repository event explicit. The title-slide research period can remain
  10 to 27 September.

### SR6-03: Long citation footers are visibly clipped

* Severity: High
* Slides: 4 to 12
* Evidence: the current exported JPGs show the longest source lines beginning
  at or beyond the left slide edge. Examples render as `ources:` or `ource:`
  rather than `Sources:`. Slides 3, 13, 14 and 15 show the intended inset.
* Exact proposed change: make every affected source footer fully visible with
  at least a 0.5-inch edge margin. Prefer concise citations, explicit
  left-alignment and a two-line footer when needed. Preserve the source
  meaning, 9-point minimum text where practical, and separation from the
  content above.
* Validation: inspect the re-exported images for slides 3 to 13, not only the
  changed YAML. Confirm that both the beginning and ending of every citation
  are visible.

## Items Deliberately Left Unchanged

* Keep 15 slides. The evidence delta does not justify a structural change.
* Keep the title-slide period as 10 to 27 September. The project research and
  document changes covered by the story still end on 27 September.
* Keep the four mentor questions on slide 14. No later document resolves them.
* Keep the cautious Phase 2 wording. The addendum says the intended
  30 November 2026 commencement still requires verification of the
  implementing instrument before operational rules are activated.
* Keep the evidence-class labels and the qualification that role-agent answers
  are sector-informed hypotheses.

## Delivery Guidance

Open with the bottom line from slide 1, then slow down on slides 4, 6 and 10 so
the mentor can distinguish case facts, planning estimates and hypotheses. On
slide 14, pause after the first question and invite the mentor to choose the
decision to discuss first. Do not rush through all four questions.

## Acceptance Criteria for the Builder

* Slides 3 and 15 show the verified commit and pull-request evidence.
* Citation footers on slides 4 to 12 are complete and readable.
* The deck keeps 15 slides and main notes remain below 2,000 words.
* Deck and geometry validators report zero issues.
* Re-exported images for slides 3 to 13 have been viewed.
* The working PPTX and `docs/presentations/ama-mentor-progress-review.pptx`
  have identical SHA-256 hashes.
* Iteration 6 updates the change record, primary research, knowledge-base
  index row and append-only log consistently.
