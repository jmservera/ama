---
title: Research for issue 224, legal evidence pack, EU AI Act currentness
ms.date: 2026-11-17
---

## Scope

Evidence pack only for issue #224 (OQ-019). No legal conclusion, approval, risk tier or compliance position.
Tier FOCUSED, docs plus one small tool test. Out of scope: #1818, #1641.

## Measurement (reproduction of the gap)

Baseline at origin/main eb51af5c9:

* `docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md` records the EU AI Act as `Unknown`, the EUR-Lex retrieval as failed and a Digital Omnibus delay as "unverified". It also says reg. 5 of S.I. 2026/82 was not read.
* `docs/reference/research/rai/legal-briefing-adm-ai-act.md` repeats the EU gap (failed attempts 2026-11-01 and 2026-11-04) and lists "EU AI Act text, commencement and amendments are unverified" as an open gap. It does read reg. 5.

Probe on 2026-11-17 with plain `curl` and a browser user agent:

| Source | HTTP | Result |
| --- | --- | --- |
| legislation.gov.uk S.I. 2026/82 reg. 5 (made) | 200 | Saving provision text read |
| EUR-Lex OJ L 2024/1689 (HTML) | 200 | Text read; Art. 113 as originally made |
| EUR-Lex ELI reg/2026/1744/oj | 200 | Amending act read |
| ICO ADM guidance page | 403 | Challenge page; still not retrieved |

## Findings (source readings, not conclusions)

* Reg. 5 of S.I. 2026/82: the s.80 and Schedule 6 amendments do not apply to any decision taken before 5 February 2026 to which Article 22(3) UK GDPR or s.14(1)/50(2) DPA 2018 applied.
* Regulation (EU) 2024/1689 (OJ 12.7.2024), Art. 113 as made: applies from 2 August 2026; Chapters I and II from 2 February 2025; Art. 6(1) obligations from 2 August 2027.
* Regulation (EU) 2026/1744 (Digital Omnibus on AI), of 8 July 2026, OJ 24.7.2026, in force on the third day after publication. Point (40) amends Art. 113(3): Chapter III Sections 1 to 3 (except Art. 6(5)) apply from 2 December 2027 for Annex III high-risk systems and 2 August 2028 for Art. 6(1)/Annex I systems; Art. 5(1) first subparagraph points (ba), (bb) and Art. 5(1a), (1b) from 2 December 2026. The EUR-Lex record for 2024/1689 lists 2026/1744 as `changed_by`.
* The earlier "unverified" Omnibus statement is superseded as to existence and dates. Whether any date applies to Zava stays a Legal/DPO question; territorial and role facts remain Unknown.
* Consolidated text and any other amending act were not compared. ICO guidance, Art. 22D regulations and a snapshot line comparison remain Unknown.

## Planning Readiness

Ready. Disposition: executed. Smallest change: dated update to the pack and briefing, plus a regression test that fails if the pack again calls the Omnibus unverified or omits the amending act.
