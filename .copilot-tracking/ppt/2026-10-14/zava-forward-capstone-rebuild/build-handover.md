---
title: Zava Forward native capstone build handover
ms.date: 2026-10-14
status: complete
task: capstone-native-rebuild-2026-10-14
phase: P01-T02
---
<!-- markdownlint-disable-file -->

# Validated working candidate — parent publication required

**Status: complete within builder ownership.** Exactly 22 refreshed slides,
18 main plus four optional appendices. No slide added or removed. No canonical
publication, source application change, cloud/model/auth operation, new agent,
dependency installation, staging, commit or push was performed. No uv was used.

## Delivery paths

All paths below are relative to:
`/home/azureuser/source/ama-wt-zava-challenge/.copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/`

| Deliverable | Path |
| --- | --- |
| Final working PPTX | `slide-deck/zava-forward-executive-draft.pptx` |
| Complete editable content | `content/global/style.yaml`; `content/slide-001/content.yaml` through `content/slide-022/content.yaml` |
| Safe slide-22 cleanup hook | `content/slide-022/content-extra.py` |
| Source copy and read-only extraction | `source/canonical-22-slides.pptx`; `source/extracted/` |
| Full fresh LibreOffice export | `slide-deck/validation/slides.pdf` — 22 pages |
| Individual fresh images | `slide-deck/validation/slide-001.jpg` through `slide-022.jpg` — 150dpi, 2000×1125 |
| Manageable contact sheets | `slide-deck/validation/contact-01-06.jpg`, `contact-07-12.jpg`, `contact-13-18.jpg`, `contact-19-22.jpg` |
| Actual relationship-bound notes | `reports/notes-association-22-rows.csv`; `reports/notes-association.json` |
| Actual native EMUs/fonts/peer rows | `reports/native-peer-geometry.json` |
| Actual rendered-word integrity | `reports/rendered-text-integrity.json` |
| Exact claim-presence/status checks | `reports/claim-oracle-checks.json` |
| Source/theme/hash integrity | `reports/provenance.json`; `reports/package-integrity.json` |
| Overall local checks | `reports/validation-summary.json` |
| Shared property checks | `slide-deck/validation/deck-validation-results.json`, `deck-validation-report.md`, 22 per-slide JSON files |
| Shared default geometry + dispositions | `slide-deck/validation/shared-geometry-results.json`, `shared-geometry-report.md`; `reports/shared-geometry-dispositions.json` |
| Actual image inspection | `reports/visual-inspection.md` |
| Execution and reproduction | `changes/build-execution.md`; `rebuild.sh`; `generate_content.py`; `validate_artifacts.py` |

## Provenance and exact checked bytes

* Canonical source at intake: `docs/capstone/deck/zava-forward-executive-draft.pptx`,
  **22 slides**, not the historical 21-slide copy.
* Source/source-copy SHA-256:
  `d089b54ff3d905c58020dfe26828d7786dac424ed4310a7547d082175f701d8e`.
* **Final working SHA-256:**
  `7b25fd7e77d1ed7d9aa908cf3da429bcfeae104beadea5ac90c1e97dbc71fbb4`.
* Final PPTX: 419,383 bytes.
* Authoritative strategist handover SHA-256:
  `700e76fc3558fca97b2cf27f73e4b4a6e57d1ff805883fa1a3dd3f67079043ed`.
* Source/candidate dimensions unchanged: **12,191,695 × 6,858,000 EMU**.
* Every source theme, master and layout part, including their relationships,
  is byte-identical in the candidate. Original logo retained. Palette:
  forest `173F35`, cream `F7F2E7`, moss `D5E2D4`, warm `E5B96A`.
* Canonical source hash remains unchanged after the build. Parent must copy
  these checked working bytes and verify the delivered hash; delivery
  equality is **not yet claimed**.

Documentation context cabe05c is distinguished from runtime source
cd14b3b379026a87ebfa3e9058ac10c0df7888eb. Slide 12/19/21 notes retain the
full adopted oracle: image05 digest e0254cb3…, serving revision12, deliberate
authorized reset, independent post-reset domain/content hashes and actual
restart proof, five separate actual GPT operator paths, five calls,
6884 tokens/15 ledger events, expired finite QA, ordinary assistant authority
absent/scans OFF, and outstanding human/staff/semantic/value gates.
Historical Decision 1 is explicitly separate. No new legal, budget,
currency-guarantee, pilot/production acceptance or outcome claim was added.

## Native/editability and alignment evidence

* Whole deck: **477 shapes**, including **311 nonempty native text frames**.
* Every nonempty text frame explicitly has **MSO_ANCHOR.TOP** and
  **MSO_AUTO_SIZE.NONE**; no vertical-centre or shrink-to-fit workaround.
* **56 peer text rows** measured: identical top, reserved height, insets and
  font setting across every row; **0 EMU peer drift**.
* **Zero text-frame pair intersections** and **zero out-of-bounds shapes**.
  Text on its own filled card and logo on white backing are intentional
  containment overlays, not collisions.
* Main slide titles: 32pt, except dense map title 30pt. Main peer body
  minimum 18pt, mostly 21–27pt; map titles/stages 17pt and map body 16pt.
  Source/footer/support labels are separately smaller, not hidden body text.
* Font is explicitly **Liberation Sans**, installed locally. Original Aptos
  was absent. This preserves the sans-serif treatment and avoids the
  unexpected local Aptos→monospace fallback. Original masters/themes remain
  untouched. Native PowerPoint font/fidelity acceptance remains human-owned.

### Slide 13 — fully native process map

**60 shapes:** 43 named textboxes, 12 native filled backgrounds, four native
directional connectors, **one explicitly named Zava branding picture**.
**Process-diagram pictures: 0.** No SVG, PNG/PDF diagram fragments, hidden text
substitute or flattened process picture is used on the slide.

