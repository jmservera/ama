<!-- markdownlint-disable-file -->
# Research: PR 1295 C3 coupled current navigation/currency defects (2026-11-09)

* Task: `pr-1295-c3-navigation-corrections` (parent `pr-1295-source-freshness`). Qualified `hve-core-all:rpi-agent`, Claude Sonnet 5.5, worktree `docs/demo-recovery-pr1295-1109`.
* Research disposition: executed (code read, regex impact simulated over every manifest note, baseline build reproduced).
* Planning Readiness: Ready.
* Correction budget: cycle 3 of 5 total (C1 and C2 spent, none reset; two remain after C3; no extension for an exhausted cohort is inferred).

## Identities (read at start)

| Item | SHA |
| --- | --- |
| Frozen start HEAD (clean) | `58229b8d30fc0019794ce4f98956beef6f0ea1e2` |
| Owner remote `origin/docs/capstone-cxo-story` (ls-remote) | `0bcf55da1d516c82567e6eb44357343054c69b76`, unchanged, ancestor of HEAD |
| `origin/main` (fresh fetch) | `f3532b02c01d7d21dadfe0d18f4f18b9f7502e07` (PR1272, tracking-only last commit) |
| Merge base | `b46a9ad9a9619db535368d1b2cbbddec8110e122`; HEAD 14 ahead, 5 behind |

`git merge-tree` dry run of main into HEAD is clean. The five main commits change no capstone, deck, pitch or tools/capstone path. Main does touch `docs/reference/README.md`, `docs/reference/log.md` and `docs/architecture/cutover-evidence-pack.md`, so main is merged before this cycle edits those files.

## Inputs read

* Coordinator brief, common brief, owner-reconcile/C1/C2 handoffs, `readiness-findings.json` (4 findings) and `functional-findings.json` (1 Medium). Original FAIL/adverse evidence is untouched.
* `tools/capstone/Invoke-Capstone.ps1` (`Update-RouteNote` 195-216, `Update-NavigationNote` 283, `Assert-CostSlide`, `Get-DeckRevision`, `Export-PitchMaterials`), `Test-DeckInsertion.ps1`, `Test-SourceHashes.ps1`, `docs/capstone/source/slides.json`, `validation.json`.

## Findings and classification

| ID | Evidence | Classification |
| --- | --- | --- |
| F1 readiness 4 + Functional Medium 1 (one defect) | `Update-RouteNote` shifts only `page|slide` followed by one space and one number. Missed forms in `slides.json`: `B13/page40, index/page27, S19/page22` (4035, no space), `index 27` (4758, 4802) and plural ranges `pages 23-24` (3029 QX and 4687 B20, with QX `1-22` and `25-26`). Native hyperlink destinations are fixed and unaffected. | Confirmed implementation defect; documentation symptom is generated pitch lines 339, 536, 770, 782 |
| F2 readiness 2 | `docs/architecture/README.md` 263-267 says the diagrams do not depict sensor ingestion; the same guide's lines 10-22, 54-57, 94-139, 152, 197-198 and 244 depict the source-coded chain. | Confirmed contradiction. The 14 October retained diagrams did omit it; the 8 November continuation does not |
| F3 readiness 1 | `docs/reference/README.md` 909 says all 54 slides/notes (current working set); 852 describes the current deck as 54-slide with baseline numbers (resident journey 13, Workbench/adoption 14-15, future 23-24). | Confirmed stale current rows. Line 204 is a dated 2026-10-29 historical statement and stays |
| F4 C2 routed item | `text-equivalent.md` R09 anchors `#L21/#L241/#L315`; headings now at 33 (`## Purpose and Method`), 253 (`## Contractor and Resident Coordination Agent`), 327 (`## Quality Verification Agent`) and match the generator anchors in `build-resident-journey.mjs` 23-25. | Confirmed; no check detects it |
| F5 readiness 3 | Hosted CONFLICTING at old owner head `0bcf55da1`. | Not a local defect, not an old-head CI requirement; stays with coordinator |

## Regex impact (simulated, then to be proven in PowerShell)

Python simulation of one explicit mapping (`13..54` to `+1`, other values unchanged) over every non-part55 manifest note differs from the current output in exactly five notes: QX (`1-22`, `23-24`, `25-26` to `1-23`, `24-25`, `26-27`), B13 (`page40`, `index/page27`, `S19/page22` to `41`, `28`, `23`), B20 (`pages 23-24` to `24-25`), B26 and B27 (`index 27` to `28`). All other notes are byte-equal to current. Slides 13..54 baseline `page N` forms already shifted once; no double shift is introduced because the new pattern is a single pass.

## Authorization boundary

* Notes are generated from `slides.json` through the existing owner-authorized navigation transformation; no `slides.json`, protected financial slide XML or visible slide text changes. Only the five notes above change. The pitch speaker script (main route, pages 1-27) has no changed note; the question bank carries the B13/B20/B26/B27 changes.
* Protected cost parts 6/11/21/32/36/52 use `Assert-CostSlide`, which calls the same transformation, so the assertion stays consistent. Their notes contain none of the affected forms.
* No new protected-financial edit, native rewrite or visible-label change is needed. Nothing is frozen for an owner decision. The pre-existing open owner decision on the C1 boundary notch is unchanged.

## Baseline reproduction (scratch `/tmp/ama-pr1295-c3`)

* `Invoke-Capstone.ps1 -Action Build` with isolated pwsh 7.6.9 exits 0; candidate SHA-256 `343d133a...cbb1a` equals the delivered PPTX and both generated pitch files are byte-equal. Build is deterministic here, so a changed candidate hash after the fix is attributable to the fix.
* Delivered PDF `b8ec7712...03d27`; `slides.json` `705875492c...400cd`; builder `01afb6e3...fcafc7` (will change by design).

## Not in scope

Historical dated evidence, TIMING lines, monetary figures, line 204 of the index, owner/C1/C2 packages and logs, native PowerPoint, AT, projector, rehearsal and live acceptance, price research, cloud or model actions.

## Planning inputs

One mapping function; table-driven literal tests in `Test-DeckInsertion.ps1`; package diff against the pre-change build proving only five note parts change; regenerate pitch, receipt and delivered files from tool output; qualified doc edits; one merge of main first.
