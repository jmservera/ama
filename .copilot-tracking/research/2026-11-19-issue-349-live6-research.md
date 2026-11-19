# Issue 349 live6 research

Disposition: executed. Rounds r1 to r5 reviewed. First unmet criterion: 1 (tenant owner provisioning; Graph read denied).
Finding: the r5 resident probe failure is worker-host DNS (sts.microsoftonline.com unresolved), not the product. Unit tests already cover unassigned and wrong-tenant denial.
Planning Readiness: Ready. The state file overwrote the r5 tracked state; r5 content remains in git history.
