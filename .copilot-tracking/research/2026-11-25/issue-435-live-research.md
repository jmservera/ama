---
title: Research for issue 435 tokenomics slide (live 2026-11-25)
ms.date: 2026-11-25
---

## Scope

Owner decision 2026-11-25: add the Tokenomics slide to the capstone deck from the docs/capstone/pitch material and commit the deck change. Synthetic demo, desktop only. No Azure change is needed; none is made.

Research disposition: executed (repository reading only). Planning Readiness: Ready.

## Findings

* The delivered deck is `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`, 55 slides, 13.33 x 7.5 in. Slide 22 (S18) carries a modelled USD 0.44 per home scenario; B25 (page 53) and B27 (page 55) are Q&A cards. No slide states the Tokenomics unit or the measured batch.
* Pitch material read 2026-11-25: `pitch/tokenomics-placement-draft.md`, `pitch/tokenomics-model-tier-comparison.md`, `tokenomics-qa-brief.md`, `pitch/tokenomics-rehearsal-notes.md`. Unit: total attributable cost divided by human-accepted proposals above an agreed quality floor. Measured batch (#432, 2026-11-18, synthetic): 12 proposals, 2,522 tokens, 180 to 225 per proposal, usage only. Earlier observation: 6,884 tokens over five runs, no human acceptance. No price, saving or payback may be claimed (criterion 6).
* Build tooling: `tools/capstone/Invoke-Capstone.ps1` needs PowerShell, which is not installed. The builder supports one declared insertion (S11A) only, so a rebuild from `slides.json` is not possible here.
* Inserting mid-route would shift pages, and many notes and labels cite fixed page numbers. The least risky placement is a new appendix card B28 appended as page 56, with its topic button jumping to S18.
* `python-pptx` 1.0.2 and LibreOffice are installed, so a direct package edit and a render check are possible.
* `gh issue view` was rate limited; the issue body was read with `gh api`. Unticked criteria: 1 (placement and rebuild), 2 (mentor), 4 (batch decision).

## Acceptance criteria

See the per-criterion table in the changes record.
