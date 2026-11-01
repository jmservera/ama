<!-- markdownlint-disable-file -->
# Research: Issue #224 UK automated-decision and EU AI Act applicability review

Task: `issue-224-adm-ai-act-legal-review`. Date: 2026-11-01. Disposition: executed.

## Prior delivery check

* Merged or open PRs referencing #224: none deliver it. PR #534 (RAI review) and PR #504 (release records) expressly leave the legal screening undelivered. Closure audit batch 2 (2026-10-31) lists all five criteria as unmet.
* Owner decision (2026-10-15): Juan Manuel Servera records the legal review as Legal owner once content is ready; the issue stays open until then.
* Consequence: an agent cannot supply the Legal/DPO decision. The deliverable is a review pack: a dated official-source check, an unsigned decision record, review items, non-inference rules and feed notes. Criteria 1 stays unmet.

## Official sources retrieved on 2026-11-01 (legislation.gov.uk, HTTP 200)

| Fact | Source |
| --- | --- |
| Data (Use and Access) Act 2025 s.80 (automated decision-making) is "in force at Royal Assent for specified purposes" (s.142(1)(2)(h)) and "in force at 5.2.2026 in so far as not already in force by S.I. 2026/82, reg. 2(j) (with reg. 5)" | legislation.gov.uk/ukpga/2025/18/section/80 |
| The page records no known outstanding effects; versions dated 19/06/2025 and 05/02/2026 | same |
| S.I. 2026/82 (Commencement No. 6 and Transitional and Saving Provisions) Regulations 2026, reg. 2: provisions come into force 5 February 2026 | legislation.gov.uk/uksi/2026/82 |
| Reg. 5 transitional text was not parsed from the retrieved page | gap, recorded as unknown |

## Not retrievable

* EUR-Lex Regulation (EU) 2024/1689: the fetch returned a bot challenge (HTTP 202, empty body). No official content retrieved.
* A web search returned secondary commentary claiming a Digital Omnibus on AI delayed Annex III high-risk obligations to 2 December 2027. This is unverified secondary discovery; it is not recorded as a fact.
* ICO guidance currentness was not checked.

## Repository findings

* Local snapshot `docs/reference/regulatory/data-protection/uk-gdpr-current-text.md` (retrieved 2026-09-19) contains Articles 22A to 22D. Its date precedes the full commencement date in the official source (2026-02-05), so no snapshot text conflict is expected, but the snapshot has not been compared line by line with the official point-in-time text.
* Seed card `automated-decision-safeguard` (`src/core/src/zava_forward/core/rulecards.py:98-109`) cites "Article 22 (illustrative citation)". The in-force provisions are Articles 22A to 22C, so the citation is outdated. Approver is "Named DPO (unassigned)".
* Card trace: requirements FR-034 and RULE-021; tests `src/core/tests/test_rulecards.py`, `src/agents/tests/test_ai_eval.py`.
* OQ-019 in the PRD holds the open question. Juan Manuel Servera is the named exercise Legal, Compliance and DPO owner (`project-rai-review.md`).
* Relevant text of Articles 22A to 22C is in the local snapshot lines 1159-1192 (meaningful human involvement; significant decision; special category restriction; safeguards: information, representations, human intervention, contest).

## Planning readiness

Ready: a documentation-only slice is feasible. Open limits: EU official text unretrieved; ICO guidance unchecked; Legal/DPO decision outstanding.

* Correction cycle 2026-11-01: review-thread fixes recorded in the changes artifact; scope unchanged.
