---
title: Issue 1847 plan critique
---
# Critique (single final-candidate pass)

Verdict: proceed. Findings, all applied directly:

* Check foreign modules before any `sys.path` mutation so rejection leaves no partial state.
* Do not reject a namespace root whose only foreign entry is a `__path__` item with no loaded foreign submodule; source roots prepended first make it safe.
* Regression must fail against the original purge (it imports successfully there), so assert both rejection and that the foreign module is still in `sys.modules`.
