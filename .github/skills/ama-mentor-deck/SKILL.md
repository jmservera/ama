---
name: ama-mentor-deck
description: "Create or update the AMA mentor progress review deck from the knowledge-base log, memory and project documents, challenge it with the Presentation Communications Strategist agent, validate it from generated assets, and publish it to docs/presentations. Use when asked to create, refresh, review or republish the mentor presentation or another AMA progress deck."
---

# AMA Mentor Deck

## Goal

Keep the mentor progress review deck true to the latest project state. Each run produces a validated PPTX in `docs/presentations/`, an independent storytelling review, and records that let the next run start from where this one stopped.

The deck is built with the hve-core `powerpoint` skill. Load that skill for the content YAML schema, the build and validation scripts and their options. This skill adds the project workflow around it.

## Inputs

* `deck`: the deck working root. The default is the most recent `.copilot-tracking/ppt/{YYYY-MM-DD}/ama-mentor-progress-review/`. Create a new dated root only when the owner asks for a new deck.
* `since`: the date or iteration of the previous deck run. The default is the latest `changes/build-validate-iteration-N.md` in the deck root.
* `notesBudget`: the main speaker-notes budget. The default is about 2,000 words, roughly 14 minutes at 140 words per minute.

## Flow

1. Sync the branch. Run `git status`, `git log --oneline -15` and `git branch -a`. If another branch holds newer log, BRD, addendum or deck work, ask the owner how to combine them before editing anything. Do not merge, rebase or push without that answer.
2. Build the delta. Read `docs/reference/log.md` entries after `since`, `docs/reference/memory.md`, and the deck's `research/primary-research.md` and latest `changes/` record. List what changed in the project that the deck does not yet show. Open only the source documents the delta names.
3. Read the current deck from its generated assets, not the PPTX. Run `python .github/skills/ama-mentor-deck/scripts/deck_yaml.py text --content-dir <deck>/content` for the slide text and notes word counts. View the exported `slide-deck/validation/slide-NNN.jpg` images.
4. Verify every figure the deck states against its source before keeping or changing it. Take commit counts from `git rev-list --count --no-merges HEAD` and `git log --oneline -- <file>`, and take dates, versions and identifiers from the documents themselves. Keep evidence classes visible: case fact, sector-informed hypothesis, proposal, estimate or unknown.
5. Edit the content YAML. Use the `deck_yaml.py` helpers for scripted edits, and `deck_yaml.py insert --at N` to open a slot for a new slide. Follow the voice guide: first person, action titles of about 65 characters or fewer, visible evidence classes, ASCII punctuation, no em dashes, British spelling, and notes that carry the story while slides carry the evidence. Take colours, fonts and layout from `content/global/style.yaml` and the existing slides.
6. Build, validate and export using the powerpoint skill's `build_deck.py`, `validate_deck.py` and `validate_geometry.py`. Write validator output to the file names already in `slide-deck/validation/`: `deck-validation-results.json`, `deck-validation-report.md`, `geometry-results.json` and `geometry-report.md`. Then run `.github/skills/ama-mentor-deck/scripts/Export-SlideImages.ps1 -PptxPath <pptx> -OutputDir <deck>/slide-deck/validation` and view every changed slide image. Fix any issue and repeat until both validators report 0 issues.
7. Challenge the deck. Dispatch the `Presentation Communications Strategist` agent with the text dump, the slide images, its previous review in `research/subagents/`, `primary-research.md`, the source documents for fact checks, the audience, the voice guide and the notes budget. Ask it to write `research/subagents/storytelling-review-iteration-N.md` with findings that each carry a slide, a severity, an exact proposed change and its evidence, and not to open the PPTX or edit other files.
8. Decide each finding. Verify it against the cited slide and source, then accept it or reject it with a reason. Apply accepted findings as one batch, bring the main notes within `notesBudget`, and repeat step 6.
9. Publish. Copy `slide-deck/<deck-name>.pptx` to `docs/presentations/<deck-name>.pptx`, replacing the previous copy, and confirm both files have the same SHA-256 hash.
10. Record the run:
    * Write `changes/build-validate-iteration-N.md` with the delta, edits, review decisions, validation results and hash.
    * Update `research/primary-research.md` for the storyline and any new evidence.
    * Update the deck row in `docs/reference/README.md`.
    * Append a dated entry to `docs/reference/log.md`, and flag any contradiction the run found rather than silently resolving it.
11. Do not commit unless the owner asks. Report the delta covered, the slides changed, the accepted and rejected review findings, the validation results, the delivery path and anything left open.

## Stop Rules

* Ask before combining branches, before a structural change (adding, removing, merging or reordering slides) that the owner has not requested, and whenever a figure cannot be verified from the repository.
* Stop without publishing if either validator reports issues that cannot be fixed within the deck YAML.
* Treat the strategist's review as advice. The review cannot change sources, override evidence labels or add facts that the repository does not support.

## Success Criteria

* Every project change in the delta is shown on a slide or deliberately left out, with the reason recorded.
* Both validators report 0 issues, every changed slide image has been viewed, and main notes are within `notesBudget`.
* The delivery copy in `docs/presentations/` matches the validated build by hash.
* The change record, primary research, index row and log entry describe the same run.

## References

* [scripts/deck_yaml.py](scripts/deck_yaml.py): `text` prints slide text and notes word counts; `insert` opens a slide slot; importable helpers load, edit and save slide YAML.
* [scripts/Export-SlideImages.ps1](scripts/Export-SlideImages.ps1): exports slide JPGs through PowerPoint on Windows when LibreOffice is unavailable.
