---
title: Cowork Presentation Outputs
description: Imported v1 and v2 presentation outputs, owner-selected public v2 scoring deck and verified local extraction
ms.date: 2026-10-24
ms.topic: reference
---

## Current Candidate

The [dated PR #438 corrections](./review-corrections-2026-10-24.md) now govern
current deployment labels, price claims and backup navigation. The current
PPTX/PDF are corrected; original Cowork handoffs and exports remain history.

The subsequent owner-requested cost recovery is now in pages 6, 11, 21, 32,
36 and 52 and their notes. The current native PDF has 54 pages; all 54 slides,
54 note parts and 27 Last Slide Viewed caller actions were retained. Use the
[build record and preview paths](../../../../.copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/changes/build-deck.md)
for this revision. It restores labelled inference and conditional funding
scenarios, not verified deployment pricing, full project TCO or issue #435
acceptance. Earlier price-review findings are preserved below and in the
dated correction record.

The owner selected Cowork v2 as the capstone presentation to score on
2026-10-23 and confirmed that these outputs are cleared for this public
repository despite their Microsoft Confidential marking. They remain drafts,
not an accepted assessment, observed rehearsal or approved operational product.

The owner subsequently supplied the [public v2 PPTX](../zava-forward-cowork-v2-draft.pptx).
It is the owner-designated current deck. Local verification with the scorer's
actual extractor found 54 slides and 54 speaker-note blocks and confirmed
the final slide-39 wording. The earlier protected source is retained below
in the handoff history only; its binary is not retained in this checkout.

The [IoT and optional-portal refinement](./refinement-2026-10-23/README.md)
now updates five slides and their notes at that same PPTX path. Use its
[new native PowerPoint PDF](../zava-forward-cowork-v2-draft.pdf) and five
native previews for the current revision. The import checks and original
hash below describe the supplied pre-refinement file, not today's revised bytes.

The [v2 handoff](./BUILD-HANDOFF-v2.md) describes 54 slides: 26 main-route
pages, a question index and 27 appendix answers. The
[v2 PDF](./Zava%20Forward%20v2%20-%20More%20homes%20ready%20with%20control%20intact.pdf)
and [contact sheet](./Zava%20Forward%20v2%20-%20contact%20sheet.png) are the
pre-refinement rendered reference. The v1 exports are historical, not an alternate
presentation for scoring.

## Imported Files

Retained generated binary outputs keep their original filenames and bytes. The v2
handoff has repository frontmatter and Markdown formatting adjustments;
its substantive content, including reported validation and save failures,
is retained. Cowork's validation claims are not independent local checks.

| File | Role |
| --- | --- |
| [BUILD-HANDOFF-v2.md](./BUILD-HANDOFF-v2.md) | Current v2 build report, forecast assumptions, limitations and outstanding decisions |
| [Original v2 PDF](./Zava%20Forward%20v2%20-%20More%20homes%20ready%20with%20control%20intact.pdf) | Historical pre-correction export; not the current presentation |
| [Original v2 contact sheet](./Zava%20Forward%20v2%20-%20contact%20sheet.png) | Historical pre-correction slide overview |
| Original v2 preview archive | Described in the handoff; not retained in this checkout. Use the five current native previews in the refinement record |
| Original protected PPTX | Described in the handoff; encrypted binary not retained in this checkout |
| [BUILD-HANDOFF.md](./BUILD-HANDOFF.md) | Historical v1 build report |
| Historical v1 PDF | Described in the handoff; not retained in this checkout |
| Historical v1 contact sheet | Described in the handoff; not retained in this checkout |
| Historical v1 preview archive | Described in the handoff; not retained in this checkout |
| [Statistics research](../../../reference/research/sector/uk-social-housing-retrofit-damp-stats-report.md) | Existing canonical report, byte-identical to Cowork's copy; not duplicated |

## Scoring Selection and Local Validation

The owner-designated current deck remains
`docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`. The
[artifact registry](../../../../.github/rubric/artifacts.json) selects this exact
path with a 20,000,000-byte allowance. The
[historical executive deck](../draft/zava-forward-executive-draft.pptx) and
nested protected-source copies are outside the selected path.
The later owner-supplied public export resolves the source encryption blocker.
The originally supplied PPTX was a CDFV2 encrypted container; that binary
is not retained here. The earlier executive deck is retained in `deck/draft/`
as historical evidence, not a second scoring candidate.

Original public-export checks, 2026-10-23 (before refinement):

* Readable OOXML ZIP with archive integrity verified
* 54 slides and 54 speaker-note blocks extracted by `prepare.extract_pptx_text`
* Slide 39 contains `Human task and comprehension validation: next milestone`,
  the final-save marker recorded in the v2 handoff
* Exactly one root PPTX matches the selected registry entry
* File size: 2,632,502 bytes
* SHA-256: `ebccfee35890332ca7aebd4f14f80141996747a4086c9ea03fda2dda5b53d860`

The PDFs parse as 46 pages for v1 and 54 for v2; the v2 PDF also contains
the final slide-39 marker. Both preview ZIPs pass member integrity checks,
with 46 and 54 images respectively. The PDF parser reports one ignored
invalid object pointer per PDF, so successful reading is not strict PDF
structural validation. Binary exports remain byte-identical to their sources.

The prepare suite reports 54 passed and one existing failure in the
deleted-file scoring fixture (`KeyError: 'total'`). That failure also
reproduces with the original HEAD implementation of `prepare.py`. All six
new deck-selection and size-boundary cases pass. No broader local publication
gate, independent acceptance review or hosted rubric run was performed.

These checks establish readable v2 evidence, not complete PDF/PPTX semantic
parity, note correctness, OneDrive service state or native-viewer fidelity.
The original save-retry report remains in the unaltered handoff history.

Before hosted scoring, complete the repository's publication gates. Scoring
uses trusted tools and registry from base `main`; the registry and
per-artifact size-limit change must reach that trusted base before a fresh
v2 score can use them.

Only the capstone deck receives a 20,000,000-byte allowance. Other artifact
types retain the existing 2,000,000-byte default; the PPTX decompression limit
is unchanged. No workflow dispatch, score-file edit, commit or push is part
of this import. Successful local extraction is not a hosted rubric pass.

## Remaining Review

Desktop PowerPoint, navigation, accessibility, rehearsal, source-currentness
and full capstone assessment remain separate gates. In particular, removing
cautious status words in v2 does not establish that a feature, forecast,
benefit or human-validation milestone has been accepted. Retain the source
report's national-versus-company, differing-base and pricing caveats.
