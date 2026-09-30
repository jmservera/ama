<!-- markdownlint-disable-file -->
# Build and Validate: Iteration 6

* Date: 2026-09-30
* Trigger: execute the completed iteration 6 storytelling review
* Branch: `main` at 94be6e5; no additional local or remote branch required combination

## Delta Covered

| Project change since iteration 5 | Deck treatment |
| --- | --- |
| Verified Git count is 42 non-merge commits through 27 Sep | Slide 3 source and slide 15 Git card |
| PRs 1 to 5 were merged by 28 Sep | Slide 15 distinguishes the later PR count from the 10 to 27 Sep research window |
| Exported citations on slides 4 to 12 lost opening or ending characters | Slides 3 to 13 use concise, explicitly left-aligned one- or two-line footers with at least 0.5-inch edge margins |

## Storytelling Review Decisions

Review: [storytelling-review-iteration-6.md](../research/subagents/storytelling-review-iteration-6.md)

| Finding | Decision | Reason |
| --- | --- | --- |
| SR6-01: Git commit count is stale | Accepted | Repository count is 42 non-merge commits through 27 Sep |
| SR6-02: merged pull-request count is stale | Accepted | Five PRs were merged by 28 Sep; the wording preserves the earlier research period |
| SR6-03: citation footers are clipped | Accepted and extended to slides 3 and 13 | The required slides and their neighbours showed the same export defect |

No findings were rejected. The deck remains 15 slides and the title period
remains 10 to 27 September 2026.

## Validation

| Check | Result |
| --- | --- |
| `build_deck.py` | 15 slides |
| `validate_deck.py` | 0 issues across 15 slides |
| Geometry validation | 0 issues across 15 slides |
| Slide images | Exported with `Export-SlideImages.ps1`; slides 3 to 13 and slide 15 inspected |
| Citation footers | Opening and ending text fully visible on slides 3 to 13 |
| Main notes | 1,967 words, about 14.1 minutes at 140 words per minute |
| Appendix notes | 153 words |

## Delivery

* Validated build:
  `slide-deck/ama-mentor-progress-review.pptx`
* Build SHA-256:
  `8F3CD9DDFAF47CB1E5738AFB7BE790E2D8A61CA70C87203D98066677D46A5F5D`
* Publish attempt: blocked because PowerPoint holds
  `docs/presentations/ama-mentor-progress-review.pptx` open.
* The lock file `docs/presentations/~$ama-mentor-progress-review.pptx` was not
  deleted or modified.
* Published SHA-256 remains:
  `D950070D0E8C1EC50951E33E5B412B6F12E02C5AF24D1272DFD45CE83F645343`
* The hashes are not identical because publication did not occur. Close the
  open presentation, then copy the validated build to the delivery path and
  verify the hashes.
