<!-- markdownlint-disable-file -->
# HVE Builder evidence: ama-mentor-deck skill

* Date: 2026-09-27
* Active modes: create, improve, refactor
* Approved write boundary: `.github/skills/ama-mentor-deck/` and one pointer in `.github/copilot-instructions.md`
* Artifact type decision: skill. The workflow recurs and needs scripts, but it is needed only when the owner asks for deck work, so on-demand loading fits better than always-on instructions. The always-on instructions keep the `docs/presentations/` delivery rule and a pointer to the skill.

## Candidate

* `SKILL.md`: goal, inputs, 11-step flow, stop rules, success criteria, references
* `scripts/deck_yaml.py`: `text` and `insert` commands plus importable helpers; exercised on the live deck (15 slides, notes word counts reported)
* `scripts/Export-SlideImages.ps1`: exported 15 slide images through PowerPoint COM during iteration 4

## Mechanical validation

| Check | Result |
|---|---|
| Frontmatter `name` matches the folder, and `description` states what and when | Pass |
| Relative links in References resolve | Pass |
| Scripts run on the target deck | Pass |

## Review pass (self-review against the review rubric)

| Dimension | Verdict | Note |
|---|---|---|
| Architecture fit | Pass | Reuses the hve-core powerpoint skill and the existing strategist agent rather than copying them |
| Outcome and structure | Pass | Goal, success criteria and stop rules are explicit |
| Emphasis calibration | Pass | Asks are tied to specific triggers: branch combination, structural change, unverifiable figure |
| Load-timing placement | Pass | The always-on surface gains one sentence |
| Reference discipline | Pass | The powerpoint schema and script options are referenced, not restated |
| Skill packaging | Pass | The body is compact, and each script's intended use is stated |

One correction was applied during review. The first draft pointed to a voice guide in `research/primary-research.md`, but that file has no voice guide, so the guide is now stated in step 5.

* Verdict: Pass
* Outcome: Pass
