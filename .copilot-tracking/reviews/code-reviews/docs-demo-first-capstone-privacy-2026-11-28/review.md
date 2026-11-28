# Independent main-story privacy, RAI and UK-price review

## Verdict and exact target

Verdict: `approve_with_comments`.

Reviewed at: `2026-11-27T23:37:55Z` (UTC; the evidence update is dated 28 November in the owner's local time).

- Repository: `/home/jmservera/source/ama`
- Branch: `docs/demo-first-capstone`
- Implementation HEAD: `01ad9aeb8eae5ad72b33f20882fab3997384b979`
- Previous-published base: `3da0011a89281482aeb6500e6524c9fe05c56d42`
- Findings: one Low documentary binding error; no Critical, High or Medium findings.

HEAD was confirmed before review and again immediately before artifact writing. The serialized `increment.diff` matches the exact Git diff between these commits. The inspected slide source, PPTX, PDF, generated script/question bank, runbook and reviewed regulatory update match their HEAD blobs.

This verdict concerns the requested main-story claims and their delivery evidence. It is not an approval of the whole PR, application architecture, deployed processing or operational readiness.

## Scope and audience strategy

Reviewed S01/page 1, S11A/page 13, S15/page 17, S17/page 21 and B28/page 56, including their actual native PNGs and generated PowerPoint notes. Reviewed their primary spoken text, the Executive Hook, related mission/price qualifications in the primary route, and the cited privacy/residency/RAI evidence. The route and optional-show checks concern timing and separation, not a fresh review of every appendix claim.

The mixed executive/technical panel needs a bounded validation decision, rather than permission to deploy or process real resident data. The sequence suits Sergeant preferences at the opening and decision, then Scientist preferences for mechanisms, evidence and price limits. Therapist framing supplies resident benefit, choice and assisted service. These are communication preferences, not personality classifications.

The early demonstration gives the panel an owned next action before the technical detail. Later privacy and RAI explanations preserve that factual core without claiming observed benefits, resident interviews or stakeholder approval.

The original 17-file readiness scope recorded in `diff-state.json` was not retried. Its original worker refusal remains unchanged in `dispatch-manifest.json`. No nested agents were used.

## Finding

### R1 — Low: the validation record retains the previous runbook digest

Location: `docs/capstone/source/validation.json:294`.

The recorded `pitch.runbook_sha256` is `0adeb77b8533df19f3fc4c90a79d1f4998a4ceb96df0b69c8bee74d7599f6f12`. That is the digest of the runbook at the previous-published base, not the reviewed HEAD.

The current `docs/capstone/demo/runbook.md` digest is `31deb5a6f423460280b480aef7993ab87b4c0a163bbefbf58c4e3f02bd12500f`. LF normalization gives the same result. A consumer using this field cannot bind the updated privacy wording and Executive Hook to the final runbook.

Suggested correction: refresh this field from the final runbook bytes after verification, without changing source content or human approval fields.

This does not indicate stale delivered narration. Independent comparison confirmed the complete runbook is embedded correctly after relative-link rebasing, the Executive Hook matches its inline script copy, and every primary-route SAY paragraph matches the manifest. The four canonical source bindings and the delivered PPTX/PDF/script/question-bank bindings pass separately.

## Claim assessment

| Claim surface | Assessment and concrete evidence |
| --- | --- |
| Not-for-profit mission and accountability | Supported as owner-confirmed fictional-company information, not inferred charity status. S01 visibly names resident benefit and accountable spend; `docs/capstone/source/slides.json:28-43` preserves unknown legal form, registration and charitable status. `docs/reference/research/company/company-profile-research.md:21-39` supports this distinction. The primary script at `docs/capstone/pitch/speaker-script.md:29-62` rejects disclosure of other households' records and treats benefits as proposals. |
| UK GDPR privacy story | S17 visibly includes purpose, minimal data, retention, rights and pending Legal/DPO approval. Its notes at `docs/capstone/source/slides.json:2505-2513` distinguish lawful basis from works consent and monitoring choice, avoid an automatic Article 9 condition for not-for-profits, and preserve the draft DPIA's lack of approval. The reviewed update at `docs/reference/regulatory/reviewed-updates/2026-11-28-privacy-residency-rai-review.md:36-57` supports those qualifications. |
| UK Standard-model target | S11A's visible title says target and proof before release. Its drawing still shows Global deployment/not UK-only and Sweden Central. Notes at `docs/capstone/source/slides.json:1294-1296` separate regional inference, catalog availability, quota, lifecycle and actual deployment. The primary narration at `docs/capstone/pitch/speaker-script.md:83-87` does not claim a wholly UK deployment. |
| Identity and provider access | S11A's narration and notes preserve separate identity, provider-access and backup review. The reviewed update at `docs/reference/regulatory/reviewed-updates/2026-11-28-privacy-residency-rai-review.md:43-48` also names logs, monitoring, support and control-plane checks. Neither UK hosting nor private endpoints is presented as proof of complete residency or compliance. |
| Responsible humans decide | S15 visibly separates named evidence review from consent, professional sign-off, Finance approval and independent quality acceptance. Its primary narration at `docs/capstone/pitch/speaker-script.md:89-99` requires competence, evidence, time and authority to correct or reject before consequences. Notes at `docs/capstone/source/slides.json:2427-2428` retain the blocked dated Quality model leg and unproved operational acceptance. The RAI report's opening and NIST assessment remain partial engineering evidence, not fairness or safety certification. |
| Global nano and UK price | B28 visibly says Global nano is not a UK-resident rate and UK-only inference needs repricing (`docs/capstone/source/slides.json:5743-5750`). Its notes at line 5770 make regional eligibility, quota and quality/lifecycle checks prerequisites. The primary script at `docs/capstone/pitch/speaker-script.md:101-105` prices the observed public-cloud configuration, not the UK target. The dated cost model separately labels GlobalStandard nano and Standard regional mini; the USD 0–50 allowance is not permission for a non-UK call or a maximum invoice. |

Original case-study and addendum grounding was read alongside the company profile and knowledge-base index. The retained research record's C11–C15 and W16–W22 sources were assessed against the dated reviewed update, draft chat/memory DPIA and project RAI review.

Independent public-source spot checks corroborated:

- UK GDPR Article 22A's meaningful-human-involvement distinction and Article 22C's covered-decision safeguards, using their current legislation.gov.uk pages.
- The ICO restricted-transfer chapter's adequacy/safeguards/derogation routes, rather than a blanket UK-only rule.
- The RSH standard's England/registered-provider scope and 1 October 2026 update.
- Microsoft's deployment-type geography distinction, and its exact Standard/Regional Europe table listing `gpt-4.1-mini`, version `2025-04-14`, for UK South. The standard-category pivot alone also contains Global tables; the check used the Standard/Regional heading.
- Microsoft's EEA-only abuse-reviewer location wording and future Modified Abuse Monitoring change notice. The ICO ADM page still identifies its revised guidance as draft consultation.

These checks establish support for the qualified presentation wording, not company applicability, subscription capacity, contractual acceptance or legal sign-off.

## Actual delivery and timing evidence

Inspected the supplied `privacy-build-2/native/slide-001.png`, `slide-013.png`, `slide-017.png`, `slide-021.png` and `slide-056.png` at their native 1600 × 900 size. The required qualifications are visible; no material clipping or overlap was observed on these five frames. S11A's diagram text is image content in the PDF, so absence of those labels from text extraction is not treated as missing visible content.

Independent read-only checks established:

- The native build's PPTX and verified-navigation PDF equal the delivered files in `docs/capstone/deck`.
- The native-render record binds to PPTX SHA-256 `3499cbe39cc9fb8138bf629589c5cba043473205846f7671462e743286674687`; the delivered PDF binding also matches.
- All five generated PowerPoint note parts contain their exact current primary SAY text and the relevant qualifications.
- All four canonical source bindings match: manifest, asset catalog, builder and native helper. Delivered speaker-script and question-bank digests match. R1 is the separate runbook-record exception.
- The complete embedded runbook and short Executive Hook match their source after documented link rebasing.
- The primary native custom show has 17 pages in the declared order. Its prepared total is 780 seconds, including the 110-second demo after the initial 30 seconds: `00:30–02:20`. The 120-second reserve remains `13:00–15:00`.
- The separate optional custom show has seven pages and 360 seconds. The script requires six additional confirmed minutes and excludes it from the primary reserve.
- The final focused fit record contains 42 changed frames and zero overflow flags. The delivered PDF contains 56 pages and 111 internal links with valid page destinations.

The prior record reports 26 selected tests plus three subtests passing. Tests, PowerPoint rendering and link-hit-region interaction were not rerun in this review; the checks above used the existing output and read-only comparisons. Spoken word counts are compatible with the allocated windows, but arithmetic and prepared text do not prove a performed rehearsal.

## Limits, delivery guidance and next decision

The 28 other revised-frame warnings and 179 inherited bounds warnings remain explicitly unaccepted. This five-frame visual review neither clears them nor establishes whole-deck accessibility, physical-projector readability, keyboard behavior or real assistive-technology acceptance.

No private datasets or settings were read. No deployment, paid inference, source edits, Git mutation, publishing or external review/comment posting occurred. No general PR comment draft was authored.

Legal/DPO applicability, lawful basis, special-category conditions, retention, rights and transfers remain human decisions. Actual service/model residency, identity/provider terms, model capacity and lifecycle, effective oversight, fairness/error evaluation and operational safety remain unproved. The dated RAI review is not a current whole-application re-audit.

For delivery, keep the opening and final ask direct. State the constructed-data and route label before the demo; point to the missing check and responsible person rather than treating example Accept/Edit/Reject controls as evidence of oversight. Slow down at the UK target and repricing qualifications. Return at demo 01:50, and open the six-minute sovereignty story only with a separate confirmed slot.

The next local correction is R1's stale digest. The bounded review is complete; human validation and all merge/posting permissions remain ungranted. Broader exact-head readiness remains pending and is not inferred from this verdict.

## Disclaimer and Human Review

> [!CAUTION]
> **Disclaimer:** This agent is an assistive review tool only. It does not provide engineering sign-off, security certification, or compliance approval and does not replace qualified human code review, security review boards, or other professional reviewers. The output consists of AI-assisted findings, observations, and suggested remediations to support a reviewer's own analysis and decision-making. All code-review findings — including functional, standards, and accessibility observations — generated by this tool must be independently reviewed and validated by a qualified human reviewer before acting on them, merging changes, or treating any finding as resolved. Outputs from this tool do not constitute engineering approval, merge authorization, or compliance certification.

- [ ] Reviewed and validated by a qualified human reviewer