All five capabilities, stages, human owners, request help, OFF trigger rows,
deterministic core, manual path, hazard and funding-to-cash boundaries are
extractable from native text. Actual notes contain the full text equivalent,
canonical IDs, source categories, registry purposes and synthetic predicates.
The five capability titles and all corresponding body regions share fixed
geometry. The rendered copy was shortened only to fit: `Trigger • OFF`
and `Assessor/coordinator`; the full approved meanings remain in notes.

| Map peer row | Actual top EMU | Actual height EMU | Font |
| --- | ---: | ---: | ---: |
| Stage | 1,554,480 | 374,904 | 17 |
| Owner | 2,066,543 | 630,936 | 16 |
| Capability title | 2,834,640 | 676,656 | 17 |
| Request label | 3,575,304 | 265,176 | 16 |
| Request body | 3,867,912 | 521,207 | 16 |
| OFF trigger label | 4,443,984 | 265,176 | 16 |
| OFF trigger body | 4,745,736 | 539,496 | 16 |

Each inset is **18,288 EMU** (0.02in). These are measured saved values,
including ≤1 EMU float-conversion truncation; peer equality is exact.
All 45 map semantic checks passed.

## Validation performed and repaired

1. Shared `build_deck.py --source <source-copy> --slides 1,…,22` preserves
   slide identities and themes. All 22 YAML slides rebuilt in place.
2. Fresh full-deck LibreOffice PDF and shared JPG export completed.
3. Shared `validate_deck.py`: **22 slides, zero issues**.
4. Actual slide→notes relationships: **22/22** topic/source sentinels and
   exact YAML note matches. Slide 13 correctly still resolves to
   `notesSlide22.xml`; slide 14 to `notesSlide13.xml`, etc.
5. Native geometry: all 311 text frames TOP/fixed; all 56 peer rows match;
   zero boundary violations/text-frame intersections; native map checks pass.
6. Actual PDF word tokens inside every corresponding native textbox bounds:
   **311/311 passed**, using 0.5pt tolerance. This is actual rendered text,
   not merely the XML/YAML text. It supplements image inspection.
7. Reviewed all 22 slides on four generated contact sheets and individual
   full-size images for dense/control/proof/cash/measurement/map/options
   slides. See inspection report; no remaining observed clipping, overlap,
   unreadable contrast or misaligned body starts.
8. First-render defects were fixed in source, followed by full fresh
   rebuilding/export: map OFF-label wrap, owner wrap, decision-panel body
   overflow, options header wrap, and retained source table on slide 22.
   A final rectangle check also removed slide 18's near-footer frame overlap.
9. The shared source-clear helper omits `graphicFrame` tables. The safe
   slide-22 hook removes retained source graphicFrames; replacements are
   fully native YAML text cells. No shared tool/source application was changed.

**Important honest warning:** the shared geometry checker at its generic
0.5in edge / 0.3in gap / 0.2in title-clearance thresholds returns nonzero:
**180 findings (154 warnings, 26 info), zero errors**. The original report is
retained, **not claimed as a clean pass**. Every finding has a disposition:
brand/footer edge bands, deliberate compact spacings and cross-column title
heuristics. The separate measured geometry, actual PDF text and image review
show no observed unresolved collision/clipping. Parent may review the
classified findings rather than treating generic dense-layout warnings as
180 independent content defects.

SDK/model vision validation was **not run** and is not claimed passed.
No PowerShell path that invokes environment setup was used.

## Reproduction commands

Run from the requested worktree:

```bash
cd /home/azureuser/source/ama-wt-zava-challenge
bash .copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/rebuild.sh
```

The script records the exact shared script paths, PYTHONPATH environment,
all-slide source rebuild, full export, shared notes/count checks, shared
default geometry and strict local reports. It does not publish. Original
extraction was:

```bash
export PYTHONPATH=/home/azureuser/.copilot/session-state/1e0d58ea-7ea9-4c65-93b7-66c89c481468/files/capstone-pptx-tools
python3 /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/experimental/powerpoint/scripts/extract_content.py \
  --input .copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/source/canonical-22-slides.pptx \
  --output-dir .copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/source/extracted \
  --resolve-themes
```

## Timing and remaining ownership

Planned main slides 1–18 total **795s (13:15)**, including the **110s recorded
public-repository-evidence walkthrough/recovery** on slide 12; recovery is
≤15s inside that allowance. Four optional appendices add no main-route time.
75s question +30s contingency yields 15:00. **This is not rehearsal evidence.**
No new demo execution, inference, login, verification/acceptance click or
private receipt playback was performed or scripted as observed.

No unresolved builder-blocking issue or clarification question remains.
Parent now owns final independent source/asset inspection, optional native
PowerPoint/font check, byte-identical canonical publication and README/index/
log/#68 updates. Staff/human/semantic/value acceptance, rehearsal/Q&A,
panel/Section-D evidence and legal currentness remain separate human gates.

## Parent Publication Validation

The parent copied the checked working bytes to the canonical path and verified
exact equality. After publication, the canonical file is intentionally no
longer the original source. The local validator therefore accepts an explicit
`--expected-canonical-sha` while always checking the archived source against
its recorded original hash. Its default still expects the pre-publication
source; no arbitrary changed canonical file is silently accepted.
`rebuild.sh` captures canonical bytes before regeneration and verifies they
stay unchanged. Post-publication checks use the exact checked delivery hash
`7b25fd7e77d1ed7d9aa908cf3da429bcfeae104beadea5ac90c1e97dbc71fbb4`.
The reports distinguish original-source preservation from intended canonical
delivery. The notes CSV uses LF line endings; metadata formatting changes do
not alter the inspected PPTX or rendered slide content.
