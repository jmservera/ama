---
title: Issue 891 chat call accounting C1 critique
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109-c1
---

## Execution

* One critique, executed once by a read-only `rubber-duck` subagent after research, plan and details existed and before any test or source edit. Verdict: Revise (2 blocking, 3 significant). Dispositions are in the plan section "Critique dispositions".

## Findings as returned

* PC-001 blocking: a witness does not prove complete coverage; a provider may call `Ai.evidence` and also make an untracked call. Fix: exactness only for a trusted constrained composition; mixed or unsupported is unverified.
* PC-002 blocking: logging uncertainty while returning 1 leaves the receipt indistinguishable from a measured count. Fix: propagate provenance to receipts or reject unsupported providers.
* PC-003 significant: nested witnesses shadow the outer; copied contexts can mutate a witness after the outer invocation returns.
* PC-004 significant: default `urlopen` follows redirects, so one witness increment can understate real HTTP requests.
* PC-005 significant: marker placement is ambiguous between opener construction and invocation.

## Dispositions

* PC-001 applied as documented scope (composition trust boundary). PC-002 partly applied: explicit log, upper-bound semantics, README; receipt provenance routed as follow-up because `chat_panel.py` is shared and not owned. PC-003 applied (closed state, tests). PC-004 applied as a defined metric and documented limit. PC-005 applied (placement after opener construction).
EOF
