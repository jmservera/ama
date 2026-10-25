# Review: demo basemap configuration (issue 119 demo slice)

Date: 2026-10-25. One independent read-only review (code-review agent) of the staged diff and artifacts, run after the live change and docs, before the first commit dad6aa07.

Verdict: PASS-WITH-FINDINGS. No overclaim of #119 acceptance, production provider approval, screen-reader acceptance or browser render. Documentation matches `server.py` (CSP host, Referrer-Policy, attribution) and `app.js`; links resolve; ASCII and `*` lists. The private before and after comparison showed only the two env entries differing (plus expected revision-name and last-modified metadata). Cost is stated as an estimate.

Findings (all addressed in the changes file errata, no history rewritten):
1. Medium: minute stamps in the research, critique and tests text were wrong or inconsistent with the 12:18:15Z live start. Errata record that the stamps are not evidence and that order is supported by `update.log` and the plan's appended critique.
2. Low-Medium: the details file kept superseded pre-critique steps. Marked superseded; the plan's critique section is authoritative.
3. Low: time and cost gate evidence timing and the allowance difference recorded in the errata.
4. Info: exact az quoting cannot be proven from `update.log`; recorded in the infra README.

Residual limitations: no browser render, no on-screen attribution, no Referer observation, no owner check; Referer and cache behaviour are code-level only. The change is operational and time-limited to 16:02Z; configuration is not a provider decision. Hosted CI, human review and the gate remain separate.
