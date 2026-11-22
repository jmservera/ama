---
title: Issue 2202 demo smoke research (2026-11-22)
---

Task: live desktop smoke of ca-cutover-test-demo-api and ca-resident-demo (sign-in, employee map live sensor items, employee AI chat, resident app load, resident AI regulatory chat). Synthetic demo, desktop only, owner decisions 2026-11-18.

Research disposition: reused. Prior probes in docs/reference/research/issue-2202-live-2026-11-21/ (probe_staff.py, probe_staff_chat.py, probe_resident.py) and issue-2202-live-deploy-2026-11-22/ already drive these flows; they read credentials at run time without printing.

Open acceptance criteria (issue 2202): images rolled; revisions Healthy and hardening enforced with rollback and agents-app difference; owner demo checks (charts, gauges, consent, chat routing, half of homes with readings); live receipt plus log entry.

Planning Readiness: Ready.
