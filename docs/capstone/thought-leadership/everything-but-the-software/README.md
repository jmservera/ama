---
title: Everything but the Software - source package
description: Completed exploratory findings, measurement lessons and publication checklist with preserved historical evidence
ms.date: 2026-11-26
---

Working title: *Everything but the Software: Stable Retention, Missing Features and the Cost of Consolidation. An Exploratory Case Study and Experiment.*

## Final editorial pass, 26 November

The [revision record](./anc/revision-report.md#final-editorial-pass-26-november)
contains the change log, three title options, before/after metrics and author
confirmations. The [complete numeric audit](./anc/editorial-audit-2026-11-26.json)
preserves both extracted lists and explains every sequence difference.
Sections 1--9 now contain 12,246 approximate words by the existing checker;
Section 7 contains 4,979. The interval correction is the only change to
numerical table cells.

The delivered [PDF](./main.pdf) includes the additive Supplement. Historical
reviews and source pins are unchanged. Both repositories are public; both
OSF registrations exist, with their actual public release still requiring
author confirmation. Employer clearance also needs confirmation.

To repeat the numeric and prose measurements against the saved intake:

```bash
python3 anc/editorial_audit.py \
  --baseline-json anc/editorial-audit-2026-11-26.json \
  --output /tmp/paper-editorial-audit-new.json
```

Choose a new output file. This command measures the current sources without
rewriting the saved baseline or assigning editorial explanations to later edits.

## Review-comment cleanup 26 November

The owner requested removal of the eight review-comment blocks after the
voice revision. All 40 comment lines were removed; every other manuscript
byte is unchanged. Earlier revision records retain the feedback dispositions.
`review_annotation_cleanup` binds the cleaned source without replacing
historical hashes or PDFs.

## Marked author-voice revision 26 November

The eight marked examples were revised first, then the lessons were captured
in [ama-author-voice](../../../../.github/skills/ama-author-voice/SKILL.md) and
connected to the scientific-writing agent. The same reader-context and
storytelling checks were applied across all 71 headed sections and eight
active TeX sources. Five sources changed; the original annotations remain
as comments and no longer render as prose.

The [marked-passage dispositions and validation record](./anc/revision-report.md#marked-author-voice-revision-26-november)
describe the product context, simpler explanations and narrative changes.
Scientific results, equations, numerical tables, source records and literal
prompts are preserved. All 88 selected authoring tests pass. ChkTeX,
structure, skill frontmatter and link checks pass; existing lint findings
and the browser-dependent diagram-regeneration exclusion remain documented.

A separate 75-page preview compiles without warnings and passes all-page
content and geometry checks. `author_context_revision` binds the revised
sources and preview. The delivered PDF is untouched. No independent
scientific, human or publication approval is implied.

## Unsupported-claim revision 26 November

The second pass reviewed all eight active TeX sources for claims without
an example, number or source. It adds named recommendations and case-record
locators, and cuts unsupported schedule, duration and cost assertions.
Participant accounts, observed results and proposed follow-ups remain distinct.
The [claim dispositions](./anc/revision-report.md#unsupported-claim-revision-26-november)
record the source passages and verification limits.

All 88 selected authoring checks pass; the unchanged native-diagram exporter
remains excluded because its browser is unavailable. The separate 75-page
PDF preview compiles without warnings and passes all-page content and geometry
checks. Numerical results, equations, prompts, bibliography and figures are
preserved. `unsupported_claims_revision` binds the sources and preview.
The owner approved keeping a concurrently committed delivered PDF; this
revision does not claim that file matches the final sources. No publication
or independent scientific approval is implied.

## Concrete-example revision 25 November

The owner authorized a whole-paper revision of generic claims, including all
seven active TeX inputs. The review covered 71 headed sections, including
starred sections. General explanations now use the recorded sign-in failure,
staff binding, prototype approval, ranking-test and read-only-view examples.
Literature passages name the inspected procedures and trials; proposed
mechanisms and future work remain proposals.

The [claim-to-example record](./anc/revision-report.md#concrete-example-revision-25-november)
identifies the sources, verification limits and checks. All 88 selected
authoring regressions pass. Native-diagram regeneration remains blocked by
its missing browser; the diagram sources and exports are unchanged.
A separate 75-page PDF preview compiles without warnings. The delivered
`main.pdf`, numerical results, equations, bibliography and literal prompts
are unchanged. `generic_claims_revision` binds the revised sources and preview
without replacing historical records or implying publication approval.

## Publication revision 24 November

The owner selected the completed experiment as the evidence base for this
paper and deferred further experimental rounds to a deeper study. The
revision preserves the original scores, thresholds, intervals, source pins
and unknowns. It adds descriptive reporting from the existing public exports:

* The realized D controls average 96.9629% final coverage. Even perfect B
  outcomes could improve on them by only 3.0371 percentage points. The
  original ten-point target remains unmet.
* All 6,300 retained F/P rows have complete observation and risk-history
  flags. Seven failing contract-checkpoints describe one persistent
  Gemini E-07 episode; rejected edits fall outside this endpoint.
* The CR1 prerequisite table separates repositories with both F9 and F10
  complete from those with a different preservation burden. Its strata
  describe post-treatment states. The two GPT outcomes remain unknown.
* The 55 held attempt charges vary across models and arms. Fully billed
  subset means retain their denominators; all-allocation payback remains
  unresolved.

The article now treats its intervals as conditional exploratory summaries.
The source chronology and exposure record cannot establish independent
provider conditions or outcome-blind amendments. The earlier 313/315
judging frame and incomplete AI-assisted calibration remain explicit.
No new candidate, evaluator or judge outcome was collected.

The [publication checklist](./anc/revision-report.md#publication-revision-and-disposition-24-november)
tracks all 24 review items, including final author and employer approvals.
Earlier dated sections below preserve their own validation results and
delivery scope.

The [historical coordinator recovery](./anc/revision-report.md#historical-coordinator-evidence)
adds source-located steering and launch prescriptions. Scheduled messages
dominate the retained history; its row counts cannot supply intervention
rates. Actual historical runtime identities and paired release/journey
observations remain unavailable.

The revised 73-page PDF includes the Supplement from page 45. Two-pass
PDFLaTeX compilation and all-page geometry/reference checks pass. Of 75
authoring checks, 74 pass; the unchanged native diagram exporter reaches
rendering but rejects five arm feature labels for text overflow on this
host. Committed diagram/export bindings pass. The
[validation record](./anc/revision-report.md#publication-validation-and-delivery)
separates that unresolved regeneration check from the successful PDF build.

### arXiv preparation

The following official guidance was checked on 24 November 2026:
[submission guidelines](https://info.arxiv.org/help/submit/index.html),
[TeX submissions](https://info.arxiv.org/help/submit_tex.html),
[moderation and generative-AI policy](https://info.arxiv.org/help/moderation/index.html)
and [content types](https://info.arxiv.org/help/policies/content-types.html).
The returned TeX and submission pages were truncated after the relevant
format/preparation sections; those sections and the full relevant content-type
and AI-policy passages were inspected. Initial guessed policy endpoints
returned 404 and were replaced with the canonical links above.

The [31 October 2025 CS notice](https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/comment-page-1/)
requires successful prior peer review for review/position papers; the notice
was corroborated through indexed official text in this pass. This manuscript
reports original exploratory empirical work. Its completed findings should
remain clear to readers and moderators. Do not recategorize it to bypass
a content-type restriction.

Prepare the submission from the final approved [article source](./main.tex),
its seven active TeX inputs, three literal prompt inputs and eleven referenced
PNG figures. Compile from the bundle root with PDFLaTeX and shell escape
disabled. The embedded bibliography supplies the references; this build
does not invoke BibTeX. Exclude generated PDFs, logs, auxiliary files,
review correspondence, raw workspaces and private mappings. Preserve those
records in their existing evidence locations.

A compilation-only archive of these 22 inputs was prepared and compiled
after extraction into a separate directory. Its 73-page output matches the
delivered PDF's extracted text on every page. The
[publication binding](./anc/supplement-integration.json) records the archive
digest and scope. Ancillary evidence stays in this repository package.
This preparation is separate from selecting approved public-release files.

Use the approved title and author spellings from the article, and copy its
final abstract into the metadata field. The current abstract is 1,802 source
characters, below arXiv's 1,920-character limit; check the actual metadata
field again at submission. Select a subject category only after checking
its scope (cs.SE is a candidate), choose the license with both authors,
and obtain any required endorsement. Set the real submission date at that
point. Inspect the PDF generated by arXiv before completing submission.
Local compilation does not exercise that service.

Employer clearance (maturing 29 November 2026 if CELA sends no further notice
under the manager-confirmed 14-day review window, provided the 14 November
submission covers this 24 November draft) and final confirmation that both
authors' sign-off covers the exact uploaded bytes remain human actions. The
sanitized study deposit is published on `jmservera/ama-thought-mve` as release
`results-exploratory-s1-v1`, while the pre-collection OSF registrations remain
linked to that repository without a post-collection OSF deposit. The existing
AI disclosure records substantial assistance and author responsibility.
Nothing in this revision authorizes arXiv upload or submission.

### Local packaging and GitHub Release

Run [anc/package_arxiv.py](./anc/package_arxiv.py) locally with Python 3.11+
and PDFLaTeX, including the TeX Live packages imported by
[main.tex](./main.tex). It uses the Python standard library and adds no
GitHub Action. From the repository root:

```bash
python3 docs/capstone/thought-leadership/everything-but-the-software/anc/package_arxiv.py \
  --output /tmp/ama-arxiv-preview-2026-11-25
```

Choose a new output directory for each run. The script follows literal
root-relative `\input`, `\include`, `\includegraphics` and `\lstinputlisting`
references and rejects missing or unsafe paths.
Inside the submission only, it moves compilation inputs from `anc/` to
`tex-inputs/` and rewrites their literal TeX file arguments. Repository
sources, prompt contents and images stay unchanged. arXiv
[reserves root-level `anc/` for ancillary files](https://info.arxiv.org/help/ancillary_files.html)
and does not accept TeX inputs there; local PDFLaTeX alone does not detect
that restriction.
It writes `everything-but-the-software-arxiv.zip`, the equivalent `.tar.gz`,
and `SHA256SUMS`. Both archives open directly to `main.tex` and its inputs,
without an enclosing directory. The script extracts the ZIP and compiles
it with shell escape disabled, using at least two passes and up to four
while references settle. Compilation failures, unresolved references or
references still changing after four passes stop packaging.

The local `main.pdf` is a fresh preview, not a submission or release asset.
The archives exclude existing PDFs, logs, auxiliary files, unused images,
editable diagrams, reviews, scripts and unrelated ancillary evidence. The
three prompt text files remain because the article typesets them. The
bibliography is embedded in the TeX source, so `references.bib` is not needed.
This tool supports this paper's literal file references, not arbitrary
TeX macro-generated dependencies or a general bibliography build pipeline.

After both authors approve the exact paper, employer clearance is satisfied
and the applicable repository publication gates pass, use authenticated
GitHub CLI (`gh auth login`) and a clean, committed checkout to publish:

```bash
python3 docs/capstone/thought-leadership/everything-but-the-software/anc/package_arxiv.py \
  --output "$HOME/arxiv-packages/paper-source-v1" \
  --publish --tag paper-source-v1
```

Keep publication output outside the checkout so it does not dirty the
worktree. `--publish` and `--tag` are required together. The command creates
a new tag at the exact local HEAD in `jmservera/ama`, whose commit must
already exist there, and uploads both archives and their checksum file to
a draft release before publishing it. It does not mark the paper as the
repository's latest software release. Every packaged input must match its
committed blob; the script rechecks the revision after compilation. It
never pushes a branch or overwrites an existing tag or release. The Git
checks compare the original inputs; archive-only path rewrites happen
after that source check.

If tag creation or upload fails, the command exits nonzero. Inspect the
repository's tags and releases before retrying: a new tag or draft can
remain. Recovery is manual; the script does not delete remote records.
An interrupted publish request may have completed remotely, so inspect
the release rather than assuming it is still a draft.

Upload either source archive, not both, through arXiv's submission page.
If replacing an earlier bundle containing `anc/`, use arXiv's Delete All
control on the upload page first, then upload the corrected archive. Its
compilation inputs should appear under `tex-inputs/`, not as ancillary files.
Select PDFLaTeX and `main.tex`, then inspect arXiv's generated PDF.
Packaging and a GitHub Release do not submit the article, grant clearance
or establish arXiv acceptance. The format guidance above was rechecked on
25 November 2026 against the official submission and TeX preparation pages.

Run the packaging regressions without network access:

```bash
python3 -m unittest discover \
  -s docs/capstone/thought-leadership/everything-but-the-software/anc \
  -p test_package_arxiv.py -v
```

## Scientific author-voice revision 24 November

The revision reviews all 70 active sections across the article and seven
TeX inputs against the completed experiment report and the owner's three
English blog samples. It rewrites the abstract and opening, removes repeated
explanations and states the results without treating the original decay
conjecture as confirmed. First-person case observations remain distinct from
the experiment's methods and findings.

The numerical table values, seven equations, literal prompts, bibliography
and source identifiers are unchanged. The prediction summary now attributes
the Sonnet/Gemini coverage range to all arms, qualifies CR1 cost savings as
inconsistent and separates structural treatment fidelity from the untested
hybrid proposal. The draft date is 24 November; it is not a submission date.

The [revision record](./anc/revision-report.md#scientific-author-voice-revision-24-november)
records the evidence check and validation. `scientific_voice_revision` binds
the current sources without rewriting earlier source/PDF records. The existing
PDF remains unchanged; a separate build validates the revised source.
Final author approval, publication clearance and arXiv submission remain
outstanding.

## Publication revision 24 November

The owner selected the completed experiment as the evidence base for this
paper and deferred further experimental rounds to a deeper study. The
revision preserves the original scores, thresholds, intervals, source pins
and unknowns. It adds descriptive reporting from the existing public exports:

* The realized D controls average 96.9629% final coverage. Even perfect B
  outcomes could improve on them by only 3.0371 percentage points. The
  original ten-point target remains unmet.
* All 6,300 retained F/P rows have complete observation and risk-history
  flags. Seven failing contract-checkpoints describe one persistent
  Gemini E-07 episode; rejected edits fall outside this endpoint.
* The CR1 prerequisite table separates repositories with both F9 and F10
  complete from those with a different preservation burden. Its strata
  describe post-treatment states. The two GPT outcomes remain unknown.
* The 55 held attempt charges vary across models and arms. Fully billed
  subset means retain their denominators; all-allocation payback remains
  unresolved.

The article now treats its intervals as conditional exploratory summaries.
The source chronology and exposure record cannot establish independent
provider conditions or outcome-blind amendments. The earlier 313/315
judging frame and incomplete AI-assisted calibration remain explicit.
No new candidate, evaluator or judge outcome was collected.

The [publication checklist](./anc/revision-report.md#publication-revision-and-disposition-24-november)
tracks all 24 review items, including final author and employer approvals.
Earlier dated sections below preserve their own validation results and
delivery scope.

The [historical coordinator recovery](./anc/revision-report.md#historical-coordinator-evidence)
adds source-located steering and launch prescriptions. Scheduled messages
dominate the retained history; its row counts cannot supply intervention
rates. Actual historical runtime identities and paired release/journey
observations remain unavailable.

The revised 74-page PDF includes the Supplement from page 46. Two-pass
PDFLaTeX compilation and all-page geometry/reference checks pass. Of 75
authoring checks, 74 pass; the unchanged native diagram exporter reaches
rendering but rejects five arm feature labels for text overflow on this
host. Committed diagram/export bindings pass. The
[validation record](./anc/revision-report.md#publication-validation-and-delivery)
separates that unresolved regeneration check from the successful PDF build.

### arXiv preparation

The following official guidance was checked on 24 November 2026:
[submission guidelines](https://info.arxiv.org/help/submit/index.html),
[TeX submissions](https://info.arxiv.org/help/submit_tex.html),
[moderation and generative-AI policy](https://info.arxiv.org/help/moderation/index.html)
and [content types](https://info.arxiv.org/help/policies/content-types.html).
The returned TeX and submission pages were truncated after the relevant
format/preparation sections; those sections and the full relevant content-type
and AI-policy passages were inspected. Initial guessed policy endpoints
returned 404 and were replaced with the canonical links above.

The [31 October 2025 CS notice](https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/comment-page-1/)
requires successful prior peer review for review/position papers; the notice
was corroborated through indexed official text in this pass. This manuscript
reports original exploratory empirical work. Its completed findings should
remain clear to readers and moderators. Do not recategorize it to bypass
a content-type restriction.

Prepare the submission from the final approved [article source](./main.tex),
its seven active TeX inputs, three literal prompt inputs and eleven referenced
PNG figures. Compile from the bundle root with PDFLaTeX and shell escape
disabled. The embedded bibliography supplies the references; this build
does not invoke BibTeX. Exclude generated PDFs, logs, auxiliary files,
review correspondence, raw workspaces and private mappings. Preserve those
records in their existing evidence locations.

A compilation-only archive of these 22 inputs was prepared and compiled
after extraction into a separate directory. Its 74-page output matches the
delivered PDF's extracted text on every page. The
[publication binding](./anc/supplement-integration.json) records the archive
digest and scope. Ancillary evidence stays in this repository package.
This preparation is separate from selecting approved public-release files.

Use the approved title and author spellings from the article, and copy its
final abstract into the metadata field. The current abstract is 1,802 source
characters, below arXiv's 1,920-character limit; check the actual metadata
field again at submission. Select a subject category only after checking
its scope (cs.SE is a candidate), choose the license with both authors,
and obtain any required endorsement. Set the real submission date at that
point. Inspect the PDF generated by arXiv before completing submission.
Local compilation does not exercise that service.

Employer clearance (maturing 29 November 2026 if CELA sends no further notice
under the manager-confirmed 14-day review window, provided the 14 November
submission covers this 24 November draft), final confirmation that both
authors' sign-off covers the exact uploaded bytes, and the approved
public-deposit/registration correspondence remain human actions. The existing
AI disclosure records substantial assistance and author responsibility.
Nothing in this revision authorizes upload or submission.

## Scientific author-voice revision 24 November

The revision reviews all 70 active sections across the article and seven
TeX inputs against the completed experiment report and the owner's three
English blog samples. It rewrites the abstract and opening, removes repeated
explanations and states the results without treating the original decay
conjecture as confirmed. First-person case observations remain distinct from
the experiment's methods and findings.

The numerical table values, seven equations, literal prompts, bibliography
and source identifiers are unchanged. The prediction summary now attributes
the Sonnet/Gemini coverage range to all arms, qualifies CR1 cost savings as
inconsistent and separates structural treatment fidelity from the untested
hybrid proposal. The draft date is 24 November; it is not a submission date.

The [revision record](./anc/revision-report.md#scientific-author-voice-revision-24-november)
records the evidence check and validation. `scientific_voice_revision` binds
the current sources without rewriting earlier source/PDF records. The existing
PDF remains unchanged; a separate build validates the revised source.
Final author approval, publication clearance and arXiv submission remain
outstanding.

## Copy Review Recommendations 16 November

The five approved copy-review recommendations are applied to the article
and two active ancillary inputs. They narrow an untested-procedure claim
to this study, identify historical reporting requirements before presenting
them, attribute supplied registration/runtime information in the author's
first person, clarify what provenance links verify and describe the observed
Gemini CR1 comparison without winner language.

The [revision record](./anc/revision-report.md#copy-review-recommendations-16-november)
preserves the original findings and evidence limits. `copy_review_revision`
binds all eight active sources and retains the preceding active Supplement
content digest. Earlier dated bindings are unchanged. Structural checks and
73 of 74 package tests pass; the unchanged diagram exporter cannot import
`esbuild`. No TeX compiler is available on PATH. The existing PDF is unchanged,
and no new layout review, scientific verification or final approval is claimed.

## Conservative Prose Follow-Up 16 November

The follow-up includes the owner's staged abstract revision and checks the
article plus all seven active ancillary TeX inputs. The existing prose
needs only small changes: simpler wording in the article and a shorter
sentence in the Supplement introduction. Scientific terms, qualified claims
and first-person case narration are retained; the two inactive inputs are
unchanged.

Independent review also found an inherited bound error in the abstract:
the methods and results support complexity at most ten, not below ten.
The abstract now matches that bound; no observations changed.

The [revision record](./anc/revision-report.md#conservative-prose-follow-up-16-november)
records the checks, and `prose_polish_revision` adds current source digests
without changing earlier bindings. Structural checks pass; 73 of 74 package
tests pass. The unchanged diagram-export test cannot load `esbuild`.
No TeX compiler is available on PATH, so no fresh PDF or layout review is
claimed. The existing `main.pdf` is byte-for-byte unchanged.

## Human Readability Source Revision 16 November

I rewrote the [article source](./main.tex) and all seven active ancillary TeX
inputs in plain language for computer scientists and data scientists using
LLMs in the SDLC. The pass covered all 70 sections and subsections, back
matter and Supplement included. Contracts, acquisition, retention, risk sets,
estimands, bootstrap intervals and ordinal ratings are now explained next to
where they are used. The two inactive historical inputs are unchanged.

The [revision record](./anc/revision-report.md#human-readability-revision-16-november)
gives the scope and checks. The revision preserves all seven displayed
equations, 40 table environments, three literal prompts, citation sequences,
the bibliography, 61 source-register bindings and the author TODOs.
The [binding](./anc/supplement-integration.json) adds
`human_readability_revision` and leaves earlier source/PDF records in place.

Only the source changed. The owner asked me to leave the existing
`main.pdf` untouched and uncommitted. That file changed outside this
revision's external build, so I could not verify its preservation.
A separate validation PDF has 73 pages, with the Supplement starting on
page 46 and the source register on page 70. All pages are nonblank, text
stays within page bounds, references resolve, and I inspected seven selected
renders. Tectonic reports only the inherited `inputenc` warning.
Structural checks and 73 of 74 package tests pass. The native diagram
exporter needs a Playwright browser that is unavailable, so I claim no
exporter pass. Earlier page counts and delivery descriptions below keep
their dated revision scope. Scientific review, hosted CI and final approvals
remain separate.

## Current Status

The subtitle now reads *Feature-Driven Decay in an Agentic Coding Loop. An
Exploratory Case Study and Experiment*, replacing *an Experiment Protocol* at
the owner's direction. The current
[paper](./main.pdf) and [source](./main.tex) present the completed exploratory
study through its principal findings: largely stable retention, selective
benefits from consolidation or review, and additional resource cost.
The [Supplement](./main.pdf#page=45) keeps the detailed results, uncertainty,
calibration and execution record in the same 73-page document.
The [source and digest register](./main.pdf#page=71) fills the final
three pages, so full identifiers no longer interrupt the narrative.
The Supplement is additive. It holds source-specific qualifications, detailed
method and rival checks, the frozen prompt, deferred rates and provenance.
The current build excludes the repeated Background text, figures and case
narratives; their earlier source versions remain in Git. Detailed
theory, illustrative economics, follow-up candidates and historical resource
arithmetic now sit in the existing Supplement, not a second document.
At the owner's request, the standalone supplement PDF/TeX/bibliography were
removed after exact archive readback and restore checks. Their original
committed versions remain in Git at `80656f32`. No source evidence was discarded.

The [24 November publication record](./anc/revision-report.md#publication-revision-and-disposition-24-november)
tracks the present source/PDF binding, all 24 review dispositions and
remaining publication gates. The
[15 November narrative and TODO record](./anc/revision-report.md#narrative-learning-and-todo-reconciliation-15-november)
preserves the v22 delivery and its evidence plan. The
[15 November direct style revision](./anc/revision-report.md#direct-style-revision-15-november)
binds the historical v23 source and PDF without changing the prior
author-voice record. The
[author voice follow-up](./anc/revision-report.md#author-voice-follow-up-15-november)
records that first-person revision and its validation. Earlier
deliveries keep their own records. The
[15 November provenance and readability record](./anc/revision-report.md#provenance-and-readability-15-november)
holds v21. The
[final-results and chart interpretation record](./anc/revision-report.md#final-results-and-chart-interpretation-15-november)
holds v20. The
[14 November critique and falsifiability revision](./anc/revision-report.md#critique-and-falsifiability-revision-14-november)
holds v19. The
[finalization follow-up](./anc/revision-report.md#finalization-follow-up-14-november)
holds v18. The
[report refresh](./anc/revision-report.md#attested-report-refresh-14-november)
holds v17. The
[readability revision](./anc/revision-report.md#readability-and-interpretation-14-november)
holds v16. Results remain enabled (`\resultstrue`);
the [13 November empirical integration](./anc/revision-report.md#study-results-and-post-collection-judging-13-november)
keeps the original results-intake and delivery record. The
[9 November supplementary judging record](./anc/revision-report.md#supplementary-blind-judging-9-november),
[8 November measurement clarification](./anc/revision-report.md#measurement-provenance-clarification-8-november)
and [execution and authorship record](./anc/revision-report.md#execution-registration-and-coauthorship-8-november)
keep their earlier dated scopes, as does the
[nine-point author review disposition](./anc/revision-report.md#author-review-disposition-1-november).
The case follows agent-assisted research,
Design Thinking challenge, prototypes, requirements, epics and stories,
autonomous delivery and renewed participant feedback. Project counts and
calendar dates no longer lead the argument. The supplied
[project-insights export](./anc/project-insights-2026-11-01.csv) supports the
backlog handoff. Its provenance and missing export metadata are in the
[evidence index](./anc/case-evidence-matrix.json).

### Narrative, Learning and TODO Reconciliation 15 November

The revised account starts with a usable workflow interrupted despite completed
issues and passing checks, then explains the decay conjecture and the
consolidation test. Mostly stable retention, selective coverage gains and
additional cost support only a narrower conclusion, and the conjecture is not
claimed as confirmed. Author reflections are attributed. Stronger-than-
expected model performance and the absence of the expected decay are reasons
to reconsider the measurement design, and they do not prove that harder tasks
must decay.

The next paper needs a separately designed, reviewed and prospectively
registered study. Longer, more coupled work and a full HVE research, plan,
implement and review comparison are candidates. Review's contribution must be
distinguished from the package where feasible. Substantially larger resource
approval is pending; no new run, judging call or protocol change was authorized.
The earlier numerical candidates and untested hybrid remain in the Supplement.

The [dated TODO disposition and remaining-work plan](./anc/revision-report.md#narrative-learning-and-todo-reconciliation-15-november)
separates decisions now applied from evidence and approvals still needed.
The supplied AICC acknowledgement records receipt on 14 November 2026,
correcting the earlier 27 October account. The author's expected response
date is 29 November, which does not guarantee clearance. arXiv is the selected target;
final-version clearance, both authors' final approval and current submission
policy/source-bundle checks remain pending. Only coauthor review was reported;
unsupported generic acknowledgements were removed.

Read-only inspection of the public experiment source and exports establishes
allocation/shuffling and asynchronous dispatch, not actual wall-clock order or
independent provider conditions. VM access will support the remaining historical
metadata, overlap and amendment/outcome-access chronology checks. It is not
needed for the editorial changes already applied.

The current PDF has 72 pages, with the Supplement beginning on page 45 rather
than page 48 in v21. I prioritised the shorter main route and the retained detail
over keeping the total page count unchanged. All 34 existing table data bodies, seven
displayed equations, three literal prompts and 61 source-register bindings
are preserved. No empirical/chart/diagram assets changed.

The 73-test authoring run passed 72 tests; the native diagram-export test
failed because the required Playwright browser was unavailable. A task-local
download did not finish and was stopped; no passing exporter check is claimed.
Structural checks pass. Tectonic produced the delivered PDF with only the
inherited `inputenc` warning; page/text geometry, nonblank pages and unresolved
reference checks pass, and selected rendered pages were inspected. The separate
`narrative_learning_revision` binding preserves v21 and all earlier bindings.
This focused editorial/tooling validation is not independent scientific review,
hosted CI, employer clearance or arXiv acceptance.

### Author Voice Follow-Up 15 November

The case narrative uses first-person singular for the author's actions and
reflections. The methods keep the participant-observer role, and the formal
author metadata and contribution statements keep the authors' names. The
future-study discussion now says what the experiment assessed and what a
follow-up design would need to examine. The study results, design and
protocol are unchanged.

The preceding 71-page PDF, Supplement start (page 45) and source-register pages
(69-71) are recorded in the `author_voice_revision` binding, which preserves
the preceding `narrative_learning_revision`. The focused authoring suite ran
74 tests: 73 passed, and the native diagram exporter could not launch because
its Playwright browser was unavailable. The structural checker passed.
Two-pass pdfLaTeX compilation succeeded with two ignored glue-shrinkage
diagnostics at `main.tex:1988`; selected pages were rendered and inspected.

### Provenance and Readability 15 November

The readability revision moves all 61 distinct identifiers previously
printed in the active paper into Table 35 at the end: 19 SHA-256 digests and
42 Git commit, tree or blob IDs. Short linked record labels replace full
hashes in Data Availability, execution history, judging and prompt provenance.
The register explains the identifier types and preserves historical/final
scopes; a matching digest establishes retained content, not claim support.

Result tables now include a local arm key. The task and checkpoint notation,
acquisition versus retention, sampling intervals versus missing-outcome bounds,
complexity and deferred intervention-demand rate are explained near their use.
Repeated numerical summaries and the long source/AI-assistance revision history
are shortened; their detailed tables and original dated records remain intact.
Follow-up designs and practice suggestions remain proposed, not demonstrated.

The full PDF remains 70 pages. The Supplement starts three pages earlier,
on page 48 rather than 51, which makes room for the three-page end register
without adding length. All 72 authoring tests and structural checks pass. Direct
comparisons preserve 1,454 fields in 34 existing tables, all seven displayed
equations, three literal prompts and every author TODO. All 61 PDF destinations
resolve, all pages are nonblank and text is in bounds; fourteen selected pages
were inspected directly or matched to inspected renders. The inherited
`inputenc` notice remains the only compiler warning.

The separate `provenance_readability_revision` in the
[binding](./anc/supplement-integration.json) preserves the v20 and earlier
deliveries. This is an assisted readability revision, not independent scientific
review or venue compliance. Remaining evidence/approval limits are unchanged;
no experiment, scoring, registration, paid call, commit or remote publication
was performed.

### Final Results and Chart Interpretation 15 November

The final [experiment report](https://github.com/jmservera/ama-thought-mve/blob/d097a10b090baefadf995ecd910eb96c324f0234/results/EXPERIMENT_RESULTS.md)
and its committed artifacts contain all 315 completed trajectories, 5,355
measured steps and 5,372 attempts across sixteen execution sources. The
owner-attested unassisted frame unlocks the primary and secondary coverage
contrasts; the primary B-D estimate remains +1.19 percentage points
(95% interval [0.10, 2.22]), below the ten-point practical benchmark.
The accepted retention panel records one open regression. Two CR1 outcomes
remain unknown, and 55 attempts retain incomplete billing. The supplementary
judging remains its earlier 313/315 snapshot (626 evaluable endpoint packets,
1,252 calls), not a new complete judging run.

The new [trajectory chart](./fig-study-trajectories.png) and
[outcome/cost chart](./fig-study-outcomes-costs.png) are generated from the
source-bound [snapshot](./anc/study-results-2026-11-15.json). Higher coverage
and fewer complexity hotspots are better on those measures. Contrasts
name their focal arm, separate the zero line from the +10-point benchmark,
and flag intervals that include zero as directionally uncertain. Readers
should take CR1 passes together with feature completeness, and unknown
outcomes are not failures. The cost panel says that upper-left is better only
at comparable delivered behaviour and that the billed sample differs from the
coverage sample. The editable economics figure marks its model as assumed.
Fewer break-even cycles mean earlier payback in that model and are not observed
savings.

All 70 authoring tests and structural checks pass. Plot ranges contain all
cell means, browser checks find no overlapping reading cues, and the 70-page
PDF has no blank pages or out-of-page text. Selected figures, the Supplement,
ledger and literal prompt pages were inspected. Only the inherited `inputenc`
notice remains. The [binding](./anc/supplement-integration.json) preserves the
earlier candidate and all dated revisions. Human approval, source-access limits,
hosted CI and independent exact-head review remain separate. No new experiment,
judge calls, VM mutation, commit or push was performed in this update.

### Critique and Falsifiability Revision 14 November

After the external hypothesis-falsifiability critique, I replaced the elastic
conjecture ("can carry ... unless") with a two-part falsifiable
formulation that separates the short-horizon decay premise (P1) from the
consolidation remedy (P2 coverage gain threshold $\Delta_*=10$ percentage
points; P3 change-request adaptability and credit payback) alongside the
structural treatment-fidelity check. Table 15 (`tab:predictionverdicts`)
summarises each criterion, observed result and exploratory verdict: P1 is
not supported on the ten-feature task, P2 is below the 10-point threshold
($+1.19$ percentage points, $[0.10,2.22]$), and P3 is not supported, while
structural fidelity succeeded.

The abstract, main coverage section and conclusion now give the per-model
coverage split next to the pooled $+1.19$-point B-D figure: GPT 6.1 Sol
gained $+3.15$ points ($[0.00,6.30]$) by overcoming F8's protected-test
allowlist lock on F9 ranking (12/21 vs 6/21 complete delivery), whereas
Sonnet 5.5 ($+0.26$ points, $[-0.15,0.75]$) and Gemini 4 Argon ($+0.15$
points, $[-0.15,0.52]$) B-D intervals span zero. Section 8.5 specifies a
30-to-40-cycle brownfield follow-up design matching the break-even regime
$N_{\mathrm{BE}}=\lceil 1+2k/\delta\rceil$, with $K\geq4$ branch-isolated
Latin-square change requests, a $2\times2$ factorial crossing refactoring
and invariant review (plus test-suite mutability), and preregistered
block-level falsification rules.

All 67 authoring tests pass, all 1,378 existing numerical table fields are
preserved, and the 66-page PDF (Supplement page 47) has zero overfull boxes
and visually verified pages. The new `falsifiability_revision` in
[supplement-integration.json](./anc/supplement-integration.json) preserves
v18 and earlier bindings.

### Finalization Follow-up 14 November

The exact Data Science and Engineering Coach assessed the remaining inference
TODO. The paper now spells out the implemented independent model/arm bootstrap
and the public block/source joins. Dependence justification and actual amendment timing
remain author decisions; no replacement estimator or new empirical runs were
introduced. Original-source checks support the retained figures with specified
full-text/abstract limits and the Laban v1 39%/35% presentation difference.

The active narrative, PDF participant contexts and native figure text name no
case partners, customers or coworkers beyond the two authors. Credited
publication authors and public speakers remain attributed. This gives no
confidentiality clearance for the complete Git history or for newly published
raw or ancillary extracts.

Read-only retrieval from the author-named VM working copies found all 5,357
attempt starts, controller durations, IDs and source commits. The study-state
hash matches Assessment v3; the retained judge config/source lineage is
consistent with SDK 1.0.28, CLI 1.0.105, `gpt-6-luna` and two repeats. No VM
restart, candidate/judge rerun or private-data inspection was needed. Unlogged
historical backend/case version identifiers cannot be recreated by a new session.

Manager approval and the 27 October CELA submission are recorded as the
owner's account. Absence of objection is no inspected final-version clearance,
and the earlier copy predates the empirical additions. The author still has to
confirm whether the current draft needs further review under the applicable
process. The experiment GitHub
repository is the selected deposit; its v4/v6/v7 archives/checksum assets are
retained, with a final release manifest and registered-archive correspondence
still to be completed.

All 66 authoring tests pass. All 1,378 existing table fields are preserved.
The single 64-page PDF retains Supplement page 45, in-page text and no blank
pages. Changed pages and the execution ledger/B/C prompts were inspected;
only the inherited `inputenc` notice remains. The
[binding](./anc/supplement-integration.json) preserves v17 and earlier history.
Hosted CI, independent exact-head review and final author/publication approval
remain separate unmet gates.

### Attested Report Refresh 14 November

The updated
[report](https://github.com/jmservera/ama-thought-mve/blob/bd75c1c2104d001d62f9fb2bb4feab438b86f763/results/WHITEPAPER_REPORT.md)
and companion extraction are pinned to `bd75c1c2104d001d62f9fb2bb4feab438b86f763`.
The local report matches the online `main` Git blob. Its published provenance
now records owner-attested intervention coverage for all 313 completed
trajectories, with none assisted. This is an operator account, not independent
verification of out-of-band activity. Two quarantined trajectories remain
partial, so the automated whole-study primary stays unavailable.

Separate complete-pair comparisons now report the equal-model-weight final
coverage differences: B-D `+1.1874` percentage points (95% bootstrap interval
`[+0.1000, +2.2247]`) and B-A `+1.4123` (`[+0.3250, +2.4497]`), each using
63 versus 63 allocated trajectories. The paper retains their exploratory,
post-collection status, unresolved scheduling dependence and small magnitude
relative to the earlier ten-point benchmark.

The existing Supplement adds model-level coverage and CR1 intervals,
full-allocation bounds and judge contrasts with abstention counts. It
distinguishes confidence intervals from missing-trajectory bounds, and
observed-scenario means from the strict complete-scenario estimand. Neither
the bounds nor the NA counts recover unrated scenario dimensions.

All 63 authoring tests pass. Checks reproduce the two pooled coverage
intervals and seven complete-cell CR1 intervals, verify 128 judge-summary
comparisons within published precision, match 241 new numerical/missingness
fields to the companion export and preserve all 886 v16 table fields.
The 64-page PDF has in-page text and no blank pages; selected rendered pages
were inspected. There are no unresolved references or overfull/underfull
boxes; the inherited `inputenc` notice remains. The
[binding](./anc/supplement-integration.json) retains all prior deliveries.
No experiment, scoring, registration, candidate or judge session changed.
Hosted CI and independent exact-head review remain unperformed.

### Readability and Interpretation 14 November

The abstract and conclusion now lead with the findings and their practical
meaning. Results distinguish acquiring a feature from retaining behaviour
that already worked, and explain why CR1 success has a treatment-dependent
retention baseline. Judging methods describe the performed assessment;
the earlier proposal remains identified as historical.

Coverage and CR1 outcomes have separate tables, as do structural metrics
and credits/minutes. Main results tables use larger type and descriptive
headings. Additional distributions, contrast bounds, size measures,
post-collection ratings, calibration and the fourteen-source ledger remain
in the existing Supplement. The claim that Gemini's baseline met every
structural target is corrected; Sonnet B's remaining lint is also explicit.
Observed spending precedes the unchanged hypothetical payback model.

All 60 authoring tests and structural checks pass. An additional 618 field,
denominator, ledger and CR1-bound checks against the staged v15 candidate
confirmed numerical preservation. The rebuilt PDF has no unresolved
references or overfull/underfull boxes; all 60 pages have in-page text and
no blank pages. Selected rendered results, conclusion and Supplement pages
were inspected. The inherited Tectonic `inputenc` notice remains.
The [current binding](./anc/supplement-integration.json) preserves the v15
delivery hashes separately. Dated sections below retain their original
status and validation scope.

### Study Results and Post-Collection Judging 13 November

The paper integrates the committed empirical study handoff from
[`results/WHITEPAPER_REPORT.md`](https://github.com/jmservera/ama-thought-mve/blob/main/results/WHITEPAPER_REPORT.md)
in `jmservera/ama-thought-mve` (`main` commit
`7943e40347862e76e3bc04490040ad5904487c86`, branch commit
`8591630c556f9f87c952f5d44ca7ce58b2bf1a83`, tree
`cb542312d8bde5d26bc716f2c8f7a5e8eaef7037`, report Git blob
`3e44ae10547b6376864089e605e946f74a378d56`, SHA-256
`2180679ce9fe18d77e3107ed5cdc01edd32749a4a15114bf23f647c516d83af4`),
backed by `results/pilot-estimation/` and `results/pilot-estimation-judging/`.

* Across 315 allocated trajectories (three models x five arms x 21 replicates;
  5,355 scheduled steps), 313 trajectories (99.37%) completed all delivery and
  CR1 steps, yielding 5,341 measured steps (99.74%) across 5,357 attempts
  spanning 14 execution source commits through
  `a9d76bb6dbb118c43315fb2a13b7bcdb732d946d`. Two trajectories
  (`pilot-estimation-gemini-4-argon-E-15` at 10/21 steps and
  `pilot-estimation-gpt-6.1-sol-C-20` at 18/21 steps) were quarantined after
  provider transport/fallback interruptions and remain in all allocation
  denominators.
* Formal primary bootstrap intervals remain withheld
  (`primary_estimates_available = false`) because no external post-collection
  operator attestation (`intervention-coverage/v1`) was supplied to certify
  the absence of out-of-band human edits and two trajectories in Arms C and E
  were quarantined. All findings are reported as exploratory estimation with
  exact CR1 identification bounds.
* Out of 5,357 attempts, 5,303 settled with complete billing (`62,052.61` AI
  credits, exact `62,052.6069`), while 54 attempts (38 native-retry holds,
  15 recovery-interrupted holds and one quarantine hold) retain `18,900.0`
  reserved credits (`783.16` credits, exact `783.16186`, certified as a
  partial lower bound).
* Ten sequential features induced only one open contract regression at P10
  across 313 completed trajectories (`claude-sonnet-5.5` and `gemini-4-argon`
  averaged 99.18% to 99.74% P10 pass rates; pooled within-cell SD is 3.11
  percentage points with 298 df). Arm B eliminated functions above cyclomatic
  complexity 10 (0.00% across all 63 Arm B runs), reduced lint density by 92%
  on `claude-sonnet-5.5` and 100% on `gpt-6.1-sol`, mitigated `gpt-6.1-sol`'s
  self-locking F8 test allowlist (raising 100% P10 completion from 5/21 in A
  and 6/21 in D to 12/21 in B and E), and roughly doubled delivery credits
  (1.84x to 2.25x vs A) without lowering CR1 cost. On `gemini-4-argon`,
  read-only review in Arm C (16/21 CR1 success, 76.2%) outperformed
  metric-gated consolidation in Arm B (8/21, 38.1%) when already-green static
  metrics left an F8 view-method blocklist trap untouched.
* Post-collection replay of 12 public-specification workflows across 3,457
  recorded commits (630 endpoint packets; 626 evaluable) found zero witnessed
  capability losses (`observed_loss = 0`). Blinded `gpt-6-luna` Assessment v3
  (`c10e6d6f`, 1,252/1,252 calls, `418.64` settled credits after halted v1/v2
  attempts holding 60 reserved credits and `5.28` settled credits) yielded
  positive complete-frame B-D and B-A contrasts on functional completeness and
  API usability (`+0.0577` and `+0.0599` for B-D at P10; `+0.0351` and
  `+0.0357` at CR1). Human calibration across `S01..S08` (90 rows, 79 scorable
  rows, 16 distinct contexts, scored by `jmservera` under
  `human-calibration-guidance/v3` with `review_status = in_progress` and
  disclosed AI-assisted failure/mismatch triage) had 94.3% to 98.7% raw exact
  agreement (87.5% to 96.9% equal-context exact agreement) and zero
  disagreements of two or more points. The 5,357-journal SDK audit confirmed
  zero interactive user-input RPCs, 99.83% `isolated_exec` tool discipline
  (74 rejected built-in `create`/`edit` attempts on Sonnet 5.5), and 36
  sessions (0.67%) ending with a permission or environment question.
* The complete v15 delivery has 56 pages, with empirical results in
  Sections 7.8-7.11 (pages 26-30) and the additive Supplement starting on
  page 46. All 58 authoring tests and structural checks pass; Tectonic
  0.17.0 compiles the PDF with zero errors, zero unresolved references and
  zero overfull or underfull boxes.

### Supplementary Blind Judging 9 November

The paper adds a prospective supplementary assessment from the supplied
[judging README](https://github.com/jmservera/ama-thought-mve/blob/b7973e200a6edbb1d19355badae3b7e03a066b09/judging/README.md),
commit `b7973e200a6edbb1d19355badae3b7e03a066b09`, README Git blob
`6cc0c236e4ca093198d38909dceb80f850196faa`. It is a separate development
branch and differs from the running source `e71037d9`. The
[main methods](./anc/experiment-protocol.tex) introduce the panel and
the [additive instrument account](./anc/measurement-provenance.tex)
defines scenario eligibility, witnessed endpoint loss, ordinal AI ratings,
full-frame missingness, blinding/calibration and separate judging costs.

After collection stops, archived measurement HEADs will supply P1-P10 and
post-CR1 evaluations without rerunning or repairing development trajectories.
The fixed panel includes ten feature workflows, a delivery/reopening journey
and CR1. Four separate 0-4 ratings concern exercised API tasks, with
unsupported dimensions null. There is no composite quality score or
human-usability claim. A low conditional loss density can accompany poor
acquisition; final fulfilment and risk-set sizes must be reported with it.
Repeated judges/scenarios/checkpoints do not enlarge independent n.
Model-balanced contrasts require the full allocated comparison frame.
The source-based assessment identified a material packet limitation:
earlier passing witnesses and retention labels are visible to the judge,
and historical/final observations reuse local IDs. Ratings may consequently
reflect historical anchoring despite requiring final evidence citations.
Post-CR1 endpoint loss also includes failures already present at P10.
The paper discloses both limits and does not describe the packets as
endpoint-only or the loss as CR1-induced. Judge-specific calibration, private block/epoch linkage
and full-frame affordability remain operator decisions.

The original endpoints, treatment budgets, registered-base/unregistered-
amendment account, historical source pins and false results switch remain.
The assessment is supplementary exploratory, not retrospectively
preregistered. Actual judging runs, calibration, outcome exposure, evaluated/
missing counts, versions and costs remain author/operator TODOs.
The [dated revision](./anc/revision-report.md#supplementary-blind-judging-9-november)
records source support, the Coach-guided assessment and validation limits.
The supplied Data Science and Engineering Coach definition was used in a
separate general-purpose agent context because the exact named agent was
not launchable; this is not independent human or scientific approval.

The initial judging-only v14 candidate had 47 pages, Supplement page 37, main judging
methods page 21, and instrument/rubric detail pages 44-46.
Tectonic 0.17.0 compiled it without errors, unresolved references or
overfull/underfull boxes; the inherited `inputenc` compatibility warning
remains. The actual changed pages, intact B/C prompt displays and all-page
layout proof were inspected. All-page text bounds, 183 internal destinations,
51 outline entries and absence of blank pages pass. Current source/PDF
bindings and historical records remain distinct.

#### Technical Flow Continuation

The owner later supplied a host/container explanation and
two flows. The first describes supplementary post-run replay and judging;
the second describes development-agent command execution. The paper uses
those names to keep a tool-enabled builder apart from a tool-free
judge. The [execution-boundary subsection](./anc/experiment-protocol.tex)
and paired runtime diagram separate trusted-host Python/JavaScript transport,
fresh command containers, persistent writable development files/Git and
read-only post-run snapshots/evaluator inputs.
They distinguish collection/isolation unavailability from observed
candidate failures and keep source-described controls separate from
verification of historical runtime conditions.

The complete v14 delivery has 49 pages, Supplement page 39,
execution-boundary text page 17, paired diagram page 19 and judging
methods page 21; detailed judging rules are pages 46-48.
The diagram retains editable Excalidraw source, native SVG/PNG exports and
source/export hashes. It is conceptual, not an execution trace.
Source comparison qualifies the supplied capability claim: four supervisor
capabilities are re-added, while the candidate child has cleared capabilities.
Development state persists by validated replay, not a writable host checkout.
The [current binding](./anc/supplement-integration.json) preserves the
earlier judging-only and 8 November records.
All 57 authoring tests and structural checks pass. The complete PDF's
all-page bounds, 184 internal destinations, 52 outline entries and absence
of blank pages pass; the paired diagram, changed pages and intact B/C
listings were inspected. Tectonic retains the inherited `inputenc` warning
without errors, unresolved references or overfull/underfull boxes.

### Measurement Provenance 8 November

The paper now states which quantities are measured, with their units, denominators,
checkpoints and instruments. It keeps functional outcomes, structural proxies,
resource observations and annotation-based integrity records apart. The
[active measurement section](./anc/experiment-protocol.tex) and
[additive field/prompt inventory](./anc/measurement-provenance.tex) are based on
read-only inspection of public
[`e71037d9`](https://github.com/jmservera/ama-thought-mve/tree/e71037d961cb80fc5c659437796de7736820f6c9).
I did not remeasure private data.

At that running-source pin there is no separate numerical LLM-as-judge.
The proposed supplementary instrument above has a distinct role.
Hidden contracts and fixed
code-analysis tools produce the outcomes and metrics. Arm C's qualitative review
is an intervention and receives no score. The
[active B template](./anc/consolidation-active-e71037d9.prompt.txt) and
[active C template](./anc/review-only-active-e71037d9.prompt.txt) are retained
verbatim with SHA-256/Git-blob regression checks. The
[historical v4 prompt](./anc/consolidation-frozen-v4.prompt.txt) is unchanged and kept separate. The paper
explains stripping/substitution and the limits of replaying private session
context from a public template.

The current Ruff call uses isolated fixed rules but does not ignore inline
`# noqa`, and no separate suppression count is exported. The earlier safeguard
claim is now corrected as a limitation, with no silent instrumentation
fix. The code's conservative unavailable retention summaries and composite-only
CR1 reporting differ from the richer planned exports, and the paper says so. Quality-report
targets are model instructions, not a hard aggregate `make check` quality gate.
The code emits no overall architecture/readability/comprehension score and no
maintainability index.

The running experiment, source epochs, registration/amendment account,
coauthors, false results switch, historical records and slides are unchanged.
The [dated revision](./anc/revision-report.md#measurement-provenance-clarification-8-november)
records the current build, PDF inspection and publication evidence.
Six documentation regressions supplement the existing authoring suite.

The checked v13 delivery has 45 pages, with the Supplement on page 37. All
50 authoring tests and structural checks pass (94 cited/105 reusable
entries; 1,806-character abstract). I rendered and inspected Tables 7/15 and the complete B/C examples.
Both templates match the visible PDF text after
whitespace normalization and exclusion of page-number footers. All-page bounds,
180 internal destinations and 49 outline destinations pass. The C example
stays together on page 45. Tectonic 0.17.0 reports no errors, unresolved references
or overfull/underfull boxes, and one inherited `inputenc` compatibility warning
remains. Historical body-word comparison is unavailable, and the old
pdfLaTeX-specific marker check is not claimed under Tectonic.
Independent scientific/human, hosted and publication approval remain separate.

### Execution, Registration and Coauthorship 8 November

The exploratory experiment is now running. The owner chose coauthor
credit for Isabel Cabezas Martin and confirmed her agreement to that credit
and the stated affiliation: Software Engineer, Frontier Company at
Microsoft. The paper and PDF metadata add her alongside Juan Manuel
Servera Bondroit, whose current name and affiliation stay as they were. I infer no location,
email, ORCID, credential, manuscript review or final approval.

Servera Bondroit conceived the study, designed the methodology and evaluation
criteria, analysed the historical exploratory case and wrote the manuscript.
Experimental analysis remains his responsibility and is not a completed new result.
Cabezas Martin conducts ongoing execution and data collection independently
under the predefined exploratory protocol and disclosed amendments.
Splitting execution from design and manuscript preparation is meant to
minimise potential experimenter bias. Both authors are Microsoft employees, so
operational separation does not establish institutional independence,
independent scientific review/analysis or demonstrated elimination of bias.
The views and competing-interest statements are plural. Employer
external-publication clearance and final-author approval remain separate.

The registered base is [OSF xcpt4](https://osf.io/xcpt4), dated
7 November 2026, as confirmed by the owner. The supplied access checks saw
an app shell and API HTTP 401, so independently verified OSF metadata is
unavailable. The date implies no timezone, approval/embargo status,
DOI or prospective timing for the entire dataset.
Current execution includes disclosed unregistered amendments for short
calibration, parallel execution and VM restarts. It is not one preregistered
confirmatory run, and I assert no new OSF amendment.

The commit-pinned active source is
[`e71037d961cb80fc5c659437796de7736820f6c9`](https://github.com/jmservera/ama-thought-mve/tree/e71037d961cb80fc5c659437796de7736820f6c9),
tree `e7ec1561d4ecee921e7c9eba3711a1ab7e9f4058`, without a tag.
The profile is `pilot-estimation.json`, design
`model-stratified-v2-five-arm`, suite `s1-retrofit`, exploratory
pilot-estimation with no formal hypotheses. The owner supplied the runtime
selection: GPT 6.1 Sol / Claude Sonnet 5.5 / Gemini 4 Argon, medium
effort, arms A-E, 21 trajectories per model per arm despite the file default
of 12, F1-F10 plus held-out CR1, seed 2027. That gives 315 planned trajectories.
The protocol's false/null current-registration fields describe the
uncompleted current amendment. The registered base still exists.

The [revision record](./anc/revision-report.md#implementation-epochs-and-evidence-states)
retains all three implementation epochs and owner-reported step counts
(651 + 227 + 369 = 1,247). Completed steps are not independent n, successful
outcomes or completed trajectories, and commit dates are not collection times.
The record keeps epoch labels, failures, unknowns and the temporal/arm/model confounding
limits. It supplies no homogeneous pooling and no post-hoc sensitivity results.
Historical v4/v6/v7 records and the earlier power/resource scenarios stay
historical and numerically unchanged. The PDF captions of the retained v6 diagrams
now label their default/full-calibration settings as historical.

The false results switch, owner-selected title, original adverse reviews,
case evidence, frozen prompt and one PDF with an additive Supplement are
preserved. The scientific-critical-thinking skill materially supported this scoped
revision. The existing `kassis2026skills` citation and earlier assistance
disclosure remain, and an 8 November assistance account is added.
This revision involved no experimental outcome analysis, model call, private-data read,
experiment-source/config change, registration/visibility action or
collection action.
The dated revision record holds the focused validation and delivered-PDF details.
Independent assessment and the publication gate are left
to the parent.

The v12 execution/authorship delivery had 40 pages, with the additive Supplement beginning
on page 35. All 44 existing tests and the structural checker pass.
Tectonic 0.17.0 reports no TeX errors, unresolved references or overfull/
underfull boxes, and one inherited `inputenc` compatibility warning remains.
All-page text bounds, 174 internal links and 47 outline destinations pass.
I inspected changed-content page renders and all-page layout proofs.
[supplement-integration.json](./anc/supplement-integration.json) holds the current source/PDF digests and active Supplement bindings. The revision record has the exact
checks, access limits and the external run.

### Recovery and Scientific Alignment 5 November

This dated recovery record retains the earlier source findings and gates.
The owner-confirmed execution account above supersedes its then-current
implementation and pre-collection status, and nothing is silently overwritten.

PR #1206 was closed at the owner's request without deleting its branch.
PR #746 had already preserved the earlier scientific skills, reviewer and manuscript work. Only amendment `3ef395b8` was recovered onto
`docs/paper-scientific-reconciliation` from current main `c6d5a8f3`.
The replay completed without conflicts and kept the existing
knowledge-base log as a prefix.

The [fresh scientific review and disposition](./anc/revision-report.md#recovery-and-scientific-alignment-5-november)
supersede the dated implementation assessment below. Read-only inspection
of `jmservera/ama-thought-mve` default `5ab24be4` verified all five arms,
the immutable 12/21/33 selector and the published
[v6 source packet](https://github.com/jmservera/ama-thought-mve/releases/tag/protocol-frozen-v6).
Its execution source is `7de2f0d4`, and the default head changes only the freeze
manifest. I did not use the stale local MVE checkout as current evidence,
and I did not reproduce the source-declared runtime qualification.

The review found three major concerns and one minor framing issue.
I corrected the current-capability wording and the primary matched-ceiling description. The protocol and measurement figure now separate the proposed
observed-subset retention/graded-CR1 reports from the inspected analyzer's
conservative unavailable summaries. The independent-arm bootstrap is an
implemented candidate and does not resolve scheduling-block
dependence. The original adverse review is retained unchanged.

Before collection, the author must resolve reporting and block-inference
alignment, record and justify the selected allocation, establish full-study
affordability/deadline acceptance and obtain an approved exact-source
prospective record. The inspected v6 manifest has a null registration date,
no recorded prospective OSF update and no collection authorization.
I changed no kit, saved study, freeze, OSF record, paid experiment or visibility.
This recovery is manuscript development. It is neither scientific acceptance
nor permission to collect data.

Nine new stdlib planning regressions reproduce all 39 resource-table cells,
three sample-size rows, nine economic sensitivity cells, discrete payback,
matched ceilings and allocation-bearing labels. A further regression guards
the current source pins and explicit reporting/inference limits.
The independent SymPy check confirms the conditional independent-cell
variance and cost summation. At assumed SD 25, the normal planning powers
for n=12/21/33 are approximately 0.396438/0.612203/0.803527. These are
hypothetical sensitivities, with no measured variability or observed power behind them.
The dated disposition records the final build and publication evidence.
The existing Scientific Agent Skills citation and four-skill assistance
disclosure are retained.

Final local validation passes all 44 authoring regressions and the structural
checker: 94 cited entries, 105 reusable entries and a 1,719-character abstract.
Tectonic rebuilds the 38-page delivered PDF, with the Supplement on page 33.
All-page text bounds and internal links pass. I rendered and inspected the revised power/resource
pages and both changed native diagrams.
One inherited `inputenc` compatibility warning remains. Historical body-word
comparison is unavailable, and the optional pdfLaTeX-specific marker check
is not claimed under Tectonic. Exact-head review, the focused repository gate
and hosted checks are separate publication steps recorded with the
replacement PR, and none authorizes experiment collection.

### Prospective Allocation 2 November

This dated record retains the original allocation revision and inspection
limits. The 5 November v6 source check above supersedes its A/B/C-only account, and it no longer describes the current implementation. The
power/resource scenarios remain historical planning and differ from active
F10/n21 execution and its short-calibration amendment.

The researcher selects 12 (default), 21 or 33 independent repository
trajectories per model per arm before study collection. The choice, its
rationale, the planning SD, the power/precision trade-off, the date and the source-bound
configuration go into the saved study record and prospective protocol. The saved
allocation cannot change on resume or in response to outcomes. Features,
tests, checkpoints and agent sessions are observations within a trajectory
and add no independent replicates.

The proposal retains three models and five arms. A is feature-only,
B is consolidation, C is information-bearing review, D is matched-resource longer
feature delivery and E is visible regression repair. For the primary
equal-model-weight ten-point B-D contrast, the existing normal approximation
with alpha .05 and target power .80 gives 12/21/33 per cell under assumed
within-cell SDs of 15/20/25 percentage points, respectively. These are
conditional planning assumptions. They are neither measured variances nor interchangeable
80%-power guarantees. Default 12 is not an 80%-power design under SD 25.

| n per model per arm | Study trajectories | Study sessions | Sessions with calibration | Maximum hours with calibration | Nominal credits with calibration |
| ------------------- | ------------------: | --------------: | -------------------------: | ------------------------------: | --------------------------------: |
| 12 (default)        |                 180 |          3,060 |                     3,300 |                       1,500.00 |                        1,107,000 |
| 21                  |                 315 |          5,355 |                     5,595 |                       2,546.25 |                        1,876,500 |
| 33                  |                 495 |          8,415 |                     8,655 |                       3,941.25 |                        2,902,500 |

Study trajectories are `15*n`, and study sessions are `255*n`. Excluded
cost-only calibration remains 15 trajectories, 240 sessions, 105 maximum
agent-hours and 81,000 nominal credits, without CR1. Combined maximum hours
are `116.25*n + 105`, and summed nominal session allowances are
`85500*n + 81000` credits. The table combines only study and calibration
allowances. It excludes prior charges and unknown-usage holds.

These allowances do not enlarge the actual 300,000-credit aggregate envelope
or 270,000-credit local admission ceiling. Prior spending, unknown-usage
holds and all-attempt costs remain in admission accounting. Cost-only
calibration must establish affordability of the entire selected allocation
and deadline. If it does not, the study halts and keeps the selected sample. A revised
allocation requires a separately authorized prospective amendment and a new
saved study. Outcome-driven resizing, a changed allocation on resume
and a silent reduction to fit the budget are all excluded.

The owner-reported MVE update accepts `--replicates 12`, `21` or `33`,
default 12, and preserves its saved selection immutably, but implements only
A/B/C. The five-arm paper has no five-arm executable implementation behind it, and D/E
and their source-bound qualification remain gaps. The earlier
[v5 candidate](https://github.com/jmservera/ama-thought-mve/tree/feat/fair-study-v5)
records do not establish current D/E implementation. The published
[v4 freeze](https://github.com/jmservera/ama-thought-mve/releases/tag/protocol-frozen-v4)
includes neither the new choices nor the MVE update.
The original registration and historical freezes remain unchanged.

The [2 November revision record](./anc/revision-report.md#prospective-allocation-revision-2-november)
records the arithmetic and source limits. The four scientific skills informed
the audit. Replicate-block scheduling still needs reconciliation with the
independent-trajectory variance and bootstrap scheme before a new freeze.
I changed and ran no MVE source or saved study here.

Pending results remain author TODOs. The rebuilt paper has 38 pages, with its
Supplement starting on page 33. All 34 authoring tests, the structural checker,
39 resource-table cells and three sample-size rows pass. Direct compiler/PDF
checks find no unresolved references, overfull text, blank pages or out-of-page
words, and I rendered and inspected both revised table pages. One inherited
`inputenc` compatibility warning remains. The historical body-word comparison
is unavailable, and the optional old log check still expects a pdfLaTeX marker.
Both allocation-bearing figures and their authoring script now use the
selectable sample and default 180 trajectories. Refreshed native SVG/PNG
exports pass overflow, hash-binding and visual checks, and the frozen prompt and
active Supplement hashes remain unchanged.
The focused repository gate against freshly fetched `origin/main` at
`a56df549` stopped at clean-candidate preflight because tracked modifications
or untracked inputs are present. I claim no passing receipt or publication readiness,
and I used no commit, stash or exclusion to bypass the gate.

No experiment was collected. New source-bound review, runtime qualification,
cost-only calibration, affordability/deadline, owner freeze, actual prospective
OSF recording and launch authorization remain gates. The owner-reported
original OSF approval does not cover this amendment. A separate researcher
provides operational separation and no independent scientific certification.

On 1 November the owner explicitly authorized development PR updates while
both repositories were public. This interim source exposure is disclosed,
and later privacy cannot erase it. Before collection the owner will make both
original repositories private, and the researcher must lack access to the
original checkouts, manuscript and author-context caches. Protected operator
assets remain separate from candidate tools. Approved researcher materials
and results are released with the paper after collection. No archive, OSF
upload, visibility change or scientific submission occurred here.

The native Excalidraw sources remain editable and bound to SVG/PNG exports.
The five-arm and measurement diagrams drop the prematurely printed CR1
topic, and the economic diagram plots the break-even boundary against k/delta.
PF1-PF3 still await real data. Original critiques, prior datasets, published
chart inputs and historical revision records are retained.

The dated sections below retain their earlier allocations, page counts and
five-arm implementation claims as historical disclosures. Their fixed-33
resource totals describe the 33 option and not the new default. The current
allocation and implementation boundaries above supersede those claims.

The [dated review and complete pending checklist](./anc/review-2026-10-29.md)
records the earlier findings, evidence coverage, applied changes, launch
blockers and deferred work. The v4 reconciliation below supersedes its
experiment-readiness statements. The historical
evidence and original [editorial critique](./critique.md) stand.

## Critique Disposition 1 November, v9

Work execution covers the offline manuscript/kit candidate and its inspected
evidence. The assessment is assisted checking. It is not independent human peer review,
statistical certification, ethics approval or venue acceptance.

### Added Reflection and Memory Sources

The owner authorized the new research in this same branch/PR.
The [contextual source synthesis](./anc/supplementary-context.md#reflection-memory-and-self-improvement-1-november-source-check)
records the complete available auto-caption check, timestamp links and
source qualifications. The main article uses the research in its bounded
correction, tooling and discussion sections. The title and experiment are
unchanged.

The captions do not support the first video's headline: Ng discusses
coding tools changing every three to six months, and says nothing about prompting dying.
Ng introduces Laurence Moroney at 16:31, and the later technical-debt and
reflection passages are Moroney's. The second video is an independent upload
of an apparent Anthropic staff presentation about persistent memory and
asynchronous dreaming. It comes from no official channel and is no independent tutorial
narration. Its uploader percentages are not experimental results.
The limits of automatic captions and unverified original recording/audio remain
explicit.

Ng's [official reflection letter](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/)
recommends Self-Refine, Reflexion and CRITIC, and the verified authors of those
papers do not include Ng. MedAgentBench is a verified Ng-coauthored paper about interactive
evaluation and contains no controlled self-improvement treatment.
The source paragraphs separate task iteration, retained memory, repository
correction and weight training, and no performance effect is transferred to
this study.
The literature-enhanced build has 35 article pages, 22 supplement pages,
89 cited main-text entries and 105 reusable bibliography entries.
Nineteen focused authoring tests and the structural/source checker pass,
and both PDFs compile without undefined references or overfull text.

### Publication and Validation Scope Correction

The owner stopped the full documentation gate on 1 November and explicitly
directed focused validation for docs. The earlier gate attempts and blockers
are historical. They do not require an unchanged application matrix to pass
before publishing this manuscript. The attached pull error came from divergent
topic history under a fast-forward-only pull policy and involved no unresolved conflicts.
The remote topic was merged cleanly and the revised paper survived. The owner
selected topic-only publication, leaving PR #692 open.

Executable kit checks remain separate: the new local image builds with strict
signatures, all 25 actual canaries pass, and all nine focused current-image
tests pass with declared dependencies. I claim no final whole-kit pass. The [experiment candidate PR](https://github.com/jmservera/ama-thought-mve/pull/6)
is a draft and does not authorize collection, freeze or OSF actions.

### PR Review Corrections

All five initial 1 November inline review findings are addressed:

* Manuscript integration checks every delivered conceptual figure, and removing
  any one of the five includes now fails its regression.
* Evidence reports use exclusive final-file creation. The tool refuses existing outputs and
  symlinks, including a report or link created during measurement, and neither overwrites retained evidence nor follows the link.
* TeX input expansion ignores comments while preserving their text and TODO
  markers. Missing or misleading disabled slices cannot affect structural
  checks or bibliography normalization, and escaped percent signs remain literal.
* The replication section states the complete pooled-SD instruction once,
  separately from the provider-drift qualification.
* The collection section separates researcher-workspace controls from the
  complete owner repository-privacy instruction.

VS Code had no registered test controller, so I verified with the existing
stdlib runner: 27 focused authoring tests pass. Source/bibliography checks and
changed-Python syntax lint pass. The 35-page article and 22-page supplement
rebuild with the selected title, without undefined references or overfull
text. I claim no full unchanged-application gate, new experiment, registration
or scientific acceptance.

The review also raised a lint-denominator finding, now corrected. Ruff receives only the
counted Python files, so frontend growth cannot dilute its density.
The [regenerated evidence](./anc/revision-metrics-2026-11-01-python-lint.json)
reports 6,365/25,756/33,618 submitted Python lines and
188.22/142.30/125.83 findings per 1,000 Python lines.
Original all-language figures remain in the historical record with a correction
notice. Source hashes, lint counts, complexity and duplication are unchanged.

### Single-document Delivery

The sole current deliverable is the 37-page [main.pdf](./main.pdf), and its
Supplement starts on page 32. The owner-directed additive revision removes
the repeated Background, three repeated figures, long case narratives and
five repeated indicator rows. It keeps the additional source qualifications and detailed
operational/rival checks, along with reproducibility definitions,
the exact frozen prompt and deferred measures/provenance.

There is one shared 94-entry cited bibliography, and the reusable source
bibliography retains 105 entries. The
[integration manifest](./anc/supplement-integration.json) separates the
original full-integration hashes from the current owner-approved additive
content. It binds the active body hashes and the complete literal prompt,
and it does not claim every earlier paragraph remains active.

Thirty-four focused tests pass, including additive-content/figure guards,
one-document delivery, all five figure-removal cases, exclusive report writes,
comment-aware inputs, literal renderer/path binding and Python lint
denominators. The selected title is unchanged. The actual PDF outline,
internal navigation and all-page bounds pass.

### Tectonic Warning Review and Remedy

The old `fvextra` dependency loaded `lineno` 4.41, whose line 296 contains a
Latin-1 `0xfc` byte in a TeX comment, and that byte caused the UTF-8 diagnostic. The
paper text was not corrupt. The literal prompt now uses `listings` wrapping
and straight-quote handling without loading `lineno`. Its original ASCII
file and SHA-256 are unchanged, and I edited no package cache or warning filter.

The short Chen/Zaharia/Zou citation uses scoped ragged-right formatting, as
already used elsewhere in the bibliography, so its justification no longer stretches.
The other underfull paragraph belonged to the repeated compact
appendix, which the additive supplement no longer includes.
`./tools/update-pdf.sh` now completes without the reported warnings, undefined
references or overfull text. I rendered and inspected the citation, supplement opening and literal
prompt pages. This implies no full application gate, new
experiment or approval.

| Recommendation | Applied change and evidence limit |
| --- | --- |
| Protect paper/code/oracles/CR1 from experiment agents | Private-repository and fresh-operator readbacks are required before collection; candidate tools remain isolated/no-network, with the host provider connection distinguished. Interim public development exposure is explicitly recorded. |
| Increase within-model replication and add fair controls | Five arms, 33/cell, 495 trajectories; D has one 45-minute/600-credit feature session versus B's 30+15 minutes/300+300. E uses visible specifications, never hidden evaluator feedback. The variance assumption and transfer limits remain explicit. |
| Replace uninformative two-run statistics | A single prospective blocked B-D coverage comparison; per-model and other contrasts secondary. Historical v1 keeps its two-run identity, four pairwise differences and nine-df planning SD, not a nominal 95% small-sample claim. CR1 is secondary and not powered by the coverage calculation. |
| Add graded CR1 and prerequisites | Contracts passed/15, prior passing contracts lost and observed/missing denominators; F9/F10 acquisition strata are post-treatment selections, not randomized subgroups. |
| Correct loss-density missingness | Observed inherited-risk denominator is separate from full risk and missingness; unknown results cannot count as not lost. Histories and episode censoring remain visible. |
| Address Goodhart and C's effect on later repairs | Structural/suppression metrics are treatment fidelity, not efficacy. Fixed external Ruff ignores local suppressions. C can influence later feature repairs; genuine review/diff annotations are required, not file-overlap inference. |
| Add feasibility, mutation and timing controls | Explicit infrastructure/missingness/oracle/privacy/billing thresholds; all-run cost/deadline admission; bounded mutation diagnostics and source hashes; observable request/tool latency with provider-active/rate-limit components unknown. |
| Randomize later change requests | A prewritten request-pool follow-up is separate from the current fixed CR1 and needs later registration. No current request is silently replaced. |
| Resolve cost arithmetic and currency contradictions | Combined 8,655 sessions/3,941.25 maximum hours/2,902,500 nominal credits exceed the unchanged 300,000 envelope. Actual affordability is not claimed; no dollar conversion or silent sample reduction. |
| Fix conditional cost-of-inaction interpretation | Explicit multiplication, k/delta break-even, null/no-payback and k=100/delta=1 counterexample at 201 cycles. k awaits billed calibration; capped feature budgets do not identify the uncapped, quality-matched delta. |
| Correct citation scope and attribution | Acceptance-criterion optionality and recording human reasons are the author's extensions. Learning-through-use source, test-deletion joke, context-file costs/success, commit-category overlap, assistant-era randomization and seven-of-twelve library findings are qualified. |
| Verify Pan numbers and locators | Four points/whiskers and the 619-event -1.1 [-3.8,+1.6] contrast checked against the PDF; 4.0-to-7.2 means are unweighted. Terminators/constructor verified in Section 5.1/Figure 5; Figure 1 supplies framing. Unconfirmed eight-of-ten detail removed. |
| Update metadata, access dates and sorting | Actual DOI/venue/page/version checks are distinguished from claim support. All 31 web entries have dated access or explicit failed/partial attempts. Stable citation IDs sort by named authors, including Young/Lopopolo/Park. |
| Preserve case evidence before it expires | Named repository metadata and the original/follow-up source hashes are retained. The owner explicitly deferred historical cloud/sign-in/usage exports; no tenant-wide query, attribution or first-failure timestamp is fabricated. |
| Check early blockage and later recovery | #349's 16 October record is not the first actual failed-sign-in time. 27 October directory-retirement sign-off does not establish a new successful journey or time-to-restored-usability. |
| Run pinned static checks and learning tracing | Three source snapshots measured with Lizard 1.24.3, Ruff 0.17.3 and jscpd 5.4.1. 487 committed research/plan files screened; 81 identity/runbook-pattern matches include generic pointers and do not prove actual session access or lost knowledge. |
| Normalize periods and explain Other | Seven/ten calendar-date churn windows are distinct from nineteen-day PR baseline. Tracking/day falls 34,026 to 24,037; product/integration 262.45 to 132.25. 60,001 Other additions are one CSV asset; contents were not read. |
| Repair lexical/figure claims | Evidence-boundary phrases, not general hedging; 24 pre-loop matches, nine on 4 October. Twenty inspected contexts are status/approval boundaries, not factual accuracy or independent coding. Zero and undefined marks differ; the full window starts 11 September; all five mechanism labels appear. |
| Report post-case specification growth | BRD/PRD approximately +15%/+42%; combined documents +25% to 173,504 words. Actual loaded tokens and provider-matched tokenization remain unavailable; the prose heuristic is removed. |
| Shorten, disclose and preserve the title | Main article plus separate evidence supplement; HIR/IDR/hashes moved to supplementary appendices. Microsoft employment/tool/programme interests and post-outcome case selection are disclosed. The requested title is retained. |
| Match the frozen prompt and preserve evidence | The supplement includes the exact v4 prompt as wrapped verbatim, with a byte hash, not a paraphrase claimed identical. Routine future product tracking can be excluded only after finite archive/restore-backed preservation; no historical tracking was wiped. |

### Evidence and Source Limits

The [access/claim register](./anc/citation-access-2026-11-01.json) lists the
inspected passages, metadata-only checks, user-supplied qualifications and gaps.
Fresh SEC/Medium/OpenAI retrievals returned 403, and organization SAML denied HVE tag access.
I attempted no bypass. YouTube returned HTML, so no video was inspected. SlopCodeBench v2 identity is pinned without inventing a
fresh NeurIPS acceptance check.

The [post-hoc evidence](./anc/revision-metrics-2026-11-01.json) contains exact
source hashes, static metrics, lexical sample and named GitHub metadata.
These checks do not reproduce original studies or prove historical deployed
usability. The [case index](./anc/case-evidence-matrix.json) retains null
release/journey links and the original 27 October record separately.
I read no private dataset or historic tenant-wide logs and ran no paid experiment.

The earlier 35-page article and 22-page standalone supplement compiled with
Tectonic before consolidation. They are historical validation records and no
longer separate current deliverables. All-page text bounds pass. The warnings are underfull boxes
and the bundled lineno UTF-8 warning, with no undefined references or overfull text.
The first PDF attempt raced case-image generation. I verified the completed PNGs
and the sequential rebuild succeeded. Nineteen focused authoring tests pass.
The reusable bibliography retains the original 98 entries and seven new
reflection/evaluation/video entries, and sources moved out of the main body remain.

Kit checks at the delegated candidate passed 849 tests with nine image checks
unavailable. The parent adds the complete fixed-panel loss-episode CSV,
credential/allocation/symlink refusal stress checks, distinct signed-build
identities and accepted-file context preservation. All 55 v5 regressions pass.
After the supported-runtime failure I installed Node 24.22.2. All 18 SDK
tests pass with zero skips, including real startup with locally rejected inference in an owned
tmux context. I performed no model/provider inference.
Restoring the unavailable local runtime exposed colliding parallel APK key
names. Distinct Git/BusyBox signing identities fix the naming collision
without bypassing signatures. The candidate rebuild is not an accepted v4 image.
Actual current-image qualification, complete source-bound gate evidence and
independent assessment remain separate, and original v4 receipts are historical.
The first exact-head assisted review found one moderate fidelity mismatch:
function-AST comparison missed weakened module/class constants. The corrected
policy freezes complete accepted Python test files, allows additions in new
files and preserves E's specification-bound exception. Module/class/fixture
and addition regressions pass. The original finding and sampled-review limits
are retained, and the review is not recast as independent human peer review or collection approval.

### Reproduce the Revised Assets

Install the named review tools with pip in a task-local environment and
jscpd 5.4.1 locally with npm. The figure run used Matplotlib 3.11.2.

```bash
node anc/revise_diagrams.mjs
node anc/export_diagrams.mjs
python3 -B -m unittest discover -s anc -p 'test_*.py' -q
python3 -B anc/check_paper.py --normalise-bibliography
tectonic main.tex --keep-logs --keep-intermediates --untrusted
```

Run case-image regeneration to completion before compiling, not concurrently.
The source-only historical metrics command is, from the repository root:

```bash
cd docs/capstone/thought-leadership/everything-but-the-software/anc
python3 -B -m review_metrics \
  --revisions 9ef7e40fa6b7d34792f2817ad0a19d2ac16eabd1 \
    29c6b512f5e68733bb2cc1882343db39f5eb2cad \
    9b74ac8daaec2a880172e43161b37ac7f2c3f801 \
  --jscpd /absolute/path/to/jscpd-5.4.1 \
  --out /new/external/review-metrics.json
```

This creates a new diagnostic file and refuses overwrite. The committed sample's
semantic annotations are a separate assisted step, not automatic truth labels.
No arXiv upload, employer clearance or scientific acceptance is implied. The
official [31 October 2025 arXiv CS moderation notice](https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/)
was inspected: this work is an original case plus prospective protocol, not a
review/position paper re-labelled to evade prior peer-review requirements.
Moderator and venue decisions remain theirs.

## Frozen Experiment Review and Revision 1 November

Work execution: Complete for the manuscript revision and conceptual figures.
Assessment: scoped assisted review, not independent human peer review,
statistical certification or venue acceptance. No venue policy was supplied.

### Evidence Inspected

* Current [manuscript](./main.tex), its experiment/discussion/data-availability
  sections, previous review, bibliography consistency and authoring tools.
* The kit at execution source
  `e8707ecc8965d3f81f5142a2603042bfca1aab15` plus manifest-only commit
  `03c50856838b539780d57216af2a4cf6744187d7`:
  [canonical protocol](https://github.com/jmservera/ama-thought-mve/blob/03c50856838b539780d57216af2a4cf6744187d7/protocol/pilot-estimation.md),
  [machine-readable decisions](https://github.com/jmservera/ama-thought-mve/blob/03c50856838b539780d57216af2a4cf6744187d7/protocol/pilot-estimation.json),
  [freeze manifest](https://github.com/jmservera/ama-thought-mve/blob/03c50856838b539780d57216af2a4cf6744187d7/protocol/freeze.json),
  contract panel, configured budget, active retention/model/cost analyzer
  and focused regressions. Historical root design/hypothesis pages explicitly
  defer to this canonical protocol.
* Complete attached `osf-v4-2026-10-31.tar.gz`: freshly downloaded checksum
  matches `1a42fac40a4f1aa82df59c8c3f7f8d6dce37d22502c5952c398362ac63d6bd65`.
  Archive member listing inspected; this is not an exhaustive readback of
  every internal evidence file or live OSF verification.

Full-text support here means I inspected protocol and code that support the
stated design. It does not mean the experiments occurred. Historical test
totals and owner acceptance are inspected records; I did not reproduce runtime
acceptance. I did not inspect the private paid datasets and transcripts or the
runtime image, and I did not independently reverify earlier case claims or any
of the 96 external publications.

### Findings and Applied Remedies

| ID | Priority and manuscript locator | Finding and impact | Applied remedy and remaining limitation |
| --- | --- | --- | --- |
| V4-1 | Major: Abstract; experiment status; Design | Paper described twelve single-model runs, CLI 1.0.103 and 2,500 credits, conflicting with frozen v4. | Reconciled eighteen runs, three models, CLI 1.0.105/SDK 1.0.28, 300,000 nominal envelope and operational soft buffers. No frozen source changed. |
| V4-2 | Major: Design; Pre-run decisions; Data availability | Local execution, missing-feature/evaluator decisions and independent review were incorrectly described as wholly pending; the kit was called private. | Described public packet, bounded container tools, withholding, rollback/continuation and owner-reviewed resolutions. Preserved missing prospective OSF update, operational gates and absence of independent scientific acceptance. |
| V4-3 | Major: Measures; Analysis; precision limits | Paper promised comprehension and HIR/IDR outcomes excluded or deferred in v4 and obscured per-model sample size. | Marked scope accurately, retained assistance logging, explained per-model primary frames and two-run uncertainty. Eighteen trajectories are not eighteen observations in each model contrast. |
| V4-4 | Moderate: Protocol/measurement figures | Quality and cost were buried in dense prose; final correctness could be mistaken for decay control. | Separate H1 coverage, H2 prior-contract loss/recovery and H6 retained-behaviour CR1; show all-attempt delivery/CR1 cost and missingness. Test-weighted scores remain correlated proxies. |
| V4-5 | Major: Discussion, Projected cost of omitting consolidation | No measured long-run cost of inaction exists; predicting a dollar saving would fabricate evidence. | Added explicit assumed sensitivity equation, null/no-payback alternative, break-even and credit-only table. This is not a registered endpoint, fitted forecast, dollar conversion or observed saving. |
| V4-6 | Remaining scientific limitation: Design/precision | B-A buys more resources; B-C changes editing/tests/notes as well as refactoring. Two runs/arm/model, one suite and one CR1 cannot establish general maintainability. | Limitations retained and made visual. A matched-resource/mechanism-isolating or larger study needs separate prospective authorization. |

### Quality and Cost Interpretation

H1 uses final `P10` coverage of all 127 scheduled feature contracts.
H2 tracks unchanged contracts that passed at an earlier `P`, using feature and
post checkpoints, at-risk denominators and retained loss episodes. A contract
that never passes counts as an acquisition failure, and a later repair does not
erase a recurrence. H6 requires all 15 CR1 contracts to pass, and every feature
contract to have passed before CR1. An unknown observation does not
automatically count as a failed contract.

Actual AI credits from all attempts are reported separately for delivery
through `P10` and for CR1, and include failed sessions and infrastructure
retries. Missing billing is unknown and is not recorded as zero. A low-cost
failure is not efficient. Tokens and elapsed seconds are separate measures.
Compatible reference gaps, complexity, duplication and lint serve as
descriptive structural proxies and do not measure comprehension.

The explanatory scenario assumes a consolidation investment of `k=5` credits per
feature cycle and a relative later-feature premium that grows by `delta`.
Net A-B cost is `delta*N*(N-1)/2 - k*N`. With `delta=0` the investment never
pays back, `delta=0.5` breaks even at 21 cycles and `delta=1` at 11. These
arbitrary parameters expose assumptions and counterexamples and are not
preferred estimates. At ten cycles even the last scenario has not paid back.
Nothing supports an empirical 40-feature forecast, a human-work saving or a
dollar conversion.

### Validation

The four focused modules `test_pilot_analysis.py`, `test_analysis.py`,
`test_measurement_integrity.py` and `test_study_report.py` passed at the frozen
source plus the separate manifest: 593 tests, zero reported skips, no model
sessions. They check constructed endpoint, missingness and cost behavior. They
do not test a collected study or audit full runtime and access.
The initial global-Python run failed because the isolated child Python could
not import the user-installed pytest. Restoring the kit's configured dependencies
with pip in an external virtual environment fixed this environment failure,
and no frozen source was patched.

The final source compiles with Tectonic 0.17.0 to a 51-page PDF. All-page
text bounds pass. I rendered the three changed infographic pages (26, 31 and 38)
and inspected them at page scale: nothing is clipped. The build reported no
overfull boxes or undefined references. The engine's standard UTF-8/inputenc
warning is retained and is not a scientific defect.
The structural checker passes, including 96 matching bibliography entries
and explicit deferred-results switches. All eleven existing paper-tooling
and conceptual-figure tests pass, including native regeneration,
editable bindings and source/export hashes for five figures. I separately
checked the exact allocation/panel, the planned-resource arithmetic and all
nine sensitivity-table cells against the frozen inputs.

A separate read-only scientific-agent critique of the revised experiment,
economics and figures found no high-confidence substantive protocol mismatch.
Its one minor finding, a stale work-in-progress status, is corrected here.
That critique is assisted checking and is not independent human peer review.
The original historical critiques remain unchanged. I consulted the capstone
Section D criteria for reusable substance, craft and dissemination, and infer
no rubric score or dissemination/publication acceptance.
The user authorized a repository PR for the revised paper. External
scientific submission, OSF mutation and data collection were not authorized.

This review performs no paid experiment and no full container/runtime audit.

## Repository Metrics Refresh 29 October

The [retained snapshot](./anc/repository-metrics-2026-10-29.json) records
GitHub API retrieval from 17:38:52 to 17:39:47 UTC and document/churn
measurements at `origin/main` commit
`9b74ac8daaec2a880172e43161b37ac7f2c3f801`. It excludes the continuing
paper branch's unmerged edits from default-branch metrics.

| Metric | Captured status |
| --- | --- |
| Merged PRs | 314 overall; 262 since 15 October |
| Post-case merges | 79 after the pinned case integration; 75 on 25-29 October |
| Issues | 211 total: 136 open and 75 closed |
| Other PR states | 11 open; 19 closed without merging |
| Current log | 458 dated entries; 69,352 entry words; 207 hedge matches |
| Whole-file words | Index 12,535; log 69,465; BRD 43,410; PRD 48,094 |
| Combined document volume | 173,504 words, not measured session input |
| Retained automated score | 77/100; A4 implementation completeness 5/5 |

The historical 183 merged-PR count is reconciled and not silently replaced.
Its pinned commit is timestamped 24 October at 16:19:38 UTC, while PR #445
records that same commit's integration at 16:19:39. The exact Git-time
cutoff gives 182. Counting through the integration gives 183, and the whole
15-24 October UTC calendar window gives 187. The snapshot retains every
window and selected PR metadata so you can check the distinction.

The post-case first-parent heuristic counts 71 integrations, separate
from the 79 GitHub merges across branches. Its source/test/tracking
additions are 11,907/31,126/181,261 lines, and tracking/source additions
are 15.22. No complexity, live usability or cost outcome was measured.
The score is the retained 17:12:55 UTC assessment of `0717be24`. It is neither
a new assessment of `9b74ac8d` nor proof of a working deployment.
The main PDF's dated follow-up, conclusion and data-availability statement
carry these boundaries. Original case tables, figures, pilot and
unresolved author decisions remain unchanged.
The refreshed manuscript has approximately 17,450 main-body words and
96 matching bibliography entries. Snapshot consistency checks, all four
paper/diagram regressions and the structural checker pass. I ran no live
journey, experiment or hosted acceptance check.

## Editorial and Visual Revision 29 October

The visual reference was
[Jiang et al., v1](https://arxiv.org/html/2608.14036v1), especially Figure 1's
separation of experimental pipelines. I inspected both pipeline panels. Its
reported effects and taxonomy are not transferred to this paper, and none of
its artwork was copied. The revision adopts one communication principle: one
scientific distinction per figure.

| Figure | Purpose | Evidence boundary |
| --- | --- | --- |
| [State inheritance](./fig-state-inheritance.excalidraw) | Show software and instruction state surviving a fresh session | Conceptual paths, not measured error propagation |
| [Pilot design](./fig-pilot-design.excalidraw) | Compare A/B/C, budgets and mutation permissions | Prospective ten-feature protocol, not execution evidence |
| [Contract states](./fig-contract-states.excalidraw) | Separate acquisition, inherited loss and recovery | Logical states, not frequencies or fabricated trajectories |
| PF1-PF3 | Plan retention, CR1 and resource visualisations | Await actual pilot data and frozen analysis rules |

The revision also fixes four wording problems. Lexical matches were called a
share of statements, a ratio used an unmeasured near-zero denominator, blanket
honesty claims needed qualifying, and a proposed prompt was described as
already used. The
same-release evidence link, independent mechanism audit and pilot runner
decisions remain open and are not resolved editorially.

Excalidraw sources are the editing authority, with stable semantic element
IDs, bound labels and arrows. Edit them in a compatible local editor or the
approved Microsoft instance at <https://aka.ms/excalidraw>, and avoid third-party
drawing services. The offline exporter uses the actual Excalidraw 0.18.1
library in a local browser. It never uses a hand-written SVG approximation, never
rewrites an edited source and blocks external HTTP requests.

The [export receipt](./diagram-exports.json) binds each source to its native
SVG and 3x PNG with SHA-256 hashes, renderer/browser versions and dimensions.
LaTeX uses the PNG. Future edits start from the Excalidraw source, never from a
PDF export or a flattened screenshot. The empirical Matplotlib generator is unchanged.

Run from the repository root with Node/npm, Python and a local browser:

```powershell
npm ci --prefix docs\capstone\thought-leadership\everything-but-the-software\anc
$env:PAPER_BROWSER_CHANNEL = "msedge"
npm run export --prefix docs\capstone\thought-leadership\everything-but-the-software\anc
python -B docs\capstone\thought-leadership\everything-but-the-software\anc\check_paper.py
python -B -m unittest discover -s docs\capstone\thought-leadership\everything-but-the-software\anc -p test_conceptual_figures.py -v
```

For bundled Chromium instead of installed Edge, install the browser with
Playwright and leave `PAPER_BROWSER_CHANNEL` unset. The export script accepts
an optional output-directory argument for isolated validation. The locked
toolchain uses available esbuild/Playwright releases; the Iconify 3.0.1
override avoids an upstream dependency requesting unavailable
`tinyexec@^1.3.1`. No registry or security setting was bypassed.

Compile from this package directory with `pdflatex main.tex` twice, or
`tectonic main.tex --keep-logs --keep-intermediates --untrusted`. Tectonic
resolves cross-references automatically. From the repository root, you can
also run the Bash helper:

```bash
./tools/update-pdf.sh
```

The helper calls `tectonic` from `PATH` and writes the PDF, logs and
intermediate files into this package directory. It resolves the package path
relative to the script, so it does not depend on the current working directory.

The existing
`check_paper.py --check-latex-log` expects a pdflatex-style output marker.
This revision instead checks the actual Tectonic log and rendered PDF.
The four new tests cover native shape/text bindings, exact source/export
hashes, full 3x raster dimensions, isolated re-export without source
overwrites, impersonal narrative, explicit pending plots and the unchanged
no-results switch.
The older shell-tooling tests require POSIX and do not validate figure
rendering.

Earlier dated sections below are historical records. Their source counts,
toolchain limits and validation claims do not describe draft v7.

## Judgment and Skills Source Revision 29 October

GitHub Copilot CLI assisted this scoped edit using the scientific-paper
writer/reviewer behavior. I retrieved and read both owner-selected sources
on 2026-10-29. Coverage includes the complete Anthropic article and the
arXiv v1 main text, references, Appendices A-C, prompts and numbered tables.
Table cells missing from simplified web output were read from the primary
HTML. I read figure captions and descriptions but did not assess the figures
visually. I did not inspect the technical PDF linked separately from the
Anthropic article; the citation identifies the article and not that PDF.

### Source Support and Qualifications

| Citation | Inspected locator and support | Applied role and boundary |
| --- | --- | --- |
| `herdagdelen2026judgment`, [How AI agents shape experts' judgment calls](https://www.anthropic.com/research/agents-judgment-calls), 2026-10-27 | Study design; Results: 50 agent-using professional analysts matched randomly assigned preferences on 86% of four analytical choices. Our study's limitations: deliberately strengthened preferences, one farming-analysis task and model. What this means: independent judgment cannot be inferred from sign-off alone; alternative designs are proposals | Discussion, "What remained mine in this case", qualifies formal approval as a proxy for independent judgment. The 86% does not cover all five decisions, estimate coding behavior or describe Zava North Homes. No proposed safeguard is declared effective |
| `jiang2026skills`, [Demystifying Agent Skills: Why They Work--Until They Don't](https://arxiv.org/html/2608.14036v1), preprint v1 | Sections 1, 3.3 and 5.1-5.3 distinguish procedural skills from workflow histories and examine matched representations, operational gains and failure boundaries. Section 5.5 separates exact-ground-truth access from downstream success. Section 4 and Appendix A.2 explain evidence-linked trajectory analysis and limited human validation | Background, Constructs, Chain of evidence and Learning evaporation: skills can stabilise procedures, but availability/access does not establish correct application. The study does not test repository instruction growth, explain the AMA failure or validate its five mechanisms |

These are full-text-supported paraphrases of the inspected passages and are not
replications. I found no direct contradiction with the case observations.
Two challenges to broader interpretations stand: instruction
maintenance can help instead of merely adding debt, and nominal human approval
does not ensure independent judgment. The manuscript states both
qualifications and does not resolve them by asserting a new case finding.
The skills study's paired skill-versus-raw interval includes zero
(Appendix A.3, Table 10). Its matched cost analysis finds workflow memory
more token-efficient than skills (Appendix A.9, Table 13).
The manuscript claims neither uniform benefit nor universal cost savings.

### Methodological Exemplar: Adopted and Deferred

The arXiv study frames a mechanism question and splits representation,
outcome labels, transfer and retrieval into separate comparisons (Section 3).
It then keeps taxonomy construction apart from findings and implementation details
(Sections 4-5, Appendices A-C). Its agent configurations are concrete
framework/model/tool settings. Skills are reusable procedural resources,
not independent actors or model-weight changes.

| Adopted clarification | Manuscript location | What remains for human authors |
| --- | --- | --- |
| Define agent as a configured model/tool/instruction loop and skill as a reusable procedure, distinct from history | Constructs and evidential boundaries | Confirm terminology fits actual historical runtime and skill artifacts |
| Explain that this case's selected-episode interpretation is not the exemplar's matched trajectory/coding pipeline | Chain of evidence and reflexivity | Independently audit O1-O5 and consequential mechanism assignments; no new coding or agreement score was produced |
| Separate absent guidance, misapplication and task insufficiency | Learning evaporation | Recover actual session inputs and access/use traces before attributing a missing lesson |
| Record owner-selected source addition and distinguish retained notes from a skill treatment | Data and analysis; Constructs | Keep the narrative source-selection boundary; a matched history/skill ablation requires a separate study |
| Distinguish outcome-level evidence from independent human judgment | Feedback starvation; Discussion | Check meaningful approval and competing reasons; proposed decision records are not a tested remedy |

The existing RQs and case-plus-protocol structure were retained. I borrowed no
taxonomy, sampling scheme, new control arm, paired run, inter-rater result or
quantitative effect from the exemplar. Its Section 7 and Appendix A.2 also
limit generalisation and disclose sampled/LLM-assisted coding instead of
exhaustive human annotation. The original `critique.md` is unchanged historical
editorial input and is neither a review nor an approval of this revision.

### Validation and Remaining Gates

Run from the repository root with the available system Python; the documented
`.venv/bin/python` is absent locally:

```bash
python3 -B docs/capstone/thought-leadership/everything-but-the-software/anc/check_paper.py
python3 -B -m unittest discover -s docs/capstone/thought-leadership/everything-but-the-software/anc -p test_paper_tooling.py -v
```

Both pass: 95 matching cited, embedded and reusable keys, 1,609 abstract source
characters, approximately 16,426 main-body words and all seven tooling tests.
The optional historical baseline is available locally, and its 10,353-word count
is not this revision's starting manuscript. The abstract, case tables, pilot
design, arms, sample, outcomes and budgets are unchanged. I modified no tools/tests,
figures, PDF, bundle or private study materials.

No `pdflatex`, `tectonic`, `latexmk`, `xelatex` or `lualatex` is available on
PATH. I installed no compiler and rebuilt no PDF, so I claim no fresh LaTeX-log,
rendered-layout or end-to-end PDF review. I did not run the complete
repository publication gate: its preflight invokes `az bicep version`, which
conflicts with the owner's explicit no-az instruction. Paper checks do not
replace that gate. This edit establishes no push, submission, experiment,
registration, independent human peer review or author/publication approval.

## Executive Feedback and Pilot Amendment 27 October

The supplied executive review is editorial input. It neither corroborates the
case independently nor approves an experiment launch. Its paragraph
identifiers below refer to the local extraction, not Word page numbers.
The original review and earlier seven-hypothesis proposal remain unchanged;
the latter is recoverable from the pre-revision source at commit `701dcea`.

### Applied Changes and Open Evidence

| Review point | Applied manuscript disposition | Remaining evidence or action |
| --- | --- | --- |
| Title/construct boundary, P0107 | Retain the title and explicitly define feature-driven decay as a prospectively investigated phenomenon, not an AMA effect | The case does not measure a decay rate |
| Three central questions, P0070-P0074 | Concentrate on retained behaviour, future changeability and resource cost; use H1/H2/H6 only as historical traceability labels | No pilot hypothesis verdicts or powered effect claims |
| Endpoint hierarchy, P0158/P0215 | Name final coverage as the primary practical outcome, retained-contract loss as the primary decay outcome and CR1 as the changeability probe | Reconcile extraction/checkpoint definitions with the actual runner before launch |
| H4/H7, P0074/P0211 | Remove the joint comprehension and half-gap claims from the formal first-pass set; make H3/H5 metrics descriptive too | Do not invent non-inferiority margins or dependent-contrast thresholds |
| Twelve-cluster precision, P0160-P0165/P0214 | Owner chose to keep four runs per arm as pilot/estimation work for feasibility, variation, endpoint behaviour and failure modes | No power/coverage simulation was performed; method boundary checks remain pre-run work, and a later confirmatory study needs a separate precision/replication plan |
| CR1 estimands, P0166-P0168/P0212 | Specify allocated-run success, conservative binary risk-difference intervals, actual failed-session consumption and explicitly conditional successful-run cost | Interval implementation, missingness/event rules and boundary cases require versioned checks before launch |
| Access/evaluator boundaries, P0171-P0178/P0209 | Separate independent suite/oracle/access review from evaluator-feedback policy and require both before exposure | Not performed or frozen by this edit; launch remains blocked |
| Failure/reset/prerequisite/outage policies, P0210 | Keep each unresolved runner branch explicit and distinguish agent failure from missing infrastructure observations | Freeze and verify B/C-after-failure, dependent continuation, retries, outages and missing-data disposition before launch |
| Measurement/runner agreement, P0213 | Keep the retained-contract panel, feature/post-feature checkpoints and reference-gap description; require actual runner/analysis reconciliation | The private kit was not opened, amended or declared in agreement |
| Independent suite/access review, P0216 | Retain as a launch prerequisite, not a completed safeguard | Requires actual independent review and retained access/oracle evidence |
| O1-O5 evidence chain, P0135/P0222 | Add the machine-readable case-evidence index and link it from the audit trail and data-availability statement | Known/reported locators are separated from null release, configuration and execution identifiers; missing corroboration is not fabricated |
| Scorer/sign-in correspondence, P0136 | Preserve chronological coexistence rather than promote it to a same-release contradiction | Dated score, assessed release/scope, deployment and journey records still need linking |
| Mechanism-assignment independence, P0137 | Retain the sole-participant/AI-assistance boundary and explicitly record the unperformed independent assignment audit | Editorial revision is not independent empirical coding |
| Mechanisms versus experiment, P0223/P0243 | State prominently that no pilot contrast manipulates or validates the five candidate mechanisms separately | The pilot estimates complete package differences only |
| Positioning, P0201-P0204/P0218 | Add AutoSaddler, SkillOpt and AgentRx with scoped first-party citations; narrow novelty to interleaved repository consolidation and retention/changeability measurement | Publication abstracts/engineering accounts were inspected, not independently replicated experiments |
| Editorial economy, P0087-P0094/P0220-P0221 | Shorten HVE exposition and the discussion; move practitioner context, Aithena/PhotoCraft detail, seven proposed practices and human-role agenda to the ancillary companion | Specific validity/identification boundaries remain near the methods they qualify |
| Optional extensions, P0224-P0230 | Defer formal fault lineage, early/late change probes, additional suites/models/CRs and matched human/agent steering | No extra sessions or extensions are added to the 212-session pilot |
| Research readiness, P0233-P0251 | Preserve one-suite/model/CR and weak-access limits without turning them into repeated global caveats | No venue compliance, acceptance, registration or human approval is claimed |

### New Positioning Sources

Retrieval date: 2026-10-27. The citations identify the inspected first-party
pages and do not invent author lists or publication venues for linked
papers.

| Source | Inspected support | Boundary |
| --- | --- | --- |
| [AutoSaddler publication page](https://www.microsoft.com/en-us/research/publication/autosaddler-automatic-harness-optimization-with-durable-updates-from-agent-execution-traces-2/) | Abstract: offline optimisation of the agent tooling using failure diagnosis, structured patches and validation-based update selection; page metadata published 2026-08-24 | Agent-led reflection and tooling improvement is prior work, not the novelty claimed for repository consolidation |
| [SkillOpt engineering account](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/) and [publication abstract](https://www.microsoft.com/en-us/research/publication/skillopt-executive-strategy-for-self-evolving-agent-skills/) | Bounded skill edits, held-out validation, retained successful versions and reported transfer; blog metadata published 2026-06-30 | Counterevidence to treating instruction change as inherently harmful; no independent replication or peer-review status is inferred |
| [AgentRx engineering release](https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/) | Guarded executable constraints and evidence-backed first-critical-failure localisation; blog metadata published 2026-03-12 | Supports traceable diagnosis, not an independent diagnosis of AMA; the review's immediately-before-manuscript timing is not adopted |

### Preserved Scope

The twelve-trajectory pilot remains S1, arms A/B/C, four runs per arm,
ten features and CR1. Its ceiling is 212 sessions and 89 agent-hours;
the separately planned calibration stage adds 50 sessions and 20 hours.
The combined ceilings, exposed runtime/model choices, 2,500-credit ceiling
and separate USD 500 statement are unchanged. Affordability and actual
calibrated caps remain unverified. No calibration or experiment was executed
as part of this manuscript task.

The earlier formal right/wrong thresholds are historical proposal material and
are not active seven-test criteria for the pilot. This is a declared prospective
amendment. It does not claim that the private tag, runner or registration has
already changed. Source-level revisions and formatting checks do not satisfy
launch, publication or independent-review gates.

### Validation and Unperformed Work

* The existing paper checker passes with 93 matching cited, embedded and
   BibTeX references, results disabled and 1,658 abstract source characters.
* Using the checker's documented main-body counting method, the source
   decreases from approximately 17,382 words at `701dcea` to 16,064:
   1,318 fewer words, excluding the additional material moved out of the PDF.
   The checker's unrelated configured historical Git baseline remains
   unavailable; this comparison explicitly uses the available revision base.
* Targeted checks confirm the unchanged suite, runtime/resource numbers and
   original O1-O5 case table; the core table contains H1/H2/H6 only.
   The evidence index retains null release/execution identifiers rather than
   supplying fabricated links.
* Tectonic produces a fresh 43-page external PDF with no unresolved
   references, rerun requests, overfull boxes or underfull boxes in its final
   TeX log. The process still reports the separate Windows Fontconfig
   configuration warning. No fresh page-by-page visual review or pdfLaTeX
   validation is claimed.
* No experiment, calibration, power simulation, private-runner check,
   independent suite/access review, preregistration or publication gate was
   performed. The pilot remains not started and launch-blocked.
* This task did not replace the package PDF, regenerate figures, modify the
   private kit, commit, push or submit externally. A separate change to the
   package PDF appeared during final validation and was left untouched.

## Citation Relevance Follow-up 27 October

The bibliography audit's sixteen relevance warnings are addressed by
removing redundant or unsupported citations and stating the role of each
retained source. A methodological precedent, historical framing or tooling
disclosure need not study agentic decay to serve its stated purpose.
These changes do not raise the original audit scores. They establish no new
source verification and are neither an exhaustive re-audit nor independent
peer review.

| Audit key | Applied disposition | Evidence boundary |
| --- | --- | --- |
| `bavota2015quality` | Replace the broad benefit-attribution claim with the study's finding that observed refactorings do not consistently target or remove code smells; separate the Kim citation | A refactoring label does not guarantee improvement; no causal benefit estimate is inferred |
| `bird2014extrinsic` | Identify the Windows/co-installed-application setting and retain it only as a methodological analogy for environmental influences | It neither tests AI-agent configuration nor diagnoses the case's sign-in failure |
| `cockburn2004crystal` | Retain Crystal Clear for incremental team practice, separate it from Hunt and Thomas's tracer bullets, and remove the unverified walking-skeleton attribution | No uninspected page or pinpoint passage is asserted |
| `dora2024` | Retain the primary report alongside the 2025 report as industry background | No mechanism-level or causal finding about this case is attributed to DORA |
| `dora2025blog` | Remove the redundant announcement from the text and both bibliography forms; retain the primary 2025 report | The report, not its announcement, carries the background citation |
| `fakhoury2024ticoder` | Move the citation from the bundled P7 recommendation to a separate test-driven interactive-generation rationale | It motivates making intended behaviour checkable, not the seven-practice package, consolidation or cross-feature retention |
| `gamma2025syntax` | Remove the unverified stochastic-evaluation remark from the mechanism argument; retain the episode's documented testing topics in practitioner context | Show notes are not a transcript or evidence that deterministic tests are unreliable or the case's scorer failed |
| `harvey2024dora` | Remove the redundant announcement from the text and both bibliography forms; retain the primary 2024 report | No separate evidentiary weight is assigned to the announcement |
| `heander2026codehealth` | State the observational review-cost/batch-fix result and its measurement role | It does not test scheduled consolidation or establish agent-caused decay |
| `hoque2022thriftydagger` | Identify robotic imitation learning as a cross-domain measurement precedent and attach the citation to incidence, action and switching-cost distinctions | Coding-tooling effectiveness and software-decay findings are not borrowed from it |
| `karpathy2025vibe` | Give the throwaway-project framing its own sentence and citation | An illustrative practitioner position, not empirical support for decay or for the tooling |
| `kassis2026skills` | Retain the actual assistance-tool citation in the generative-AI disclosure and state its provenance-only role | It does not substantiate case findings or the consolidation hypothesis |
| `kelly2019hgdagger` | Identify robotic imitation learning as a cross-domain measurement precedent and attach the citation to takeover/return of control | The proposed HIR definition and study design remain the paper's own |
| `martin2024weprogrammers` | Remove the book from both bibliography forms and rely on the already-cited Product Engineers interview for executable feedback and customer understanding | No unverified chapter or page is supplied |
| `martin2026outcodes` | Remove the inaccessible video and its attributions from the text and both bibliography forms; use the existing Product Engineers interview for the supported practitioner argument | The video's spoken content is not retrospectively declared verified |
| `willison2025vibeeng` | Describe the post's concrete testing, planning, documentation, version-control and review practices with a separate citation | Practitioner accountability, not an experimental comparison or a result on tooling effectiveness |

The original audit remains a historical assessment. Keeping a source for
an explicitly bounded role answers its recommendation. It does not change the
source's topic or its original numerical relevance score.
Other audit findings, including unverified source-specific numerical
passages and unrelated access or attribution notes, are not closed by this
relevance-only follow-up. Publication and human approval gates remain open.

### Validation

* The existing paper checker passes with 110 cited, embedded and reusable
   bibliography keys, results disabled, 1,604 abstract source characters
   and approximately 17,380 main-body words under its documented counting
   method. Its historical Git-baseline comparison remains unavailable.
* A separate pre-edit comparison confirms the abstract is unchanged
   and the experiment protocol is identical after line-ending normalisation,
   except for its source-context paragraph about robotic intervention
   measures. Hypotheses, outcomes, HIR definition, budgets, thresholds and
   study status are unchanged.
* All sixteen original warning keys have a disposition above. The four
   removed keys are absent from manuscript and BibTeX; all twelve retained
   sources remain cited with explicit roles. The original audit is not
   overwritten or re-scored.
* Tectonic 0.17.0 produces a fresh 49-page external PDF with no unresolved
   citations, references or rerun requests. Four small overfull boxes
   remain, maximum 5.295 points, plus one underfull bibliography line and
   the environment's fontconfig configuration warning. This is not a
   pdfLaTeX build or a fresh page-by-page visual review.
* The package PDF, figures, arXiv bundle and private study materials remain
   unchanged. No complete RPI publication gate, commit, push, submission
   or human approval is claimed.

## Industry-Led Revision 27 October

A read-only developmental critique preceded all edits. Three research-agent
lanes investigated historical maintenance, inherited coding errors and chart
data, and instruction context with PhotoCraft. A follow-up checked
longitudinal instruction-file studies. A fresh scoped critique found no
material remaining framing issues. These were assisted editorial and
research passes and not independent human peer review.

The revision changes the argument's order:

* Knight Capital's dormant fault and deployment failure, followed by
   Cunningham's WyCash consolidation account, establish the pre-AI problem.
* PhotoCraft's command coverage and project-authored readiness estimates
   introduce the distinction between completed features and usable workflows.
* Paired repository-history evidence makes errors inherited by later feature
   work distinct from errors carried within a conversation.
* Instruction-file histories and context-file experiments extend maintenance
   to the prompts, skills and notes governing development.
* AMA follows as the traceable trigger for the consolidation experiment.
   The mechanism summary now separates accumulation, transmission, selection
   and correction. It no longer treats every process problem as propagation.

The abstract, research questions and conclusion follow that structure.
The narrative repeats fewer validity disclaimers; specific
sampling, measurement and identification limits remain beside their methods
and in the limitations sections. Software entropy is a maintenance analogy
and not an asserted physical law. Context debt is attributed to prior work.

### Source Checks

All retrievals below are dated 2026-10-27. Locators identify the inspected
source material, not experiments reproduced here. This is a focused source
synthesis rather than an exhaustive or systematic review.

| Source | Inspected support and use | Coverage and interpretation |
| --- | --- | --- |
| [SEC release 2013-222](https://www.sec.gov/newsroom/press-releases/2013-222), 16 October 2013 | Paragraph beginning "According to the SEC's order": 2005 router defect, 2012 incorrect deployment, more than four million orders for 212 customer orders and loss above USD 460 million | Full-text support in the official release. The linked order PDF was not meaningfully extracted. This is a latent-fault, deployment and control example, not a feature-churn rate |
| [Cunningham's original WyCash report](http://c2.com/doc/oopsla92.html), 1992 | Paragraphs on adapting the financial product, revising mature code and consolidating an initially expedient implementation | Original industrial experience account; no controlled cost estimate or longitudinal numerical dataset is attributed to it |
| [Pan et al. v1](https://arxiv.org/html/2610.14768v1), 10 October 2026 | Sections 2.5, 3.1-3.2 and 4.1-4.2, Tables 2-3, and Section 5.1, Figures 4-5: fresh sessions, paired history, inherited-test failures, clean histories and two fault-reuse examples | Full-text support for the scoped claims and chart transcription. ER includes current and prior tests; TR concerns the current task alone. Selected cohorts overlap and are not randomised repairs |
| [Chatlatanagulchai et al. v2](https://arxiv.org/html/2511.12884v2), 9 August 2026 | Sections 4.2.2-4.2.3: sampled post-adoption commits, overlapping edit labels, additions and deletions; Section 5.1: context-debt proposal | Full-text support. The paper associates day-scale updates with project maintenance, not immediate corrective prompt tuning. Edit labels do not measure loaded context or downstream performance |
| [Mohsenimofidi et al. v4](https://arxiv.org/html/2510.21413v4), 5 February 2026 | Section 4.3 and Table 2: 155 files, 77 unchanged after creation; detailed coding of 169 commits in ten high-change files | Full-text support. Add/modify/remove categories overlap; the selected files do not establish a rate for repositories generally. Intent was not coded |
| [Gloaguen et al. v3](https://arxiv.org/html/2602.11988v3), 29 September 2026 | Sections 4.1-4.4, Tables 2-3 and Appendix B: context inclusion, cost, task resolution, instruction-following, length analysis and documentation-removal ablation | Full-text support. Reported 20%/23% average cost increases concern generated files on SWE-bench Lite/CTXbench; resolution differences are non-significant. Length alone did not explain results; useful-context counterevidence is retained |
| [Nigh's GitHub article](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/), 19 November 2025, updated 25 November | "What works in practice" and "Key takeaways": explicit commands, examples, boundaries and iterative additions | Full-text practitioner account, not a controlled evaluation or numerical effect of corrective instructions. Its custom-agent definitions are distinguished from repository-wide context files |
| [Rajasekaran et al., Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 29 September 2025 | "The anatomy of effective context" and long-horizon context sections: brittle prompt logic, exception lists, curation, retrieval and note maintenance | Full-text first-party engineering account; the paper uses its design reasoning rather than a quantified intervention effect |
| [PhotoCraft pinned source](https://github.com/storytold/photocraft/tree/5bb853654196eca807212ff8955ba2eb293071ea) | Scorecard, target-app parity assessment and dispatch-count implementation, checked against the existing dated observation record | Source-level and project-authored support, not fresh application execution. The original source pin and 25 October tracker boundary remain unchanged |

The research lane rechecked Sinha and Laban against the versions inspected
earlier. Their conversation-history results stay separate from repository
inheritance, and I estimated no points from their curves. The Laban version's
39% main-text versus 35% teaser discrepancy remains recorded in the historical
source note below. SlopCodeBench's full-text extraction was still incomplete.
SWE-CI remains supporting context, not a new plotted dataset. Existing
author-verification tasks are not marked complete.

### Published-Data Figures

[published-evidence.json](./anc/published-evidence.json) keeps the source
versions, locators, units, cohorts and transcription notes. The existing
[figure generator](./anc/make_figures.py) can now build all figures, only the
case figures, or only the published-data figures.

* [Inherited-history figure](./fig-inherited-history.png) plots Pan's Table 3
   event-resolution differences and published 95% repository-clustered
   bootstrap intervals. The aggregate, inherited-failure and clean-history
   rows stay visible. Values are transcribed from the paper and not recomputed
   from rounded percentage columns. Nothing is pooled across studies or
   digitised from curves.
* [Instruction-maintenance figure](./fig-instruction-maintenance.png) plots
   78 addition, 32 modification, 19 deletion and ten maintenance labels in
   100 sampled commits. Labels overlap. Add/delete totals combine line-level
   and section-level labels, and maintenance is the remainder of 139 assignments.
   The bars are not distinct-commit percentages and do not form a
   context-degradation curve.

Each caption gives the source, denominator, definition and relevant
conditioning. I inspected the new chart images visually and checked that they
were not blank. I also ran the generator's complete default path in
external scratch, which left the two existing case figures untouched.

### Validation and Reproduction

I installed Tectonic 0.17.0 from its official Windows release into the user
profile and checked the archive SHA-256 against the release metadata:

```text
f61ce51f0b0ade1015b7de7ef368541c5424e9756ecbd0d7af97d6d48030845f
```

The author asked for pip rather than uv, so I installed the plot dependencies
with the existing virtual environment's pip: matplotlib 3.10.7 and
Pillow 12.0.0. Earlier uv download attempts failed. The editor's generic
installer also invoked uv, so the successful installation did not use it.
No project dependency manifest changed. I cancelled a separate PyMuPDF
installation and did not retry it, using the browser's PDF viewer instead.
Context7 tools were unavailable, so official Tectonic documentation and release
metadata supplied the installation information.

The successful commands, from the repository root, are:

```powershell
& .\.venv\Scripts\python.exe docs/capstone/thought-leadership/everything-but-the-software/anc/check_paper.py
& .\.venv\Scripts\python.exe docs/capstone/thought-leadership/everything-but-the-software/anc/make_figures.py --only published
& "$env:LOCALAPPDATA\Programs\Tectonic\0.17.0\tectonic.exe" --untrusted --keep-logs --keep-intermediates --outdir "$env:TEMP\ama-paper-industry-20261027-23e0fd2e" docs/capstone/thought-leadership/everything-but-the-software/main.tex
```

The external PDF has 49 pages. I inspected its title page and the two new
standalone figure images. The browser did not follow PDF page fragments or
expose page controls, so I did not review the PDF layout page by page. The final
TeX log has no unresolved references or rerun requests and no overflow above
ten points. Four smaller overfull boxes remain (maximum 5.295 points), plus one
underfull bibliography line. Tectonic also emits a fontconfig configuration
warning, though the PDF opens with rendered text. This is a Tectonic/XeTeX
build and gives no new pdfLaTeX validation.

The structural checker passes with 114 matching cited, embedded and reusable
bibliography keys and results disabled. The protocol section is identical
to the starting commit after normalising line endings. Transcription,
denominator, image-dimension and nonblank checks pass. Editor diagnostics
report no errors in the changed manuscript, bibliography or plotting script.
The historical-baseline word comparison is unavailable because its configured
Git object is missing. The current approximate body count is 17,277.

Output is under `%TEMP%/ama-paper-industry-20261027-23e0fd2e/`. The package
PDF and case figures remain unchanged against the starting commit. This pass
ran no experiment and made no private-kit modification, commit, push or
submission, and it did not run the complete RPI publication gate. Remaining
venue and external-publication decisions are unchanged.

## Compounding-Error Evidence 26 October

The owner asked for sources and evidence on compounding error in AI and
agentic development. The main background now separates accumulating
failures from an inherited error that makes later work more failure-prone, and
it keeps four kinds of evidence apart instead of treating them as one result.

This was a bounded primary-source check and not a systematic review. Discovery
used the arXiv query `compounding errors coding agents`, with the first 25 of
31 returned records inspected for relevance, plus references from Sinha et al.
Sources after 26 October 2026 were outside scope. The default research skill's
Parallel CLI was unavailable, so I retrieved the primary pages directly.
No manuscript or private study material went to a search service.

The support states below refer to passages the assistant inspected on
26 October 2026. They are neither independent human verification nor replicated experiments.

| Source and inspected version | Claim and genuine locator | Evidence state and interpretation limit |
| --- | --- | --- |
| [Zhang et al., arXiv:2305.13534v1](https://arxiv.org/html/2305.13534), 22 May 2023 | Sections 3.1-3.4: wrong QA answers accompanied by false justifications that the same model often rejects in a separate session | Full-text support for scoped snowballing claims; two 2023 models and QA, not code generation or repository propagation. No forced-wrong-prefix experiment is attributed to this study |
| [Sinha et al., arXiv:2509.09677v3](https://arxiv.org/html/2509.09677v3), 13 March 2026 | Section 3.2 and Figures 5-6: controlled variation of errors in prior histories changes subsequent state-update accuracy; Qwen3 thinking models avoid the effect in this setup | Full-text support, including methods, results and figure captions; synthetic execution task, not a repository-decay estimate. Thinking-model counter-evidence is retained |
| [Laban et al., arXiv:2505.06120v1](https://arxiv.org/html/2505.06120v1), 9 May 2025 | Sections 3.3 and 6.1, Table 1, Appendix F.1-F.2: sharded/concatenated controls, relative performance loss, early-answer associations and answer bloat | Full-text support for the specified comparisons and diagnostic analyses; simulated conversations, not natural-user observations or a defect-specific coding intervention |
| [Pan et al., arXiv:2610.14768v1](https://arxiv.org/html/2610.14768v1), 10 October 2026 | Section 2.5; Sections 4.1-4.2, Tables 2-3; Section 5.1, Figure 5: paired history comparison, downstream resolution costs, selected clean-history subset and reuse of defective string-splitting logic | Full-text support for the scoped numerical and example claims; preprint, short Python maintenance chains and no reproduced application run. Clean-history conditioning is not a randomised repair experiment |

The Laban version reports two different figures: its abstract and
Section 6.1 give an average 39% relative drop, while the Figure 1 teaser
caption says 35%. The manuscript attributes 39% to the main results/Table 1,
and it is a relative drop, not a percentage-point loss or a defect rate. This check does not
resolve which figure the authors intended for the teaser, and it does not
reanalyse the simulation outputs.

I retrieved SlopCodeBench v2 metadata and abstract, but full-text
extraction failed, as did the attempted multi-agent-failure HTML retrieval.
Their existing contextual citations are not upgraded to fresh full-text
verification. SWE-CI and the randomised maintainability study remain contextual
citations that this pass did not newly audit. Numeric claims from other
studies remain under the existing author-verification boundary.

I extracted Zhang's metadata with the citation skill's arXiv parser and
cross-checked it against the primary abstract and full-text pages; the abstract
page confirmed the arXiv DOI. The inspected arXiv metadata gave no journal
reference, so the added citation identifies the preprint and invents no venue.
Both bibliographies include the new entry and pin
the inspected Sinha, Laban and Pan versions. The structural checker passes
with 108 matching cited/embedded/BibTeX keys and results disabled.

The proposed measurement section also adds fault-lineage annotation: a
distinct later failure needs code/diff and execution evidence linking it to
an inherited fault. Repeated failure of the same test counts as persistence
and is not a new propagated error. A matched faulty-versus-repaired snapshot comparison
remains a separately resourced prospective extension. Existing arms, numerical
H1-H7 criteria, sample sizes and budgets are unchanged. I neither inspected
nor executed the private kit.

The external build has no TeX warnings, unresolved references or underfull/
overfull boxes. I inspected the changed background on pages 3-4 and the
measurement note on page 26. These checks do not establish scientific
acceptance. This pass ran no experiment, commit, push, registration or submission.

## Software Evolution Prose Restoration 26 October

At the owner's request, I restored the opening paragraph of "Software that only grows"
verbatim, with its historical narrative and cited estimates.
A separate short paragraph keeps the limits of the evidence and separates
motivating decay as a hypothesis from demonstrating it.
The source checker passes with 107 matching references. The external build
has no TeX warnings, and I checked the restored passage visually on page 3.
The statistics have no new original-source verification, which remains
pending under the manuscript's existing disclosure.

## Subtitle and Decay Measurement Follow-up 26 October

The owner asked to restore *Feature-Driven Decay* and to design
the exercise to measure that hypothesis. The manuscript now includes a
proposed measurement amendment. It makes no claim about the private runner:

* Freeze a contract panel and eligibility map. Track previously passing,
   unchanged behaviour after each feature and again after consolidation/review.
* Record open losses, exposure-normalised density, onset, recurrence,
   recovery and duration. Separate never-implemented behaviour, same-cycle
   post-feature damage, rejected/reset attempts and missing measurements.
* Read loss counts against their risk sets and full functional coverage, so
   incomplete implementations do not look healthy because they have fewer
   contracts to lose. Runs remain the independent analysis units.
* Compare structural trajectories with stage-matched cumulative references,
   which separates required feature complexity from excess deterioration. The
   reference-gap analysis supplements H3 and does not silently replace it.
* Treat final changeability and its decline over time as separate questions. An
   optional repeated core-contract change on disposable early/late snapshots
   needs an additional probe, sessions, budget and prospective approval, and
   it is outside the existing 212-session first pass.
* State rival and disconfirming patterns: stable retention,
   reference-matched growth, acquisition-only benefits and unstable oracles.
   The existing arms cannot identify feature accumulation against a randomised
   no-feature control.

H1-H7 numerical criteria, existing arms, budgets and sample sizes are unchanged.
The H2 count interpretation and new measurement definitions need a versioned
reconciliation with the private kit before fresh runs. No existing tag or
earlier-run label is rewritten, and no new empirical observation is asserted.

The structural checker passes with 107 matching citation keys, results disabled
and a 1,848-character source abstract. Shell-escape-disabled compilation has
no warnings, unresolved references or underfull/overfull boxes. I inspected the restored
title, measurement pages 25-26 and the updated pre-run table visually.
An editor diagnostic still asked for a cross-reference rerun from its separate
build state. The clean external validation log does not show that request.

The workspace PDF hash changed from
`15eaff90df23a95ff528fe23d923ebcc40e20bbf79c5e8b49955fa982ac3c6d7`
at intake to
`2df76caf48edf2e1e866e11fa115e310c78d9eb65bad06990fbc37d61774160f`
during editing. The pre-explicit-build backup has the latter hash, so it is
not a byte-preserved intake copy. I reverted no PDF. Existing staged work
remains staged, and I did not commit, push, register or publish.

## Developmental Revision 26 October

The owner authorised the recommended manuscript revisions on the existing
branch while preserving other uncommitted work. The revision:

* Replaces the causal decay subtitle with delivery-usability divergence and
   consistently qualifies the unmatched score/release/capability comparison.
* Shortens background and repeated practitioner discussion, moves selected
   external repository observations to an appendix and places case validity
   beside the five candidate mechanisms. The full rival register stays in
   an appendix, and practices sit in the discussion.
* Names H1 as final functional coverage, separating acquisition, retention
   and repair. H5's wording describes bounded overhead and late-feature savings
   and makes no monetary payback claim. Endpoints, thresholds, arms, sample and budgets are
   unchanged.
* Adds the intended procedural sequence and an unresolved pre-run decision
   table covering evaluator feedback, failed-feature continuation, outages,
   analysis, H4/H7, resource caps and human-help telemetry. The table does not
   describe verified runner behaviour or newly approved scientific choices.
* Normalises Figure 1's lower panel to daily hedge matches per 1,000 words.
   Zero-word days have undefined density instead of a fabricated zero rate. Figure 2
   uses dashed hypothetical links, marks context effects unmeasured and
   separates proposed human checkpoints from the consolidation experiment.
* Shortens the human-learning research agenda and AI-assistance disclosure
   while retaining human responsibility and verification limits. Earlier
   revision histories and source-access limits below are preserved.

The body is about 14,500 words, down from approximately 17,454, using the
existing checker: introduction through conclusion, including tables but
excluding abstract, references and appendices. Case methods begin on page 5
of the external build rather than page 8 of the prior build. The 107 cited,
embedded and reusable bibliography keys still match. All seven existing
tooling tests pass. Final shell-escape-disabled compilation has no warnings,
unresolved references or underfull/overfull boxes. I inspected whole-document contact
sheets and full-size changed figures, title, hypothesis and pre-run pages.
Visual and structural checks do not establish accessibility
conformance or scientific acceptance.

The preserved workspace PDF's SHA-256 is
`2e97f6eeea3ef2aa30817fd953fa888bd22ddfa75b3a86d50aa4a22c4f481cdc`,
unchanged between the preservation check and build validation. Existing
staged README/log changes remain staged. This revision stages,
commits, pushes and submits nothing. The full RPI publication gates and independent
exact-head assessment have not run.

The release-linked case evidence package, original-source checks, actual
private-kit provenance and information boundaries, pre-run statistical
decisions, registration and publication permissions remain unresolved.
I fabricated no source capture, independent corroboration or approval.

## Historical Status Before 26 October

The repository-context revision below is the latest source record. It adds
bounded observations from Aithena, Squad and PhotoCraft without changing the
title, subtitle, author affiliation or H1-H7 experiment. AMA remains the
single principal case, and the selected examples are not comparative results.

The table-flow revision below supersedes earlier confirmatory first-pass
wording and PDF-handling instructions. The title and subtitle are unchanged.
The four-runs-per-arm first pass is now explicitly exploratory, and any later
confirmatory study needs a separately specified prospective analysis plan.

The 25 October author clarification supersedes the earlier method and study
descriptions below. Execution is paused. The author reports tagging the protocol;
the exact snapshot and completed registration remain to be supplied. Earlier
runs keep their original labels and timestamps and will not enter the fresh
first-pass analysis. No study results are reported.

The separate private experiment kit is the intended study record. The ancillary
MVE notes here are earlier proposals and not the frozen or registered protocol.
Do not overwrite the tagged kit with these copies. Registration preparation is
deferred, and public release and external deposits still need permission.

The source is now the critique-revised draft v4. The earlier workflow did not replace
the PDF with its external build or refresh the arXiv bundle. A separate
workspace build regenerated the PDF during editing, and the owner then explicitly
chose to leave that current PDF untouched. Pre-edit PDF preservation cannot
be claimed. The external compilation is validation output and not a submission
package.

## Reader Layout and Developmental Revision 25 October

This historical revision narrowed the subtitle to delivery-signal/usability
divergence, adjusted the narrative and table placement, and kept the
exploratory protocol without changing its hypotheses, thresholds, budgets or
sample. Its external 43-page PDF was reported without compiler warnings or
unresolved references, and rendered-page and table-proximity checks were done.
The structural check recorded 104 matching references. The later table-flow
revision below supersedes this build's layout and PDF evidence.

## Repository Context and Hypothesis Revision 25 October

The author clarified that the hypothesis predates AMA. Aithena's maintenance
difficulty is retrospective author testimony and not an independently measured
complexity trajectory. The expectation that HVE's research, plan critique
and implementation review would improve on simpler workflows is an
expectation and not an established framework advantage.

The [minimised observation record](./anc/repository-observations-2026-10-25.json)
keeps source SHAs, queries, counts, sampling rules, claim locators and
exploratory rivals/predictions. It excludes reporter identities, raw issue
bodies, attachments, private standards and proprietary application material.
I inspected public project code narrowly and did not execute it. I selected no unspecified
Microsoft Office clone and treated none as evidence.

| Source | Inspection boundary | Supported observation and qualification |
| --- | --- | --- |
| [PhotoCraft](https://github.com/storytold/photocraft/tree/5bb853654196eca807212ff8955ba2eb293071ea) | Pinned `main`; README/agent instructions, CI, architecture, scorecard, gap/parity records, menu-count implementation; 15 declared bug reports and two selected PR bodies | A Photoshop reimplementation, not the entire Adobe suite. Its 631/631 menu count checks recognised command/tool/UI paths, not execution of every reference workflow. Its own 10 October assessment distinguishes about 76% breadth from about 45% readiness; these are historical, partly subjective project estimates |
| [Aithena](https://github.com/jmservera/aithena/tree/f27aa2e9f949ea76f2a437249e68b52670a22835) | Pinned `dev`; Squad records, verification script, six selected audit reports, two narrow source traces and all open-PR metadata | Review/retrospective/quality-gate machinery exists. Active preflight tests coexist with unconditional Phase 3 scenario skips; the indexer acknowledges in a `finally` block. No runtime failure, lost document or measured maintainability effect is claimed |
| [Squad](https://github.com/bradygaster/squad/blob/481c944596abfa2053e2acd88d765639f994d795/README.md) | Corrected repository, pinned `dev` README | Persistent learning and human-led accountability are explicit; current documentation is not historical-version evidence for Aithena |

At the 25 October 2026 22:52:26 UTC count query:

| Tracker category | PhotoCraft | Aithena |
| --- | --- | --- |
| Open issues excluding PRs | 2,060 | 34 |
| Open issues with exact `bug` label | 212 | 3 |
| Closed issues | 2,604 | 705 |
| Open PRs | 1,091 | 35 |
| Merged PRs | 3,189 | 842 |
| Closed-unmerged PRs | 610 | 240 |

The complete PhotoCraft open-PR inventory contains 49 drafts. REST's combined
`open_issues_count` is not a bug count. The bug-body sample consists of the
ten newest and five oldest open bug-labelled issues by creation time, so it is not a
representative defect sample. Selected reports cover printing, PSD opening,
platform differences and network-share prompts; the latter explicitly says
the file saves. Some reports are duplicates or need clarification. Issue
labels, open state and pinned source are different kinds of evidence, and
the separate live API requests are not an atomic snapshot.

The record keeps the counter-evidence: meaningful corpus and
layer checks, fixed gaps and large merged output; PhotoCraft PR #9552's
helper-consolidation proposal; and 34 of Aithena's 35 open PRs labelled
`dependencies`, with the remaining PR supplying benchmark evidence. Queue
size does not measure architectural decay or unfinished feature count.
PhotoCraft's own third-party export-oracle gap is narrower than an absence
of behavioural tests. Its scorecard/gap documents disagree on a corpus
denominator, so I calculate no success ratio from those fields. I do not
present historical performance and parity estimates as fresh measurements.

The manuscript derives a candidate distinction between issue-level
correction and cumulative system steering. A separate matched-resource,
independent-oracle comparison could separate human-specific judgement,
agent-led steering and coverage explanations. The manuscript establishes no
superiority, human necessity, defect incidence or causal effect, and it does
not silently redesign the tagged consolidation experiment. Selection after the
author's experience, alpha-stage scope, adoption/detection and review
capacity remain alternative explanations.

Both bibliographies gain three source references. The Hypothesis
Generation assistance is disclosed under the existing Scientific Agent
Skills citation and gives no independent empirical verification.

### Repository-Context Build Record

The inspected external build is `/tmp/ama-paper-repository-context-5wfzbv/`.
It has 44 pages and 107 matching cited/embedded/BibTeX references, with
results still disabled and the source abstract unchanged at 1,676 characters.
The seven existing tooling tests pass. Final shell-escape-disabled
pdfLaTeX passes have no warnings, unresolved references or underfull/overfull
boxes. A breakable ancillary-file locator fixes the initial text overflow.

I inspected whole-document contact sheets and full-size new/contextual, discussion,
data-availability and table pages. Two selective barriers and
a nearby reference to the additional-rivals table keep tables near their
discussion after the added text. The final auxiliary labels and extracted references give:

| Table | First discussion | Table page |
| --- | --- | --- |
| 1: Evidence audit trail | 10 | 11 |
| 2: Timeline | 11 | 12 |
| 3: Period metrics | 11 | 12 |
| 4: Churn | 13 | 13 |
| 5: Within-case contrasts | 14 | 14 |
| 6: Mechanisms summary | 16 | 16 |
| 7: Working theory | 16 | 16 |
| 8: Protocol summary | 22 | 22 |
| 9: Hypotheses | 23 | 23 |
| 10: Recorded rivals | 30 | 31 |
| 11: Additional rivals | 32 | 32 |
| 12: Appendix practices | 41 | 41 |

This build replaces `main.pdf` under the existing owner permission, and the earlier
build maps below are historical. The title page keeps the requested role
and affiliation without an email address. The arXiv bundle is not refreshed.
This session did not modify unrelated work, run the full clean-candidate
publication gate or obtain an independent exact-head assessment. Concurrent shared-branch
activity included the source changes in commits, but this editing session did not
commit, merge or push. The final build record and PDF remain local changes.
This build does not establish publication approval or external submission.

## Table Flow and Developmental Revision 25 October

The owner authorised continuing on the existing PR branch, preserving other
uncommitted work and replacing `main.pdf` with this revision's build.

* Ordinary tables now use `[!htbp]`, with selective `placeins` barriers between
  the case, mechanisms, practice, protocol, discussion and conclusion.
  The mechanisms summary follows its introduction, and the practices table stays
  in its appendix. The revision forces no `[H]` placement and relocates no historical evidence.
* A linking passage separates the missing identity/staff configuration from the
  future-changeability hypothesis. The manuscript does not claim that consolidation would
  have prevented the observed sign-in failure.
* By owner decision, the first pass is exploratory. Existing arms, thresholds,
  budgets and sample sizes are retained. H4 accuracy non-inferiority and H7
  endpoint/zero-or-negative-gap policies stay explicitly unresolved. Binary
  intervals, model fallbacks, failure disposition and any later confirmatory
  hierarchy need prospective decisions and no invented editorial fixes.
* A compact evidence-package requirement names the missing score scope,
  release/configuration and failed-journey linkage. The revision claims no new API captures,
  same-release verification, registration or study results.
* Universal attention and causal scrutiny claims are bounded, and repeated
  protocol qualifications are shortened using cross-references.
* Both bibliographies include Kassis et al., *Scientific Agent Skills*,
  doi:10.48550/arXiv.2609.00065, for the revision method. I checked the latest arXiv
  record on 25 October 2026 (v2, five authors, no published
  journal reference shown), and the citation uses the unversioned DOI.

The earlier revision and validation records below remain historical. They
do not establish this revision's PDF placement or publication gates.

<a id="current-source-reconciliation-25-october"></a>

### Table-Flow Build Record

The external build at `/tmp/ama-paper-tableflow-aprrsq/` has 42 pages.
Final shell-escape-disabled pdfLaTeX passes report no warnings, unresolved
references or underfull/overfull boxes. The structural checker passes with
104 matching references, results disabled and a 1,676-character source
abstract; all seven existing paper-tooling tests pass.

I inspected rendered whole-document contact sheets and full-size table pages.
The revised PDF replaces `main.pdf` with owner permission, and the
arXiv bundle is not refreshed. Auxiliary labels and extracted PDF references
give these locations:

| Table | First discussion | Table page |
| --- | --- | --- |
| 1: Evidence audit trail | 9 | 10 |
| 2: Timeline | 10 | 11 |
| 3: Period metrics | 10 | 11 |
| 4: Churn | 10 | 11 |
| 5: Within-case contrasts | 12 | 12 |
| 6: Mechanisms summary | 14 | 14 |
| 7: Working theory | 14 | 15 |
| 8: Protocol summary | 20 | 21 |
| 9: Hypotheses | 22 | 22 |
| 10: Recorded rivals | 29 | 29 |
| 11: Additional rivals | 29 | 30 |
| 12: Appendix practices | 39 | 39 |

The larger protocol and additional-rivals tables use nearby dedicated pages.
This layout inspection is not an accessibility certification, independent
empirical review or verification of missing source evidence. Existing
unrelated staged/unstaged/untracked work is preserved. The complete
clean-candidate publication gate and independent exact-head assessment
have not run, and the record claims no commit, push or external submission.

## Critique Revision 25 October

The owner selected author mode, the existing LaTeX format and preservation of
the tagged experiment. Work continued on the current open-PR branch, keeping
the existing PDF and unrelated worktree changes. It changed no private study files,
application behaviour, cloud resources or experiment runs.

| Critique area | Treatment in draft v4 |
| --- | --- |
| Central claim and causal title | Adopted the single-loop observational subtitle and aligned abstract, three research questions and three contributions to divergence, candidate explanations and a prospective test |
| Case methodology | Added operational construct boundaries, a five-row observation--interpretation--proposition audit trail, reflexivity and bounded within-case/negative-case contrasts; no new dataset or independent coding is claimed |
| Mechanisms | Labelled the five explanations as candidates and added a definition, indicators, counter-evidence, rivals and experimental implication for each in an appendix |
| Practice and practitioner material | Reduced the main discussion, moved extended accounts, informal observations and detailed practices/checklist to appendices, and labelled numerical practice limits as untested heuristics |
| Rival explanations | Expanded the matrix to distinguish migration, owner decisions, environments/dependencies, scope, acceptance coverage, models, budgets, context/rate limits, ambiguity and prototype debt, including untested alternatives |
| Protocol interpretation | Added a one-page summary, explicit package-level estimands, endpoint hierarchy, small-sample/cluster limits, multiplicity limits, unverified blinding/access and missing-data rules, credit-versus-currency and CR1 withholding boundaries |
| Proposed redesign | Not adopted, by owner decision: C remains read-only, no equal-total-budget comparison is added, H1 retains priority and H6 remains the changeability probe. Hypotheses, thresholds, budgets, sample and prior-run labels are unchanged |
| Additional empirical work | Not invented: power simulations, independent case coding, annotation agreement, suite/access review and actual registered study results remain unperformed or unverified |

An owner-requested follow-up restores a substantive Beck paragraph in the main
practitioner conversation. It ties care for code and tests, learning through
product use, preservation of future options and reflective delegation to the
consolidation hypothesis. This is conceptual motivation and gives no evidence that the
consolidation procedure works. The longer practitioner accounts remain in the appendix.

The revision makes the case and protocol's limits more explicit, but it does not
claim to resolve every methodological concern in the critique. New
evidence tables and protocol limitations add content despite the cuts to
repetitive practitioner and practice material. The record claims no overall word-count reduction
or venue page-limit acceptance.

### Citation Corrections and Additions

Primary source retrieval on 25 October supports six new references, now 103
matching entries in the embedded and reusable bibliographies:

* [Why AI Agents Still Need You](https://arxiv.org/abs/2506.12347v3),
   accepted at ASE 2025: observed collaboration, not a randomised estimate of
   optimal human intervention
* [CRBugBench](https://arxiv.org/abs/2610.13668v1), 9 October 2026 preprint:
   review-agent evaluation, including complex/non-local and proprietary-context
   limitations; only metadata and the abstract were retrieved successfully
* [Building to the Test](https://arxiv.org/abs/2606.28430v1), 26 June 2026
   preprint: an unchanged partial behavioural oracle can pass a demo while
   the requested reusable library is unused or absent. This is not evidence
   that the tests were weakened
* [SWE-Sharp-Bench](https://arxiv.org/abs/2511.02352v2): an existing reproducible
   C# issue-resolution benchmark; the accessed v2 is identified rather than
   implying a review of its later v3
* [Belief & Evidence](https://www.microsoft.com/en-us/research/publication/belief-evidence-in-empirical-software-engineering/),
   ICSE 2016: experience-based beliefs need not correspond to project evidence
* [Extrinsic Influence Factors](https://www.microsoft.com/en-us/research/publication/extrinsic-influence-factors-in-software-reliability-a-study-of-200000-windows-machines/),
   ICSE 2014: operating-environment effects are distinct from intrinsic code
   properties, in a different application setting

The existing [RefactorBench source](https://arxiv.org/html/2503.07832v1)
reports 100 tasks across nine Python repositories. The critique described it as
180 tasks across 20 repositories. The link the critique supplied pointed to an
unrelated code-review appendix. The HITS study link required authentication, so
I did not use it as public study evidence and accessed no protected content.

I checked the full text for RefactorBench and Building to the Test. The other
additions rely on primary publication metadata and abstracts. None of this
amounts to independent replication, author verification of every research
statistic or a systematic literature review.

### Revision Validation

* The existing structural checker passes with 103 matching cited references,
   an abstract of 1,663 source characters, unique resolved labels and results
   disabled.
* Two pdfLaTeX passes with shell escape disabled produce a 42-page PDF with no
   warnings, underfull or overfull boxes, or unresolved references. The external
   build is at `/tmp/ama-paper-critique-o1Iyxr/`. The workspace PDF was
   regenerated separately during editing, and I left it untouched after the owner
   clarified.
* A fresh AI reader test found three wording gaps, about unmeasured effort,
   CR1 exposure and credit versus monetary cost. I corrected them. This was
   editorial testing. It was neither an independent empirical coder nor human
   peer review.
* I did not inspect the PDF visually because the checked toolchain had no PDF
   renderer. Compilation and clean logs say nothing about visual quality,
   accessibility, scholarly acceptance or publication permission.
* The complete local publication gates, exact-head independent assessment and
   external approval remain separate steps. No commit, push or submission is claimed.
* The tracked-edit whitespace checks pass, as does a separate check of the new
   untracked research record. The package README, bibliography and tracking
   records have no editor diagnostics. The knowledge-base index and log keep
   earlier Markdown issues, and the editor's workspace LaTeX build keeps a rerun
   notice. The fresh external two-pass log has none.

## Related Work Review of 25 October

Reviewed Pavlenko et al.,
[Towards an AI Software Factory for Data Systems, v1](https://arxiv.org/html/2609.36323v1),
submitted 28 September 2026 and retrieved 25 October 2026. The
[arXiv metadata](https://arxiv.org/abs/2609.36323v1) supplies the 26-author
bibliographic record. The manuscript and reusable bibliography now include it
as `pavlenko2026factory`.

* The paper bears directly on feedback starvation and reflective delegation.
   Hotspan selects evidence-backed optimisation targets, and Darwin's agents
   use test and runtime feedback to generate, refine and select hypotheses.
   This is bounded steering against measurable objectives in existing systems.
   It gives no evidence of autonomous product selection.
* Its World Model keeps raw evidence apart from rebuildable views and compact,
   provenance-linked retrieval, and updates are reviewed. That offers an
   alternative to expecting every session to read an accumulating log. It is
   untested against this case's learning evaporation. The fine-tuning evidence
   is an early circle-packing demonstration and does not show durable
   engineering judgement in general.
* The reported threefold productivity estimate counts application-work PRs
   per engineer-hour and excludes the 57% of team time spent on infrastructure
   and repository onboarding. Output enters engineering review queues. The 13.8%
   mean performance gain applies to the best-performing 20 of 45 OSS systems.
   Neither number is a controlled estimate of maintainability or end-to-end
   delivery effectiveness.
* The token-efficiency comparator is inconsistent within v1. The introduction
   and Section 2.3 associate 22x with OpenEvolve, but Section 4 reports 22x
   against MAP-Elites and 17x against OpenEvolve. The manuscript neither imports
   that multiplier nor tries to resolve the discrepancy.
* The novelty wording now concerns the effect of scheduled consolidation
   between feature additions. It no longer claims to invent automated improvement
   or agent reflection. The reviewed paper does not isolate that intervention or
   evaluate an unforeseen change request. This focused review is not an
   exhaustive literature search.

The experiment's hypotheses, thresholds, budgets and tagged materials are
unchanged. Reported findings are attributed to the source authors. Checking the
sources is not independent replication, and the manuscript author's verification
of research statistics is still pending.

## Files

| File | Purpose |
| --- | --- |
| `main.tex` | Paper source. The bibliography is embedded, so it compiles on arXiv without BibTeX. |
| `fig-log-growth.png` | Figure 1: words and hedging phrases appended to the project log per day (400 dpi). |
| `fig-causal-loop.png` | Figure 2: the reinforcing loop and the feedback-first intervention (400 dpi). |
| `references.bib` | Reusable BibTeX entries, including the embedded cited bibliography; both bibliographies are ordered by key. |
| `anc/case-evidence-matrix.json` | Machine-readable O1-O5 index distinguishing reported source locators, author accounts and missing release/execution evidence; not new independent corroboration. |
| `anc/supplementary-context.md` | Practitioner/framework context, external repository observations, proposed practices and deferred extensions moved outside the main PDF. |
| `anc/log_metrics.py` | Recomputes the log measures in Appendix A from `docs/reference/log.md` at commit `29c6b51`; `--json` writes the per-day data. |
| `anc/log_daily.json` | Per-day entries, words and hedging phrases (output of `log_metrics.py --json`). |
| `anc/make_figures.py` | Redraws both figures from `anc/log_daily.json`. |
| `anc/check_paper.py` | Reports the current approximate body count and checks citations, labels, environments, braces, inline comments and abstract length. Historical comparison is optional. |
| `anc/test_paper_tooling.py` | Isolated stdlib regressions for the paper checker and exported TCR helper. |
| `anc/protocol_checks.py` | Historical check of rank-test floors and the earlier eight-feature A/B proposal; it does not validate active ten-feature five-arm execution. |
| `anc/test_protocol_planning.py` | Existing regressions for the retained conditional planning/resource scenarios, historical source pins and figure labels; not validation of study execution or inferential coverage. |
| `anc/repo_history_metrics.py` | Measures path-class line churn at the pinned commit, separating literal merges from PR-numbered first-parent integrations. |
| `anc/repo_history_metrics.out.txt` | Saved history measurement, including definitions, commands and limitations. |
| `anc/mve-feature-consolidation-harness/` | Earlier MVE proposal notes: divergence log, experiment design, hypotheses and plan. Not the separate tagged study kit. |

arXiv publishes everything under `anc/` as ancillary files.

### Tooling export provenance

The minimal [TCR helper](anc/mve-feature-consolidation-harness/tcr) is adapted
from private `jmservera/ama-thought-mve`, `skeleton/tcr`, commit
`20e7f97c5c162cffd0f771ce501e146081912edc`, Git blob
`aa35d75d77ec13aab2384481917e66c243e8ba64`, using the source supplied by the
parent. The adaptation replaces the shared log with a cleaned-up per-invocation
log and includes test, staging and commit failures in the rollback path, with
stage-specific diagnostics and nonzero status. It retains `make -s test`, the
`tcr:` commit prefix and the untracked `reports/` exclusion. It is not the
full registered study kit, and I claim no fix to the private source.

The helper is destructive. Use it only in an explicitly disposable worktree,
never in AMA or the private study repository. See its
[usage and rollback limits](anc/mve-feature-consolidation-harness/experiment-design.md#5-the-harness-consolidation-step-arm-b).
The checker runs without Git or repository metadata, including on source archives.
When the old object is missing it reports `HISTORICAL_COMPARISON UNAVAILABLE`
and still validates the current paper. Existing historical-comparison output
is kept when that source is available.

## Figures

The figures are plain PNG files generated from public data in the repository, so they carry no document protection. pdfLaTeX reads PNG directly. SVG does not work for arXiv: the `svg` package needs Inkscape and shell escape, and arXiv does not run shell escape.

Before you upload, check that the PNG copies synced to your OneDrive open without a protection prompt. If any copy has picked up protection, redraw the figures on a machine outside the corporate tenant:

```bash
pip install matplotlib pillow
python3 anc/make_figures.py          # writes both PNGs next to main.tex
```

To rebuild the data from the public repository first:

```bash
git clone https://github.com/jmservera/ama && git -C ama checkout 29c6b512f5e68733bb2cc1882343db39f5eb2cad
python3 anc/log_metrics.py ama/docs/reference/log.md --json anc/log_daily.json
```

## Compile

* Overleaf: upload the submission ZIP as a new project and select pdfLaTeX. It contains `main.tex` at its root and compilation dependencies under `tex-inputs/`; arXiv reserves root-level `anc/` for non-compilation ancillary material.
* Locally: run `pdflatex -no-shell-escape main.tex` at least twice, repeating until the final log has no unresolved or changing references. The packaging tool enforces a four-pass limit.
* From this package directory, run `chktex main.tex`. The local [.chktexrc](./.chktexrc) recognizes whitespace-consuming commands, literal identifiers and valid arm-contrast en dashes without disabling warning categories. From another directory, pass its path with `chktex -l`. Use the retained external Tectonic build below to inspect compiler warnings.
* Packages, all in TeX Live: lmodern, geometry, microtype, graphicx, booktabs, tabularx, placeins, array, enumitem, xcolor, natbib, xurl, caption, hyperref.
* Completed exploratory results are unconditional; the former results switch and inactive reporting TODO branch have been removed. Historical requests and their dispositions remain in the revision record and Git history. Publishing further results requires checked runs, source-bound analysis and owner authorization.
* The final article source retains its editor compiler directive and explicit author-confirmation comments. Dated editing and permission records remain in the revision report and historical source bindings; compiler guards, disclosures and the additive Supplement remain active.
* Focused source checks: from this package, run `python3 -B -m unittest discover -s anc -p 'test_*.py' -q` and `python3 -B anc/check_paper.py`.
* Tectonic also works. Keep compiler intermediates and logs, caches and rendered inspection pages in an explicit external build directory. Inspect its actual log and PDF before replacing only `main.pdf`. The optional `--check-latex-log` expects a pdfLaTeX-specific output marker, so it does not validate a Tectonic build.
* Tectonic can report undefined forward references and changed citations, labels or bookmarks on its first pass. Its automatic reruns resolve them. The `-p` stream includes every pass, so `tectonic -p main.tex | grep '[Ww]arning'` also prints warnings that have already been resolved; that pipeline's exit status comes from `grep`, not the compiler. Check the final retained log after a successful build:

  ```bash
  tectonic -p --untrusted --keep-logs --keep-intermediates --outdir /path/to/build main.tex &&
    grep -En 'Warning:|Overfull|Underfull|Missing character:|^!' /path/to/build/main.log
  ```

  No output from `grep`, with exit status 1, means no matching final-log diagnostics. Exit status 2 indicates a `grep` error, not a clean log. Any diagnostics that remain in the final log need investigation.

## What changed in draft v2

* New thesis: feature accumulation degrades software, and agents speed this up through compounding errors and output that exceeds review capacity.
* New background on software evolution (Lehman, Parnas, Eick, Cunningham, Fowler, Tornhill and Borg, Besker) and on recent studies of agent-driven decay. Counter-evidence is included (Echoes of AI, SWE-Maintain, and the Herraiz caveat on Lehman's laws).
* New Table 4, which maps the base rate and the two accelerants to the five mechanisms.
* New Section 7.1, *A consolidation procedure*: after every feature the loop stops, then reviews and refactors through test && commit || revert before the next feature starts.
* New Section 8, *Testing the procedure*, covering hypotheses H1-H7, three arms (no consolidation, consolidation, placebo review-only), suites, measures, analysis and bias controls.
* New Appendix B with the consolidation prompt.
* New sources, including Lanzetta (two articles) and Lamanna (*Changing how we build*).

## Original draft v3 changes

These notes record the earlier revision, before the author clarification below.
Where they conflict with it, the clarification supersedes its method attribution and experimental choices.

* Reframed the paper as an exploratory single-case study with a
   participant-observer, a defined unit of analysis and a bounded MVP-week contrast.
   Added the ACM SIGSOFT reporting standard and disclosed AI-assisted log coding.
* Added nine references on flow and debt, deployed consolidation practices, PR-based
   evaluation, CodeHealth and registered-report protocols. The novelty is a
   controlled test of a practised intervention, not the invention of clean-up.
   Waseem et al.'s full text contains descriptive scan counts, which contradicts the
   review brief's blanket description of no quantitative results.
* Softened causal claims and added six rival explanations, including migration,
   my gate rules, budget constraints and identity setup.
* Changed the exploratory first pass to four runs per arm and eight features,
   and kept five runs per arm per suite for the main study. Verified the rank-test
   floors and the 64 feature, 32 consolidation and eight change-request steps:
   46 agent-hours, or 11.5 idealised hours across four parallel sessions.
* Scoped first-pass CR1 to the available F1-F8 behaviour. The main study still
   needs F9-F10 for the full ranking and export checks. Both variants must be
   frozen before the pilot, so they cannot be selected after seeing results.
* Made suite a fixed effect and run a random intercept. Clarified interval-based
   verdicts, the post-consolidation end state, missing features, change-request
   regression protection and B's extra time. Registration remains pending, and I
   have invented no date or URL. The divergence log records the pre-run changes.
* Reported the Sonnet 5.5 worker selector introduced on 21 October in PR #420,
   Automatic coordinator selection and the separate deployed assistant model.
   I still need to check the historical HVE and underlying service versions.
* Added human intervention rate (HIR) and intervention-demand rate as secondary
   measures, with whole-feature-cycle denominators, event reasons and human
   minutes. Primary runs remain unassisted. An actual rescue is a recorded
   deviation, not a replacement run. No hypothesis threshold or adoption gate changed.
* Added pinned line-churn evidence with literal-merge and squash-integration
   views. Artefact/source additions are 29.28 before the loop and 10.27 during it.
   These counts do not establish structural decay. I did not measure complexity
   because lizard was not installed, and I installed no dependencies.
* Retained the main title, Monday checklist, PNG figures and `\resultsfalse`.
   I did not attempt the optional 15% body cut, because the required additions
   increase the body. The experiment has not been run.

## Author clarification of 25 October

* Corrected the method: the author supplied observations, explanations and the
   consolidation remedy, and GitHub Copilot organised and named patterns. There
   was no systematic entry-by-entry qualitative coding. Microsoft 365 Copilot
   summarised and found sources, and Copilot Cowork generated slides.
* Recorded the author-confirmed HVE snapshot, programme name, historical model
   roles and selective specification review. Replaced daily MVP use with
   intermittent use and separated product-use feedback from approvals and
   technical oversight.
* Qualified learning loss and noted documentation growth before the backlog
   loop. Generalised partner descriptions. Permission for the peer observation
   and external publication remains pending.
* Added the account-wide rolling 28-day dashboard totals with their limits:
   USD 1,809 price-list consumption value, not an invoice or AMA-only cost.
* Recorded the selected S1 design: A/B/C, ten features plus CR1, four independent
   runs per arm; Sonnet 5.5, medium effort and CLI 1.0.103. Local execution leaves
   residual access risk, because it lacks container isolation. S2 library lending is deferred.
* Checked the accepted arithmetic: 212 first-pass sessions and 89 agent-hours;
   262 sessions and 109 agent-hours including the pilot. The combined ceiling
   is 2,500 AI credits. Its relation to the separate $500 budget is unverified.
* Kept HIR extraction prospective: Cowork extraction, then author checks
   and adjudication. Telemetry coverage is unverified, and missing events do not
   establish zero interventions. Independent suite review, research-statistic
   checks, figure verification and reviewer participation remain TODOs.
* Added HG-DAgger and ThriftyDAgger as precedents for measuring intervention,
   with explicit HIR and demand-rate formulas. The cycle denominator is a
   study-specific adaptation, not a universal standard. Incidence, event
   frequency and human effort remain distinct.
* Reframed the abstract, research questions and discussion around whether an
   additional agent can perform reflection and course correction. The current
   consolidation experiment is a bounded first test. It does not test unrestricted
   steering, and it does not show that reflective work is exclusively human. Tagged study
   materials, hypotheses and thresholds are unchanged.
* Preserved earlier protocol proposals and kept `\resultsfalse`. A Git tag is
   not registration, and earlier started runs cannot be retrospectively
   described as preregistered.

Run the saved checks from the repository root, using its existing environment:

```bash
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/check_paper.py
.venv/bin/python -B -m unittest discover -s docs/capstone/thought-leadership/everything-but-the-software/anc -p test_paper_tooling.py -v
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/repo_history_metrics.py
```

The historical `protocol_checks.py --check-documents` mode expects the earlier
proposal wording across the manuscript and local protocol copies. It does not
check that the current revision agrees across files. Its legacy arithmetic remains historical;
the accepted A/B/C design has 120 feature, 80 post-feature and 12 CR sessions:
`(120 * 30 + 80 * 15 + 12 * 45) / 60 = 89` agent-hours, excluding the pilot.

## Before you submit

1. Resolve every `TODO(author)` comment in `main.tex` (search for `TODO`):
    * verify research statistics against original papers and the log-growth figure against daily data;
    * retain source metadata, dashboard evidence and original instruction messages where available;
    * recover historical runtime/build identifiers without inventing unexposed versions;
    * obtain permissions and confirm partner anonymisation without naming either partner or its staff;
    * verify the exact tagged protocol, suite, analysis and prior-run chronology before registration;
    * document the exploratory-framing amendment and complete registration before fresh runs, retaining the real date and URL;
    * complete independent suite review, reviewer recruitment and HIR coverage checks;
    * reconcile credit and monetary limits, calibration choices and analysis rules;
    * write results and update acknowledgements only after the corresponding work occurs.
   Also resolve the visible protocol limitations before treating a fresh study
   as confirmatory: exact costing and endpoint rules, sample precision, multiplicity,
   failure and missing-data disposition, CR1 non-exposure and effective blinding.
   This revision keeps the design as it was and supplies none of the missing checks.
2. Treat the local MVE copies as historical proposals. Archive the exact authorised registered study materials separately, keep the originals, and exclude credentials, DLP sidecars and unapproved internal content.
3. Rewrite in your own voice where needed. The rubric allows AI drafting, but the idea, evidence and recommendation must be yours.
4. Get the internal approvals Microsoft requires for external publication.
5. Compile, then read the PDF end to end. Check tables and figures for overflow.
6. arXiv publishes the source files, comments included. Before you upload, strip the comments (for example with `arxiv_latex_cleaner`) and leave out `README.md`.

## Running the experiment with HVE Core

Continue from the separately tagged private study kit, not from the earlier
ancillary proposal copies. Before registration, verify that the tagged record matches the accepted
design and analysis. Preserve every earlier run with its
original labels and timestamps, and start the fresh exploratory first pass only after
prospective documentation and registration. Do not change frozen materials in place or silently replace the
original design after seeing results.

## arXiv notes (checked 24 Oct 2026)

* Primary category: cs.SE. Optional cross-lists: cs.HC, cs.AI.
* Since 31 Oct 2025, arXiv CS accepts review articles and position papers only after peer-review acceptance. Research papers are not affected, so frame the paper as a data-backed case study with a method, data and threats to validity, not as an opinion piece.
* Since 21 Jan 2026, a first-time submitter in cs.SE needs either prior authorship in the domain or a personal endorsement from an established arXiv cs.SE author.
* arXiv asks authors to report significant use of generative AI. AI tools cannot be authors, and authors are responsible for all content.
* The abstract field limit is 1,920 characters. The conservative source count
   after the framing revision is 1,619, including LaTeX syntax and normalised whitespace.
