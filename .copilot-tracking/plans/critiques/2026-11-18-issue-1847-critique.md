---
title: Issue 1847 critique
---
# Critique (one pass, self)

Verdict: proceed with README-only delta.

* Risk: re-implementing delivered code duplicates #1849; rejected. Compatible advice: state measured versus hypothesised claims in the doc; applied by citing only tested behaviour.
* Gap noted, not fixed: a noneditable install loaded first by another test module is rejected, not isolated, by design; isolating every test module is a separate follow-up.
* Tier: test-only plus docs; FOCUSED holds; the issue's full gate stays with the coordinator.
