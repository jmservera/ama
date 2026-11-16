---
title: Issue 1818 final-candidate critique (single pass)
date: 2026-11-16
verdict: proceed with applied findings
---

* Role leakage: provider must be built server-side and default to `restricted`; browser must never decide. Applied in P2.
* Unbounded cost: consent per home is N queries; cap 100 homes and mark rest `not-loaded`. Applied in P1.
* Cluster mode has no sensor data; filter must say it applies only to individual homes. Applied in P3.
* Map privacy test asserts no private packets; new keys use only fixed vocabulary strings. Applied.
* Uncalibrated is an always-true property today; surfaced as a constant badge, not a transient state. Accepted.
* Live Azure walkthrough criterion stays unticked; no claim of live transport. Accepted.
